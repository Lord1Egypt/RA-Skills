"""Append-only audit log for IBKR-investing lifecycle events.

Layout: ~/.aeon/ibkr/audit.jsonl  — one JSON object per line.

Events emitted:
    proposal_created       — propose-trade pending file written
    proposal_cancelled     — user cancelled before executing
    proposal_executed      — trade placed via IBKR
    proposal_rejected      — IBKR refused the order
    daily_cap_breach       — guardrail prevented a trade at execute time
    drawdown_trigger       — dca_dip recommended a buy from the reserve
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.path.expanduser("~/.aeon/ibkr"))
AUDIT_LOG = ROOT / "audit.jsonl"


def append(event: str, **fields) -> None:
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
