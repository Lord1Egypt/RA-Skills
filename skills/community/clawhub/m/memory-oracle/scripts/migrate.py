#!/usr/bin/env python3
"""
memory-oracle: migrate.py
Schema version management. Run on upgrade to apply new migrations.

Usage:
  migrate.py              # Apply pending migrations
  migrate.py --check      # Show current version without changes
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import load_settings, SCHEMA_VERSION

SETTINGS = load_settings()

# Add migrations here as (version, description, sql_statements)
MIGRATIONS = [
    # (2, "Add tags column", [
    #     "ALTER TABLE facts ADD COLUMN tags TEXT DEFAULT '[]'",
    # ]),
]


def get_current_version(conn) -> int:
    try:
        row = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        return int(row[0]) if row else 0
    except sqlite3.OperationalError:
        return 0


def apply_migrations(conn, current: int, target: int) -> list:
    applied = []
    for version, description, statements in MIGRATIONS:
        if version <= current or version > target:
            continue
        print(f"  Applying migration v{version}: {description}")
        for sql in statements:
            try:
                conn.execute(sql)
            except sqlite3.OperationalError as e:
                print(f"    WARNING: {e} (may already be applied)")
        conn.execute(
            "INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
            (str(version),),
        )
        conn.commit()
        applied.append({"version": version, "description": description})
    return applied


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Migrate")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    if not os.path.exists(db_path):
        print("Database not found. Run init_db.py first.")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    current = get_current_version(conn)

    print(f"Memory Oracle — Schema Migration")
    print(f"  Current version: {current}")
    print(f"  Target version:  {SCHEMA_VERSION}")

    if args.check:
        if current >= SCHEMA_VERSION:
            print("  Status: up to date")
        else:
            pending = [m for m in MIGRATIONS if m[0] > current and m[0] <= SCHEMA_VERSION]
            print(f"  Pending migrations: {len(pending)}")
            for v, desc, _ in pending:
                print(f"    v{v}: {desc}")
    else:
        if current >= SCHEMA_VERSION:
            print("  Already up to date.")
        else:
            applied = apply_migrations(conn, current, SCHEMA_VERSION)
            if applied:
                print(f"  Applied {len(applied)} migrations.")
            else:
                print("  No migrations needed (schema created at latest version).")
            # Ensure version is set
            conn.execute(
                "INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
