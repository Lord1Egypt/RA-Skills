#!/usr/bin/env python3
"""
prune_usage.py — Delete rows older than a cutoff date from request_facts.

Usage:
    python3 scripts/prune_usage.py 2024-04-25

The cutoff date is inclusive — all rows with created_at_utc < YYYY-MM-DDT00:00:00
(in practice, strictly before midnight UTC of that date in HKT) are deleted.

After deletion, an optional VACUUM can be run to reclaim disk space.
"""
import argparse
import sqlite3
from datetime import datetime, timezone, timedelta

SKILL_DIR = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
DB_PATH = __import__("os").path.join(SKILL_DIR, "config", "usage.db")


def delete_before(conn, cutoff_iso):
    """Delete rows with created_at_utc strictly before cutoff_iso."""
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM request_facts WHERE created_at_utc < ?", (cutoff_iso,))
    count = c.fetchone()[0]
    if count == 0:
        return 0
    c.execute("DELETE FROM request_facts WHERE created_at_utc < ?", (cutoff_iso,))
    conn.commit()
    return count


def main():
    parser = argparse.ArgumentParser(description="Prune old rows from request_facts.")
    parser.add_argument("cutoff", help="Cutoff date YYYY-MM-DD (rows older than this are deleted)")
    parser.add_argument("--vacuum", action="store_true", help="Run VACUUM after deletion to reclaim disk space")
    parser.add_argument("--dry-run", action="store_true", help="Show count but don't delete")
    args = parser.parse_args()

    try:
        cutoff_dt = datetime.strptime(args.cutoff, "%Y-%m-%d")
    except ValueError:
        print("Error: date must be YYYY-MM-DD")
        return 1

    # Interpret cutoff as HKT midnight -> UTC midnight (cutoff HKT - 8h)
    # This means rows with created_at_utc < (cutoff_date 00:00 HKT = cutoff_date-1 16:00 UTC)
    # For simplicity: use the UTC equivalent of cutoff 00:00 HKT
    cutoff_hkt = cutoff_dt.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc) + timedelta(hours=8)
    cutoff_utc = cutoff_hkt - timedelta(hours=8)
    cutoff_iso = cutoff_utc.isoformat()

    conn = sqlite3.connect(DB_PATH)

    deleted = delete_before(conn, cutoff_iso)

    if args.dry_run:
        print(f"[DRY RUN] Would delete {deleted} rows older than {args.cutoff} ({cutoff_iso} UTC)")
    else:
        print(f"Deleted {deleted} rows older than {args.cutoff}")

    if args.vacuum and not args.dry_run and deleted > 0:
        print("Running VACUUM...")
        conn.execute("VACUUM")
        print("Done.")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
