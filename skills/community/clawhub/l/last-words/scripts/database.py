#!/usr/bin/env python3
"""
Database management for last-words skill.
Stores messages, configuration, and activity logs in SQLite.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_DIR = Path.home() / ".openclaw" / "last-words"
DB_PATH = DB_DIR / "data.db"


def init_db():
    """Initialize the database with required tables."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Main message table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            audio_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Delivery configuration table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT CHECK(method IN ('email', 'wechat', 'phone')),
            contact TEXT NOT NULL,
            smtp_host TEXT,
            smtp_port INTEGER,
            smtp_user TEXT,
            smtp_pass TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Activity log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_chat_at TIMESTAMP,
            days_inactive INTEGER,
            warning_sent INTEGER DEFAULT 0,
            warning_level INTEGER DEFAULT 0,
            delivered INTEGER DEFAULT 0,
            delivered_at TIMESTAMP,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Status tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Initialize last_chat_at if not exists
    cursor.execute("INSERT OR IGNORE INTO status (key, value) VALUES ('last_chat_at', ?)",
                   (datetime.now().isoformat(),))

    conn.commit()
    conn.close()


def save_message(content: str, audio_path: str = None):
    """Save or update the final message."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear old message, keep only one
    cursor.execute("DELETE FROM message")
    cursor.execute(
        "INSERT INTO message (content, audio_path) VALUES (?, ?)",
        (content, audio_path)
    )

    conn.commit()
    conn.close()
    return True


def get_message():
    """Get the stored message."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT content, audio_path, created_at FROM message ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"content": row[0], "audio_path": row[1], "created_at": row[2]}
    return None


def save_config(method: str, contact: str, smtp_host: str = None, smtp_port: int = None,
                smtp_user: str = None, smtp_pass: str = None):
    """Save delivery configuration."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM config")
    cursor.execute("""
        INSERT INTO config (method, contact, smtp_host, smtp_port, smtp_user, smtp_pass)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (method, contact, smtp_host, smtp_port, smtp_user, smtp_pass))

    conn.commit()
    conn.close()
    return True


def get_config():
    """Get delivery configuration."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT method, contact, smtp_host, smtp_port, smtp_user, smtp_pass FROM config LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "method": row[0],
            "contact": row[1],
            "smtp_host": row[2],
            "smtp_port": row[3],
            "smtp_user": row[4],
            "smtp_pass": row[5]
        }
    return None


def update_last_chat():
    """Update the last chat timestamp to now."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT OR REPLACE INTO status (key, value) VALUES ('last_chat_at', ?)",
        (now,)
    )

    conn.commit()
    conn.close()


def get_last_chat():
    """Get the last chat timestamp."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM status WHERE key = 'last_chat_at'")
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return datetime.fromisoformat(row[0])
    return datetime.now()


def log_check(days_inactive: int, warning_sent: bool = False, warning_level: int = 0,
              delivered: bool = False):
    """Log an activity check."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    last_chat = get_last_chat()
    delivered_at = datetime.now().isoformat() if delivered else None

    cursor.execute("""
        INSERT INTO activity_log (last_chat_at, days_inactive, warning_sent, warning_level, delivered, delivered_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (last_chat.isoformat(), days_inactive, int(warning_sent), warning_level,
          int(delivered), delivered_at))

    conn.commit()
    conn.close()


def get_last_delivery_status():
    """Get the last delivery/warning status."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT days_inactive, warning_sent, warning_level, delivered, checked_at
        FROM activity_log
        ORDER BY id DESC LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "days_inactive": row[0],
            "warning_sent": bool(row[1]),
            "warning_level": row[2],
            "delivered": bool(row[3]),
            "checked_at": row[4]
        }
    return None


def reset_all():
    """Reset all data."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM message")
    cursor.execute("DELETE FROM config")
    cursor.execute("DELETE FROM activity_log")
    cursor.execute("DELETE FROM status")

    conn.commit()
    conn.close()
