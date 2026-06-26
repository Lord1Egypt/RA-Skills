#!/usr/bin/env python3
"""
Mapulse DB — SQLite persistence layer
Tracks users, watchlists, alerts, push logs, news, and profiles.
No payment/billing — this is a free skill.
"""

import sqlite3
import os
import json
import time
from datetime import datetime

DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create tables."""
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT DEFAULT '',
            first_name TEXT DEFAULT '',
            total_calls INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS news_seen (
            hash TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            seen_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS push_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            push_type TEXT NOT NULL,  -- 'briefing' | 'crash_alert' | 'news_alert'
            content TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS watchlist (
            user_id TEXT NOT NULL,
            ticker TEXT NOT NULL,
            added_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (user_id, ticker)
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            ticker TEXT NOT NULL,
            threshold REAL NOT NULL DEFAULT 3.0,
            active INTEGER DEFAULT 1,
            last_triggered REAL DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_push_user ON push_log(user_id);
        CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts(active, ticker);

        CREATE TABLE IF NOT EXISTS user_profile (
            user_id TEXT PRIMARY KEY,
            focus_type TEXT DEFAULT '',
            focus_stocks TEXT DEFAULT '',
            push_preference TEXT DEFAULT 'standard',
            prefer_panorama INTEGER DEFAULT 1,
            profile_complete INTEGER DEFAULT 0,
            profile_asked_at TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS news_digest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT DEFAULT '',
            category TEXT DEFAULT '',
            level TEXT DEFAULT '',
            impact_direction TEXT DEFAULT '',
            impact_text TEXT DEFAULT '',
            impact_sectors TEXT DEFAULT '',
            score INTEGER DEFAULT 0,
            batch_time TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_digest_batch ON news_digest(batch_time);
        CREATE INDEX IF NOT EXISTS idx_digest_score ON news_digest(score DESC);
    """)
    conn.commit()
    conn.close()


# ─── User Management ───


def get_or_create_user(user_id, username="", first_name=""):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    if row:
        if username or first_name:
            updates = []
            params = []
            if username:
                updates.append("username=?")
                params.append(username)
            if first_name:
                updates.append("first_name=?")
                params.append(first_name)
            if updates:
                params.append(user_id)
                conn.execute(f"UPDATE users SET {', '.join(updates)} WHERE user_id=?", params)
                conn.commit()
                row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        conn.close()
        return dict(row)

    conn.execute(
        "INSERT INTO users (user_id, username, first_name) VALUES (?,?,?)",
        (user_id, username, first_name)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row)


def increment_calls(user_id):
    """Increment call count for a user."""
    conn = get_conn()
    conn.execute(
        "UPDATE users SET total_calls=total_calls+1, updated_at=datetime('now') WHERE user_id=?",
        (user_id,)
    )
    conn.commit()
    conn.close()


def get_status(user_id):
    user = get_or_create_user(user_id)
    return (
        f"📈 *Mapulse 사용 현황*\n"
        f"📊 총 조회: {user['total_calls']}회\n"
    )


# ─── User Profile ───

def get_user_profile(user_id):
    """Get user profile, create if not exists."""
    conn = get_conn()
    row = conn.execute("SELECT * FROM user_profile WHERE user_id=?", (user_id,)).fetchone()
    if row:
        conn.close()
        return dict(row)
    conn.execute("INSERT OR IGNORE INTO user_profile (user_id) VALUES (?)", (user_id,))
    conn.commit()
    row = conn.execute("SELECT * FROM user_profile WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else {"user_id": user_id}


def update_user_profile(user_id, **kwargs):
    """Update user profile fields."""
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO user_profile (user_id) VALUES (?)", (user_id,))
    if kwargs:
        sets = ["updated_at=datetime('now')"]
        params = []
        for k, v in kwargs.items():
            sets.append(f"{k}=?")
            params.append(v)
        params.append(user_id)
        conn.execute(f"UPDATE user_profile SET {','.join(sets)} WHERE user_id=?", params)
    conn.commit()
    conn.close()


def sync_watchlist_to_profile(user_id):
    """Sync watchlist tickers to user_profile.focus_stocks."""
    conn = get_conn()
    rows = conn.execute("SELECT ticker FROM watchlist WHERE user_id=?", (user_id,)).fetchall()
    tickers = ",".join([r["ticker"] for r in rows]) if rows else ""
    conn.execute("INSERT OR IGNORE INTO user_profile (user_id) VALUES (?)", (user_id,))
    conn.execute(
        "UPDATE user_profile SET focus_stocks=?, updated_at=datetime('now') WHERE user_id=?",
        (tickers, user_id)
    )
    conn.commit()
    conn.close()
    return tickers


# ─── Init ───

init_db()


if __name__ == "__main__":
    init_db()
    print(f"DB initialized: {DB_PATH}")
    conn = get_conn()
    users = conn.execute("SELECT * FROM users").fetchall()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"  {u['user_id']}: calls={u['total_calls']}")
    conn.close()
