#!/usr/bin/env python3
"""reminder.digest — markdown digest of active reminders for cron prompts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def render_markdown(limit: int = 20, header: str | None = None) -> str:
    with get_connection() as conn:
        rows = list(conn.execute(
            "SELECT id, title, due_date FROM reminders WHERE status='active' "
            "ORDER BY COALESCE(due_date, '9999-99-99'), id LIMIT ?",
            (limit,),
        ))
    if not rows:
        return "今天没有未完成提醒。"
    lines = [header or "**Active reminders:**"]
    for r in rows:
        due = f" — due {r['due_date']}" if r["due_date"] else ""
        lines.append(f"- [#{r['id']}] {r['title']}{due}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--header")
    args = p.parse_args()
    print(render_markdown(args.limit, args.header))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
