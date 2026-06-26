#!/usr/bin/env python3
"""mit.log — upsert today's or tomorrow's MIT."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def _bool(v: str) -> int:
    return 1 if str(v).lower() in {"1", "true", "yes", "y", "t"} else 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--upsert", action="store_true", required=True)
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--task", required=True)
    p.add_argument("--completed", default="false")
    args = p.parse_args()

    completed = _bool(args.completed)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO mit_entries (date, task, completed) VALUES (?, ?, ?) "
            "ON CONFLICT(date) DO UPDATE SET task=excluded.task, "
            "  completed=excluded.completed, updated_at=datetime('now')",
            (args.date, args.task, completed),
        )
        conn.commit()
    print(json.dumps({"ok": True, "date": args.date, "task": args.task,
                      "completed": bool(completed)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
