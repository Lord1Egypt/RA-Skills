#!/usr/bin/env python3
"""verify_eval_no_phantoms.py — detect (and optionally remove) eval-file entries
whose journal_id points to a file that does NOT exist on disk.

Phantom entries arise when a bridge step recomposes a `datetime.now()` timestamp
for a journal a PRIOR step already wrote (e.g. forge-scan-235217Z registered but
the real file is forge-scan-235144Z). They pollute the eval store and can mask
real gaps on the next dispatcher scan.

Usage:
    python3 verify_eval_no_phantoms.py            # report only (exit 1 if phantoms)
    python3 verify_eval_no_phantoms.py --fix      # remove phantom lines in place

Cron-safe: no shell pipes, no execute_code. Pure in-process file IO.
"""
import json
import os
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 verify_eval_no_phantoms.py [--fix]")
    sys.exit(0)

PROF = "<hermes-home>/profiles/indigo"
JDIR = os.path.join(PROF, "commons", "journals")
EVAL_FILES = [
    os.path.join(PROF, "commons/data/ocas-praxis/journals_evaluated.jsonl"),
    os.path.join(PROF, "commons/data/ocas-dispatch/journals_evaluated.jsonl"),
]


def line_is_phantom(line):
    line = line.strip()
    if not line:
        return False, None
    try:
        rec = json.loads(line)
    except json.JSONDecodeError:
        return False, None
    jid = rec.get("journal_id") or rec.get("journal_file") or ""
    if not jid:
        return False, jid
    fp = os.path.join(JDIR, jid)
    return (not os.path.exists(fp)), jid


def main():
    fix = "--fix" in sys.argv
    total_phantom = 0
    for evf in EVAL_FILES:
        if not os.path.exists(evf):
            print(f"[skip] missing {evf}")
            continue
        with open(evf) as f:
            lines = f.readlines()
        kept = []
        phantoms = []
        for ln in lines:
            is_ph, jid = line_is_phantom(ln)
            if is_ph:
                phantoms.append((ln.rstrip("\n"), jid))
            else:
                kept.append(ln)
        total_phantom += len(phantoms)
        if phantoms:
            print(f"[PHANTOM] {evf}: {len(phantoms)} phantom entr(y/ies)")
            for ln, jid in phantoms:
                print(f"    missing on disk: {jid}")
            if fix:
                with open(evf, "w") as f:
                    f.writelines(kept)
                print(f"    removed {len(phantoms)} phantom line(s)")
        else:
            print(f"[clean]  {evf}: no phantoms ({len(lines)} lines)")
    if total_phantom and not fix:
        print(f"\n{total_phantom} phantom entr(y/ies) found. Re-run with --fix to remove.")
        sys.exit(1)
    print("\nDone.")


if __name__ == "__main__":
    main()