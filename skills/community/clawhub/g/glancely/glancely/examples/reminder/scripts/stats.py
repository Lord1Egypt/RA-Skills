#!/usr/bin/env python3
"""reminder.stats — dashboard payload."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def build_stats() -> dict:
    with get_connection() as conn:
        active = conn.execute("SELECT COUNT(*) c FROM reminders WHERE status='active'").fetchone()["c"]
        overdue = conn.execute(
            "SELECT COUNT(*) c FROM reminders WHERE status='active' "
            "AND due_date IS NOT NULL AND due_date < date('now', 'localtime')"
        ).fetchone()["c"]
        completed_7d = conn.execute(
            "SELECT COUNT(*) c FROM reminders WHERE status='done' "
            "AND completed_at >= datetime('now','-7 days')"
        ).fetchone()["c"]
        rows = [dict(r) for r in conn.execute(
            "SELECT id, title, due_date, status FROM reminders WHERE status='active' "
            "ORDER BY COALESCE(due_date,'9999-99-99'), id LIMIT 10"
        ).fetchall()]

    if active == 0 and completed_7d == 0:
        return {"freshness_hours": None, "status": "empty",
                "summary": {"active": 0, "overdue": 0, "completed_7d": 0}, "rows": []}

    return {
        "freshness_hours": 0,
        "status": "ok",
        "summary": {"active": active, "overdue": overdue, "completed_7d": completed_7d},
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    print(json.dumps(build_stats(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
