#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compact task ledger to keep it small.

Policy:
- Keep all unfinished tasks' events
- Keep done tasks events only for today (default), and archive snapshot for older

Archives to: memory/tasks/archive/tasks_YYYY-MM-DD.json

Note: This is optional; you can disable the cron job.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from _config import load_config
from task_ledger import load_events, derive_state


def main() -> int:
    cfg = load_config()
    mem = Path(cfg["memory_dir"]) / "tasks"
    ledger = mem / "active_tasks.jsonl"
    if not ledger.exists():
        print("NO_LEDGER")
        return 0

    events = load_events()
    state = derive_state(events)

    today = datetime.now().strftime("%Y-%m-%d")

    # archive snapshot
    arch_dir = mem / "archive"
    arch_dir.mkdir(parents=True, exist_ok=True)
    snap_path = arch_dir / f"tasks_{today}.json"
    snap_path.write_text(json.dumps(list(state.values()), ensure_ascii=False, indent=2), encoding="utf-8")

    # keep rules
    keep_ids = set()
    for t in state.values():
        st = t.get("status")
        if st in ("todo", "doing", "blocked"):
            keep_ids.add(t["id"])
        elif st == "done":
            if (t.get("updated_at") or "").startswith(today):
                keep_ids.add(t["id"])

    kept = []
    for ev in events:
        if ev.get("id") in keep_ids:
            kept.append(ev)

    tmp = ledger.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for ev in kept:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    tmp.replace(ledger)

    print(f"OK compact kept_events={len(kept)} tasks={len(keep_ids)} archive={snap_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
