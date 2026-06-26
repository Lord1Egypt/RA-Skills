import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "kplc.sqlite")

def get_db():
    """Return a connection usable as a context manager."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    # Restrict DB file to owner-only before first write
    if not os.path.exists(DB_PATH):
        fd = os.open(DB_PATH, os.O_CREAT | os.O_WRONLY, 0o600)
        os.close(fd)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                token TEXT UNIQUE,
                units REAL,
                amount REAL,
                raw_text TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                balance REAL,
                notes TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

if __name__ == "__main__":
    init_db()
