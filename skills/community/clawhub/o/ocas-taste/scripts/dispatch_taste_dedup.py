#!/usr/bin/env python3
"""
Dispatch-wave dedup script for ocas-taste.

Removes duplicate signals that arise when multiple dispatch waves re-scan the
same time window. Uses a broader key than taste_signals_dedup.py:
  (venue_name, event_date[:10], extraction_source)

Usage:
  cd <hermes-home>/profiles/<profile>/commons/data/ocas-taste && /usr/bin/python3 scripts/dispatch_taste_dedup.py

Or with dry-run:
  /usr/bin/python3 scripts/dispatch_taste_dedup.py --dry-run
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Dispatch-wave dedup keyed on (venue_name, event_date, extraction_source).')
    print("Usage: dispatch_taste_dedup.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)

import json
import os
import sys
from pathlib import Path

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 dispatch_taste_dedup.py")
    sys.exit(0)


DATA_DIR = Path(os.environ.get("AGENT_ROOT", os.environ.get("AGENT_ROOT", os.path.join(os.path.expanduser("~"), ".hermes")))).joinpath("profiles/indigo/commons/data/ocas-taste")
SIGNALS_FILE = DATA_DIR / "signals.jsonl"

DRY_RUN = "--dry-run" in sys.argv


def main():
    if not SIGNALS_FILE.exists():
        print(f"ERROR: {SIGNALS_FILE} not found")
        sys.exit(1)

    signals = []
    with open(SIGNALS_FILE) as f:
        for line in f:
            if line.strip():
                signals.append(json.loads(line))

    total_before = len(signals)

    # Dedup key: venue + date + source (broad enough to catch dispatch-wave re-scans)
    seen = set()
    deduped = []
    removed = 0

    for s in signals:
        key = (
            s.get("venue_name", ""),
            s.get("event_date", "")[:10],
            s.get("extraction_source", ""),
        )
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        deduped.append(s)

    total_after = len(deduped)

    print(f"Total signals: {total_before}")
    print(f"Duplicates removed: {removed}")
    print(f"Signals after dedup: {total_after}")

    if DRY_RUN:
        print("(dry-run — no changes written)")
        sys.exit(0)

    with open(SIGNALS_FILE, "w") as f:
        for s in deduped:
            f.write(json.dumps(s) + "\n")

    print("Written.")


if __name__ == "__main__":
    main()