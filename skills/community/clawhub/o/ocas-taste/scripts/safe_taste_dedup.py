#!/usr/bin/env python3
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Styx-safe dispatch dedup; refuses to drop Styx-sourced signals.')
    print("Usage: safe_taste_dedup.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import os
"""Safe Taste signal dedup — preserves Styx signals (which use `date`, not `event_date`).

DISPATCH_TASTE_DEDUP.PY IS UNSAFE FOR STYX: it keys on event_date[:10]. Email/calendar
signals carry `event_date`; Styx signals (from the daily Styx delta) carry `date`. So every
Styx signal collapses to key (venue_name, None, 'styx') and ALL-BUT-ONE per venue is deleted.
Confirmed live 2026-07-22 (deleted 47 of 49 Styx signals) and reaffirmed 2026-07-23.

This script keys on (event_date or date)[:10] so Styx signals are deduped correctly per
(venue, day) and never collapsed. It backs up signals.jsonl before mutating and REFUSES to
write if the Styx count would drop.

Usage:
  python3 safe_taste_dedup.py [--dry-run]
"""
import json, sys, os, shutil, time
from collections import defaultdict

DATA = os.path.expanduser("~/.hermes/profiles/indigo/commons/data/ocas-taste")
SIGNALS = os.path.join(DATA, "signals.jsonl")


def date10(s):
    d = s.get("event_date") or s.get("date") or ""
    return d[:10] if d else ""


def keyfn(s):
    return (s.get("extraction_source", "?"), s.get("venue_name", ""), date10(s))


def main():
    dry = "--dry-run" in sys.argv
    with open(SIGNALS) as f:
        lines = [l for l in f if l.strip()]
    sigs = [json.loads(l) for l in lines]
    groups = defaultdict(list)
    for i, s in enumerate(sigs):
        groups[keyfn(s)].append(i)
    keep = set()
    removed = 0
    for idxs in groups.values():
        keep.add(idxs[0])
        removed += len(idxs) - 1
    out = [sigs[i] for i in sorted(keep)]
    styx_before = sum(1 for s in sigs if s.get("extraction_source") == "styx")
    styx_after = sum(1 for s in out if s.get("extraction_source") == "styx")
    print(f"BEFORE: {len(sigs)}  AFTER: {len(out)}  REMOVED: {removed}")
    print(f"STYX: before={styx_before} after={styx_after} {'OK' if styx_after == styx_before else 'CORRUPTED!'}")
    if styx_after != styx_before:
        print("ABORT: Styx signals would be lost. Refusing to write.", file=sys.stderr)
        sys.exit(2)
    if dry:
        print("DRY RUN — no write.")
        return
    bak = f"/tmp/signals.pre-safe-dedup.{time.strftime('%Y%m%dT%H%M%SZ')}.jsonl"
    shutil.copy(SIGNALS, bak)
    print("BACKUP:", bak)
    with open(SIGNALS, "w") as f:
        for s in out:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print("WROTE", SIGNALS)


if __name__ == "__main__":
    main()
