#!/usr/bin/env python3
"""Populate a demo data.db with realistic mood/reminder/mit/diary-cache entries.

Usage:
    GLANCE_HOME=$PWD/examples/demo-data python3 examples/demo-data/seed.py

After running, build the dashboard against the same GLANCE_HOME to see
all panels populated without needing a real Google OAuth client. The diary panel
will still show "error" — diary_logger needs Calendar — that's expected.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import apply_all_migrations, get_connection
from glancely.core.storage.db import get_db_path

SKILLS_ROOT = REPO_ROOT  # now inside glancely/examples/


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def seed() -> None:
    apply_all_migrations(SKILLS_ROOT)
    now = datetime.now()
    with get_connection() as conn:
        conn.execute("DELETE FROM mood_entries")
        for delta_h, score, label, raw in [
            (0.5, 8, "happy", "feeling great after the morning run"),
            (3, 7, "focused", "deep work on the auth module"),
            (5, 6, "tired", "sluggish after lunch"),
            (8, 7, "calm", "wrapped up the day, relaxed"),
            (26, 5, "stressed", "deadline pressure building"),
            (50, 8, "happy", "good chat with friends"),
        ]:
            ts = now - timedelta(hours=delta_h)
            conn.execute(
                "INSERT INTO mood_entries (created_at, mood_score, mood_label, note, raw_text) "
                "VALUES (?, ?, ?, ?, ?)",
                (_iso(ts), score, label, raw, raw),
            )

        conn.execute("DELETE FROM reminders")
        for title, due, status, days_ago_done in [
            ("renew passport", "2026-06-01", "active", None),
            ("call dentist", "2026-05-10", "active", None),
            ("file Q2 expenses", "2026-05-05", "active", None),
            ("backup laptop", None, "active", None),
            ("water plants", "2026-04-30", "done", 2),
            ("submit conf abstract", "2026-04-25", "done", 5),
        ]:
            completed_at = _iso(now - timedelta(days=days_ago_done)) if days_ago_done else None
            conn.execute(
                "INSERT INTO reminders (title, due_date, status, completed_at) "
                "VALUES (?, ?, ?, ?)",
                (title, due, status, completed_at),
            )

        conn.execute("DELETE FROM mit_entries")
        today = now.date()
        for delta_days, task, completed in [
            (0, "ship public repo v0.1", 0),
            (-1, "write component contract", 1),
            (-2, "draft scaffolder", 1),
            (-3, "test migrations", 1),
            (-4, "design dashboard", 0),
            (-5, "decide auth model", 1),
        ]:
            d = (today + timedelta(days=delta_days)).isoformat()
            conn.execute(
                "INSERT INTO mit_entries (date, task, completed) VALUES (?, ?, ?)",
                (d, task, completed),
            )

        conn.commit()
    print(f"Seeded demo data into {get_db_path()}")


if __name__ == "__main__":
    seed()
