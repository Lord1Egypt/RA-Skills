#!/usr/bin/env python3
"""mit.today_brief — print today's MIT for the cron-time prompt."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def main() -> int:
    today = date.today().isoformat()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT date, task, completed FROM mit_entries WHERE date = ?",
            (today,),
        ).fetchone()
    payload = {
        "date": today,
        "task": row["task"] if row else None,
        "completed": bool(row["completed"]) if row else None,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
