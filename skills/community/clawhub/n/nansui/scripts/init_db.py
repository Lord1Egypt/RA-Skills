#!/usr/bin/env python3
"""Initialize the ride-insights SQLite database from the bundled schema."""

import argparse
import sqlite3
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='Initialize the ride-insights SQLite database')
    ap.add_argument('--db', required=True, help='Path to the SQLite database to create/update')
    ap.add_argument('--schema', required=True, help='Path to the SQL schema file')
    args = ap.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = Path(args.schema).read_text(encoding='utf-8')

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()

    print(f'DB ready: {db_path}')


if __name__ == '__main__':
    main()
