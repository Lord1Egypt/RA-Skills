#!/usr/bin/env python3
"""
Journal a trade decision to trades.json.
Input (stdin JSON): trade journal entry dict.
Adds timestamp if missing and outputs the entry.

usage: echo '{"symbol":"BTCUSDT",...}' | journal_trade.py [trades.json]
If trades.json is given, appends to it; otherwise just echoes the entry.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    entry = json.load(sys.stdin)
    entry.setdefault("ts", datetime.now(timezone.utc).isoformat())

    if len(sys.argv) >= 2:
        path = Path(sys.argv[1])
        trades = []
        if path.exists():
            try:
                trades = json.loads(path.read_text())
            except Exception:
                trades = []
        trades.append(entry)
        path.write_text(json.dumps(trades, indent=2))

    print(json.dumps(entry, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
