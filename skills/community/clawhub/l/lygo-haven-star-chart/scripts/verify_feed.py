#!/usr/bin/env python3
"""Verify immutable feed chain in-process (no subprocess)."""

from __future__ import annotations

import json
import sys

from _stack_paths import resolve_stack_root
from _stack_tools import load_tool


def main() -> int:
    stack = resolve_stack_root()
    feed_mod = load_tool(stack, "haven_star_chart_feed.py")
    rows = feed_mod.read_ledger()
    ok, errs = feed_mod.verify_chain(rows)
    print(json.dumps({"chain_valid": ok, "entries": len(rows), "errors": errs}, indent=2))
    if not ok:
        return 1
    feed_path = stack / "docs" / "haven_star_chart" / "haven_star_chart_feed.json"
    if feed_path.is_file():
        feed = json.loads(feed_path.read_text(encoding="utf-8"))
        for row in (feed.get("entries") or [])[:5]:
            print(
                json.dumps(
                    {
                        "seq": row.get("seq"),
                        "status": row.get("status"),
                        "agent_id": row.get("agent_id"),
                        "node_id": row.get("node_id"),
                        "entry_hash": (row.get("entry_hash") or "")[:16],
                    }
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())