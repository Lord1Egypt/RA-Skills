#!/usr/bin/env python3
"""mood.stats — dashboard payload."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def build_stats() -> dict:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) c FROM mood_entries").fetchone()["c"]
        today = conn.execute(
            "SELECT COUNT(*) c FROM mood_entries WHERE date(created_at) = date('now', 'localtime')"
        ).fetchone()["c"]
        avg7 = conn.execute(
            "SELECT AVG(mood_score) a FROM mood_entries "
            "WHERE mood_score IS NOT NULL AND created_at >= datetime('now', '-7 days')"
        ).fetchone()["a"]
        last_row = conn.execute(
            "SELECT created_at, mood_label, note FROM mood_entries ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        rows = [
            dict(r) for r in conn.execute(
                "SELECT created_at, mood_score, mood_label, note FROM mood_entries "
                "ORDER BY created_at DESC LIMIT 10"
            ).fetchall()
        ]

    if total == 0:
        return {"freshness_hours": None, "status": "empty",
                "summary": {"total": 0, "today": 0}, "rows": []}

    freshness_hours = None
    if last_row:
        last_dt = datetime.fromisoformat(last_row["created_at"])
        freshness_hours = round((datetime.utcnow() - last_dt).total_seconds() / 3600.0, 2)

    return {
        "freshness_hours": freshness_hours,
        "status": "ok",
        "summary": {
            "total": total,
            "today": today,
            "avg_score_7d": round(avg7, 2) if avg7 is not None else None,
            "last_label": last_row["mood_label"] if last_row else None,
        },
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    print(json.dumps(build_stats(), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
