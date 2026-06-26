#!/usr/bin/env python3
"""reminder.log — add, complete, list reminders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.storage import get_connection


def main() -> int:
    p = argparse.ArgumentParser()
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--add", action="store_true")
    grp.add_argument("--done", action="store_true")
    grp.add_argument("--cancel", action="store_true")
    grp.add_argument("--list", action="store_true")
    p.add_argument("--title")
    p.add_argument("--due", help="YYYY-MM-DD")
    p.add_argument("--notes")
    p.add_argument("--id", type=int)
    p.add_argument("--limit", type=int, default=50)
    args = p.parse_args()

    with get_connection() as conn:
        if args.add:
            if not args.title:
                p.error("--add requires --title")
            cur = conn.execute(
                "INSERT INTO reminders (title, due_date, notes) VALUES (?, ?, ?)",
                (args.title, args.due, args.notes),
            )
            conn.commit()
            print(json.dumps({"ok": True, "id": cur.lastrowid}, ensure_ascii=False))
            return 0
        if args.done or args.cancel:
            if not args.id:
                p.error("requires --id")
            new_status = "done" if args.done else "cancelled"
            conn.execute(
                "UPDATE reminders SET status = ?, completed_at = datetime('now') WHERE id = ?",
                (new_status, args.id),
            )
            conn.commit()
            print(json.dumps({"ok": True, "id": args.id, "status": new_status}, ensure_ascii=False))
            return 0
        if args.list:
            rows = [dict(r) for r in conn.execute(
                "SELECT id, title, due_date, status, notes FROM reminders "
                "WHERE status = 'active' ORDER BY COALESCE(due_date, '9999-99-99'), id LIMIT ?",
                (args.limit,),
            ).fetchall()]
            print(json.dumps({"ok": True, "reminders": rows}, indent=2, ensure_ascii=False))
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
