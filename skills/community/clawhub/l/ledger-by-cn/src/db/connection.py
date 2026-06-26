"""
Database connection and schema management.
"""
import sqlite3
import os
from pathlib import Path
from typing import Optional


def is_ascii(s: str) -> bool:
    """Check if string contains only ASCII characters."""
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def get_db_path(ledger_name: str, base_path: Optional[str] = None) -> str:
    """
    Get the database file path for a ledger.
    
    Args:
        ledger_name: Name of the ledger
        base_path: Base path for ledger data (default: ~/.openclaw/skills_data/ledger/)
    
    Returns:
        Full path to the SQLite database file
    """
    if base_path is None:
        base_path = os.path.expanduser("~/.openclaw/skills_data/ledger")
    
    # If ledger name is ASCII (English), convert to lowercase
    if is_ascii(ledger_name):
        ledger_name = ledger_name.lower()
    
    ledger_dir = os.path.join(base_path, ledger_name)
    os.makedirs(ledger_dir, exist_ok=True)
    
    return os.path.join(ledger_dir, "ledger.db")


def init_db(db_path: str) -> sqlite3.Connection:
    """
    Initialize database and create tables if they don't exist.
    
    Args:
        db_path: Path to SQLite database file
    
    Returns:
        Database connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Create tables
    cursor = conn.cursor()
    
    # Ledgers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledgers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ledger_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ledger_id) REFERENCES ledgers(id)
        )
    """)
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ledger_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT '其他',
            account TEXT DEFAULT '现金',
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ledger_id) REFERENCES ledgers(id)
        )
    """)
    
    # Openings (期初结余) table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS openings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ledger_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ledger_id) REFERENCES ledgers(id),
            UNIQUE(ledger_id, month)
        )
    """)
    
    conn.commit()
    return conn


def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Get a database connection.
    
    Args:
        db_path: Path to SQLite database file
    
    Returns:
        Database connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def close_db(conn: sqlite3.Connection) -> None:
    """
    Close database connection.
    
    Args:
        conn: Database connection to close
    """
    if conn:
        conn.close()
