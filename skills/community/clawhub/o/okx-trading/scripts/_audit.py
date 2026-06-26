"""Append-only audit log for grid lifecycle events.

Layout: ~/.aeon/okx/grid_audit.jsonl  — one JSON object per line.

Events emitted by okx_grid_step.py:
    grid_applied          — grid orders placed (after YES)
    fill                  — a buy or sell limit filled
    restock               — opposite-side order placed after a fill
    cost_basis_protected  — sell skipped because price < avg_px * (1 + min_profit_gap)
    position_capped       — buy skipped because position >= max_position_base
    rescaled              — auto-rescale fired (range re-centered around current price)
    halted                — grid halted by guardrail breach

Reads cheap (`tail -n 50`); writes O(1). The file is intentionally
unbounded — disk pressure shows up as audit_growth in monitoring rather than
as silent rotation.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.path.expanduser("~/.aeon/okx"))
AUDIT_LOG = ROOT / "grid_audit.jsonl"


def append(event: str, **fields) -> None:
    """Append one audit entry. Never raises — audit failure must not abort a trade."""
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        record = {
            "ts_iso": datetime.now(timezone.utc).isoformat(),
            "ts_epoch": int(time.time()),
            "event": event,
            **fields,
        }
        with AUDIT_LOG.open("a") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception:
        pass


def tail(n: int = 50) -> list[dict]:
    """Return the last n audit entries (newest last). Cheap for typical sizes."""
    if not AUDIT_LOG.exists():
        return []
    lines = AUDIT_LOG.read_text().splitlines()[-n:]
    out: list[dict] = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out
