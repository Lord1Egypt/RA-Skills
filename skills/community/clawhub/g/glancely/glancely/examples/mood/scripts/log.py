#!/usr/bin/env python3
"""mood.log — write a mood entry."""

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
    p.add_argument("--raw", required=True, help="The user's full reply")
    p.add_argument("--score", type=int, help="Optional 1-10 mood score")
    p.add_argument("--label", help="Optional mood label (happy, tired, ...)")
    p.add_argument("--note", help="Optional curated note (defaults to --raw)")
    args = p.parse_args()

    note = args.note if args.note is not None else args.raw
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO mood_entries (mood_score, mood_label, note, raw_text) "
            "VALUES (?, ?, ?, ?)",
            (args.score, args.label, note, args.raw),
        )
        conn.commit()
        rid = cur.lastrowid

    print(json.dumps({"ok": True, "id": rid}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
