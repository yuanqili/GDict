from flask import Flask, render_template, g
from dict import WordEntry
import os
import sqlite3

app = Flask(__name__)


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/definition/<word>')
def word_definition(word=None):
    word = WordEntry(word)
    return render_template('definition.html', word=word.lexeme, long=word.long, short=word.short)


@app.route('/database')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT * FROM vocabulary')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

if __name__ == '__main__':
    app.run()
