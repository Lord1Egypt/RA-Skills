#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reactivate stale tasks from the task ledger.

- Only auto-reactivate tasks with auto=true
- Blocks external actions (URLs, openclaw message send)
- Auto status transition after execution:
  - repeatable=false: rc=0 -> done, rc!=0 -> blocked
  - repeatable=true: keep doing
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from task_ledger import derive_state, load_events, append_event, now_ts


BLOCK_EXTERNAL_TOKENS = [
    "openclaw message send",
    "--channel feishu",
    "--channel webchat",
    "http://",
    "https://",
]


def parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(ts, fmt)
        except Exception:
            pass
    return None


def is_external_action(cmd: str) -> bool:
    c = (cmd or "").lower()
    return any(tok in c for tok in [t.lower() for t in BLOCK_EXTERNAL_TOKENS])


def run_local(next_cmd: str, timeout_s: int = 180) -> Tuple[int, str]:
    parts = shlex.split(next_cmd)
    if not parts:
        return 2, "empty next"
    try:
        res = subprocess.run(parts, cwd=str(Path.cwd()), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout_s)
        out = (res.stdout or "").strip()
        err = (res.stderr or "").strip()
        msg = out if out else err
        return res.returncode, msg[:4000]
    except Exception as e:
        return 1, str(e)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stale-min", type=int, default=5)
    ap.add_argument("--max", type=int, default=2)
    args = ap.parse_args()

    tasks = derive_state(load_events())
    now = datetime.now()

    stale: List[Dict[str, Any]] = []
    for t in tasks.values():
        if t.get("status") not in ("doing", "blocked"):
            continue
        if not t.get("auto"):
            continue
        lt = parse_ts(t.get("last_touch")) or parse_ts(t.get("updated_at"))
        if not lt:
            continue
        mins = (now - lt).total_seconds() / 60.0
        if mins >= args.stale_min:
            stale.append({"task": t, "stale_min": mins})

    stale.sort(key=lambda x: x["stale_min"], reverse=True)

    acted = 0
    for item in stale[: args.max]:
        t = item["task"]
        next_cmd = t.get("next") or ""
        if not next_cmd:
            continue
        if is_external_action(next_cmd):
            append_event({"ts": now_ts(), "event": "touch", "id": t["id"], "notes": "reactivate_skipped: external action"})
            continue

        append_event({"ts": now_ts(), "event": "touch", "id": t["id"], "notes": f"reactivate: running `{next_cmd}`"})
        rc, msg = run_local(next_cmd)
        append_event({"ts": now_ts(), "event": "touch", "id": t["id"], "notes": f"reactivate_result rc={rc} msg={msg}"})

        repeatable = bool(t.get("repeatable"))
        if not repeatable:
            if rc == 0:
                append_event({"ts": now_ts(), "event": "update", "id": t["id"], "status": "done", "notes": "auto_done: reactivate rc=0"})
            else:
                append_event({"ts": now_ts(), "event": "update", "id": t["id"], "status": "blocked", "notes": f"auto_blocked: reactivate rc={rc} msg={msg[:200]}"})
        else:
            append_event({"ts": now_ts(), "event": "touch", "id": t["id"], "notes": "repeatable: keep doing"})

        acted += 1

    print(f"OK reactivated={acted} candidates={len(stale)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
