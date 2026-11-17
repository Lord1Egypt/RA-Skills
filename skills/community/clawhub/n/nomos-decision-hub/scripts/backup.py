#!/usr/bin/env python
"""NOMOS backup utility (v0.5).

Exports all decision records, hub reports, sessions, and events to a single
JSON file for archival / point-in-time restore. For a full binary backup,
combine with ``pg_dump``.

Usage:
    SP_DATABASE_DSN=postgresql://user:pass@host/db python scripts/backup.py --out backup.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import psycopg2
import psycopg2.extras

TABLES = ("nomos_decisions", "nomos_hub_reports", "nomos_sessions", "nomos_events")


def main() -> int:
    parser = argparse.ArgumentParser(description="NOMOS JSON backup exporter")
    parser.add_argument("--out", default="nomos_backup.json")
    args = parser.parse_args()

    dsn = os.getenv("SP_DATABASE_DSN", "").strip()
    if not dsn:
        print("SP_DATABASE_DSN not set.", file=sys.stderr)
        return 1

    conn = psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        out: dict[str, list] = {}
        with conn.cursor() as cur:
            for table in TABLES:
                try:
                    cur.execute(f"SELECT body FROM {table}")
                    out[table] = [row["body"] for row in cur.fetchall()]
                except psycopg2.errors.UndefinedTable:
                    conn.rollback()
                    out[table] = []
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(out, fh, default=str, indent=2)
        print(f"backup written to {args.out}")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
