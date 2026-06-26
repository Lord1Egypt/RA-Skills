#!/usr/bin/env python3
import argparse
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    title TEXT,
    raw_text TEXT NOT NULL,
    summary TEXT,
    source TEXT DEFAULT 'chat',
    md_file TEXT,
    md_anchor TEXT,
    payload_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    entry_id TEXT PRIMARY KEY,
    amount REAL,
    currency TEXT,
    category TEXT,
    subcategory TEXT,
    pay_method TEXT,
    merchant TEXT,
    FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    entry_id TEXT PRIMARY KEY,
    status TEXT,
    priority TEXT,
    project TEXT,
    due_date TEXT,
    completed_at TEXT,
    FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE IF NOT EXISTS schedules (
    entry_id TEXT PRIMARY KEY,
    schedule_date TEXT,
    start_time TEXT,
    end_time TEXT,
    location TEXT,
    status TEXT,
    FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE IF NOT EXISTS ideas (
    entry_id TEXT PRIMARY KEY,
    idea_type TEXT,
    status TEXT,
    related_task_id TEXT,
    FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS entry_tags (
    entry_id TEXT NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (entry_id, tag_id),
    FOREIGN KEY(entry_id) REFERENCES entries(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()

    print(f"initialized database at {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
