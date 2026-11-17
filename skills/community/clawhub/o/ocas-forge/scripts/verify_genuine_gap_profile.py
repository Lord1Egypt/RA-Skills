#!/usr/bin/env python3
"""
verify_genuine_gap_profile.py — bounded per-skill two-store reconciliation.

CONFIRMED NEEDED 2026-07-15: the ocas-forge SKILL.md closure recipes
reference `verify_genuine_gap_profile.py` and `reconcile_dispatch_eval_today.py`
as if they exist, but the dispatch-bridge-script-reality audit confirmed
NONE of those helpers are on disk. This is the working replacement: a
bounded per-skill `os.listdir` walk (NOT recursive glob/os.walk — those
descend into self-nested `journals/journals/...` symlinks and emit dozens
of false-positive "gap" hits).

WHAT IT DOES:
  For every skill in commons/journals/<skill>/<DATE>/, lists on-disk *.json
  journals (skipping dispatch-wave-* meta journals) and checks each against BOTH
  authoritative eval stores:
    commons/data/ocas-dispatch/journals_evaluated.jsonl  (key: "filename")
    commons/data/ocas-praxis/journals_evaluated.jsonl     (key: "journal_id")
  A journal is a GENUINE GAP if it is absent from EITHER store.

USAGE:
  python3 scripts/verify_genuine_gap_profile.py [--date YYYY-MM-DD] [--json]

Default date = UTC today. Prints per-journal membership and a final
GENUINE GAP count. Exit code 0 if gap==0 (safe to declare closure),
1 otherwise (closure NOT achieved — do not exit the dispatch wave).

NOTE: custodian self-bridged cron journals are a known ~15 residual set and
are excluded by design — they are NOT genuine dispatch gaps.
"""
import json
import os
import sys
from datetime import datetime, timezone

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 verify_genuine_gap_profile.py [--date YYYY-MM-DD] [--json]")
    sys.exit(0)

BASE = os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo"))
JD = os.path.join(BASE, "commons/journals")
DISP = os.path.join(BASE, "commons/data/ocas-dispatch/journals_evaluated.jsonl")
PRAX = os.path.join(BASE, "commons/data/ocas-praxis/journals_evaluated.jsonl")

# Skills that produce self-bridged cron journals we exclude from the genuine-gap
# assertion (custodian convergence loop). They are not dispatch gaps.
EXCLUDED_SKILLS = {"ocas-custodian"}


def norm_rel(v):
    # Normalize historical key variants: strip leading "journals/",
    # "commons/journals/", and "profiles/indigo/commons/journals/" prefixes so
    # membership checks match the bare relpath used by bridge writers.
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


def main():
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    as_json = "--json" in sys.argv

    # Accept any known key ("filename", "journal_id", "journal").
    disp_set = load_membership(DISP, "filename") | load_membership(DISP, "journal_id") | load_membership(DISP, "journal") | load_membership(DISP, "journal_file")
    prax_set = load_membership(PRAX, "journal_id") | load_membership(PRAX, "journal") | load_membership(PRAX, "filename") | load_membership(PRAX, "journal_file")

    gaps = []
    for skill in sorted(os.listdir(JD)):
        if not skill.startswith("ocas-"):
            continue
        if skill in EXCLUDED_SKILLS:
            continue
        d = os.path.join(JD, skill, date)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json"):
                continue
            if fn.startswith("dispatch-wave-"):
                continue  # meta journal, not a journal to evaluate
            rel = f"{skill}/{date}/{fn}"
            in_d = rel in disp_set
            in_p = rel in prax_set
            if in_d and in_p:
                continue
            gaps.append(rel)
            if not as_json:
                print(f"GAP  {rel:55s} dispatch={in_d!s:5s} praxis={in_p!s:5s}")

    if as_json:
        print(json.dumps({"date": date, "genuine_gap": len(gaps), "gaps": gaps}))
    else:
        print()
        print(f"Date: {date}")
        print(f"GENUINE GAP (excluding custodian): {len(gaps)}")
    return 0 if len(gaps) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())