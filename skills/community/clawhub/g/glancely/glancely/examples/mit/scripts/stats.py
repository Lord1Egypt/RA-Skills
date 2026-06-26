#!/usr/bin/env python3
"""mit.stats — dashboard payload."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def build_stats() -> dict:
    today = date.today().isoformat()
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) c FROM mit_entries").fetchone()["c"]
        if total == 0:
            return {"freshness_hours": None, "status": "empty",
                    "summary": {"total": 0}, "rows": []}
        today_row = conn.execute(
            "SELECT date, task, completed FROM mit_entries WHERE date = ?", (today,)
        ).fetchone()
        last90 = list(conn.execute(
            "SELECT date, task, completed FROM mit_entries "
            "WHERE date >= date('now','-90 days') ORDER BY date DESC"
        ))
        completed_7d = sum(1 for r in last90[:7] if r["completed"])
        recent = [dict(r) for r in last90[:10]]

    last_dt = datetime.fromisoformat(last90[0]["date"]) if last90 else None
    freshness_hours = (
        round((datetime.utcnow() - last_dt).total_seconds() / 3600.0, 2)
        if last_dt else None
    )

    return {
        "freshness_hours": freshness_hours,
        "status": "ok",
        "summary": {
            "today_task": today_row["task"] if today_row else None,
            "today_completed": bool(today_row["completed"]) if today_row else None,
            "completed_last_7d": completed_7d,
            "logged_last_7d": len(last90),
            "completion_rate_7d": round(completed_7d / len(last90[:7]) * 100, 1) if last90 else 0,
        },
        "rows": recent,
    }


def main(argv: list[str] | None = None) -> int:
    print(json.dumps(build_stats(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
