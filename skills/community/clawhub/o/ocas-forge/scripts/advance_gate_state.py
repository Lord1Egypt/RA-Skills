#!/usr/bin/env python3
"""advance_gate_state.py — advance dispatch monitor + praxis ingest gate state.

Used during mixed-wave / re-detection closure when NO pipeline run advanced the
gate state. The dispatcher's monitor re-fire gate is SEPARATE from the eval-store
gap closure, so after `closure_closeout_check.py` reports gate [2] False you must
advance it yourself or the wave re-fires every ~5 min.

What it does:
  - Recomputes max journal mtime over a BOUNDED per-skill walk (never `**`
    recursive glob — the journals tree has a symlink loop that nests infinitely).
  - Writes BOTH monitor copies: journal_ingest_state.json  latest_mtime = max_mt + PAD
  - Writes praxis ingest_state.json: last_ingest_run = ISO(max_mt + PAD)
PAD = +5s to cover any heartbeat that lands during the write.

NEVER hand-type the mtime literal — truncation silently leaves state < max and
re-fires the wave forever. Recompute programmatically and write via json.load+dump.

Usage: python3 scripts/advance_gate_state.py --date 2026-07-22
"""
import argparse
import json
import os
import datetime

HERMES_ROOT = os.path.expanduser("~/.hermes")
PROFILE_ROOT = os.path.expanduser("~/.hermes/profiles/indigo")
PAD = 5.0


def collect_mtimes(date):
    roots = [
        os.path.join(HERMES_ROOT, "commons", "journals"),
        os.path.join(PROFILE_ROOT, "commons", "journals"),
    ]
    mtimes = []
    for base in roots:
        if not os.path.isdir(base):
            continue
        for skill in os.listdir(base):
            d = os.path.join(base, skill, date)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                if fn.endswith(".json"):
                    p = os.path.join(d, fn)
                    try:
                        mtimes.append(os.path.getmtime(p))
                    except OSError:
                        pass
    return mtimes


def advance_json(path, key, value):
    if not os.path.exists(path):
        print(f"  WARN skip (missing): {path}")
        return
    with open(path) as f:
        d = json.load(f)
    d[key] = value
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
    print(f"  wrote {path}: {key}={value}")


def main():
    ap = argparse.ArgumentParser(description="Advance dispatch closure gate state.")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()

    mtimes = collect_mtimes(args.date)
    if not mtimes:
        print(f"ERROR: no journals found for {args.date}")
        return 1
    max_mt = max(mtimes)
    new_float = max_mt + PAD
    new_iso = (datetime.datetime.fromtimestamp(max_mt, datetime.timezone.utc)
               + datetime.timedelta(seconds=PAD)).isoformat()
    print(f"max journal mtime: {max_mt:.6f} -> advanced: {new_float:.6f} ({new_iso})")

    monitor_copies = [
        os.path.join(HERMES_ROOT, "commons", "data", "monitor_state", "journal_ingest_state.json"),
        os.path.join(PROFILE_ROOT, "commons", "data", "monitor_state", "journal_ingest_state.json"),
    ]
    praxis_ingest = os.path.join(PROFILE_ROOT, "commons", "data", "ocas-praxis", "ingest_state.json")

    for path in monitor_copies:
        advance_json(path, "latest_mtime", new_float)
    advance_json(praxis_ingest, "last_ingest_run", new_iso)
    print("DONE. Re-run closure_closeout_check.py and require '=== gates ALL CLOSED ==='.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
