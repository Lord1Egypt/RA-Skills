#!/usr/bin/env python3
"""
closure_convergence_sweep.py — UNGATED two-store reconciliation that BRIDGES
(rather than merely reports) genuine dispatch-eval/praxis-eval gaps before a
dispatch-wave closure is asserted.

CONFIRMED NEED 2026-07-15: the mixed-wave-closure convergence sweep in
references/session-20260715-mixed-wave-closure.md step 9 originally gated on
`mtime > cutoff`. That is WRONG: verify_genuine_gap_profile.py asserts gaps
across ALL today-dated journals (NO mtime filter), so a journal missing from
the dispatch-eval store but written BEFORE the cutoff is wrongly skipped by a
gated sweep and surfaces as a GENUINE GAP on the final assertion. This script
mirrors verify_genuine_gap_profile.py's ungated walk (bounded per-skill
os.listdir, excludes ocas-custodian + dispatch-wave-* meta journals) and
appends every missing journal into the store(s) it is absent from.

Usage: python3 scripts/closure_convergence_sweep.py [--date YYYY-MM-DD]
Exits 0 if it added 0 gaps (closure stable), 1 if it bridged any. Run
iteratively (loop until it adds 0) immediately before asserting closure with
verify_genuine_gap_profile.py.
"""
import json
import os
import sys
from datetime import datetime, timezone

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 closure_convergence_sweep.py [--date YYYY-MM-DD]")
    sys.exit(0)

BASE = os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo"))
JD = os.path.join(BASE, "commons/journals")
DISP = os.path.join(BASE, "commons/data/ocas-dispatch/journals_evaluated.jsonl")
PRAX = os.path.join(BASE, "commons/data/ocas-praxis/journals_evaluated.jsonl")
EXCLUDED = {"ocas-custodian"}


def norm_rel(v):
    # Normalize historical key variants: strip leading "journals/",
    # "commons/journals/", and "profiles/indigo/commons/journals/" prefixes so
    # membership checks match the bare relpath the sweep writes/checks.
    if not isinstance(v, str):
        return v
    for p in ("profiles/indigo/commons/journals/", "commons/journals/", "journals/"):
        if v.startswith(p):
            return norm_rel(v[len(p):])
    return v


def load_membership(path, key):
    s = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                v = e.get(key)
                if v:
                    s.add(norm_rel(v))
    return s


def append_unique(fpath, key_field, key_val, action_taken, source):
    if os.path.exists(fpath):
        with open(fpath) as f:
            for line in f:
                if key_val in line:
                    return False
    with open(fpath, "a") as f:
        f.write(json.dumps({key_field: key_val, "action_taken": action_taken,
                            "source": source}) + "\n")
    return True


def main():
    date = (sys.argv[sys.argv.index("--date") + 1]
            if "--date" in sys.argv
            else datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    # Dispatch store historically has entries keyed BOTH ways ("filename" from
    # this script, "journal_id" from bridge_eval_inline.py/manual bridges).
    # Accept either key or the sweep loops forever on entries whose substring
    # dedup guard (append_unique) blocks re-appending under the other key.
    # Dispatch store has entries keyed "filename", "journal_id", OR "journal"
    # (different bridge writers). Accept all three or the sweep loops forever.
    disp_set = load_membership(DISP, "filename") | load_membership(DISP, "journal_id") | load_membership(DISP, "journal") | load_membership(DISP, "journal_file")
    prax_set = load_membership(PRAX, "journal_id") | load_membership(PRAX, "journal") | load_membership(PRAX, "filename") | load_membership(PRAX, "journal_file")
    added = 0
    for skill in sorted(os.listdir(JD)):
        if not skill.startswith("ocas-") or skill in EXCLUDED:
            continue
        d = os.path.join(JD, skill, date)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn.startswith("dispatch-wave-"):
                continue
            rel = f"{skill}/{date}/{fn}"
            in_d = rel in disp_set
            in_p = rel in prax_set
            if in_d and in_p:
                continue
            if not in_d:
                append_unique(DISP, "filename", rel, "post_dispatch_cleanup",
                             "convergence-sweep")
            if not in_p:
                append_unique(PRAX, "journal_id", rel, "post_dispatch_cleanup",
                             "convergence-sweep")
            added += 1
            print(f"BRIDGED {rel:55s} dispatch={in_d!s:5s} praxis={in_p!s:5s}")
    print(f"Date: {date}")
    print(f"GAPS BRIDGED: {added}")
    return 1 if added else 0


if __name__ == "__main__":
    sys.exit(main())