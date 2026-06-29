#!/usr/bin/env python3
"""
mark_seen.py
Marks all jobs in data/raw_jobs.json as seen in data/seen_jobs.db
so they don't appear in future runs.
Called by the agent after it has output the results in chat.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR   = Path(__file__).parent.parent
INPUT_PATH = BASE_DIR / "data" / "raw_jobs.json"
DB_PATH    = BASE_DIR / "data" / "seen_jobs.db"

def main():
    if not INPUT_PATH.exists():
        print("No raw_jobs.json found — nothing to mark.")
        return

    with open(INPUT_PATH, encoding="utf-8") as f:
        jobs = json.load(f)

    if not jobs:
        print("No jobs to mark.")
        return

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            job_id TEXT PRIMARY KEY,
            seen_at TEXT
        )
    """)

    count = 0
    for job in jobs:
        if job.get("id"):
            conn.execute(
                "INSERT OR IGNORE INTO seen_jobs (job_id, seen_at) VALUES (?, ?)",
                (job["id"], datetime.utcnow().isoformat())
            )
            count += 1

    conn.commit()
    conn.close()
    print(f"Marked {count} jobs as seen.")

if __name__ == "__main__":
    main()
