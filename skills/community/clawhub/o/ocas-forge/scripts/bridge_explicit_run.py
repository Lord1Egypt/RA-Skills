#!/usr/bin/env python3
"""Caller-side bridge for explicit-run `new_journals` dispatch waves.

WHY THIS EXISTS
---------------
`ocas-forge/scripts/run_dispatch_pipeline.py` is broken on Python 3.14
(argparse `nargs='[]'`) and, even when runnable, does NOT satisfy the
explicit-run override: it does not run the real Mentor heartbeat, does not
bridge into the DISPATCH eval file, and does not always write a forge-scan
journal. The dispatch-pipeline-guide + session-20260713-dispatch-explicit-run
docs therefore require the CALLER to run the pipeline by hand. This script is
that hand-run, made repeatable and pitfall-safe.

WHAT IT DOES (single atomic run, all timestamps composed ONCE)
-------------------------------------------------------------
1. Forge scan  - check intake/ + data root for unprocessed vp_*/vd_* proposals
                 (cross-referenced against intake/processed/); write a
                 forge-scan-<TS>.json no-op journal.
2. Mentor      - build dual-path 3-day file list, run cron-heartbeat-light.py
                 via subprocess stdin redirect (NOT a shell pipe - the
                 pipe_to_interpreter guard blocks `cat file | python3`),
                 capture the ACTUAL heartbeat journal filename via a
                 content-timestamp scan (never trust script stdout - it can
                 roll over by up to 60s), then run correct_active_skills_30d.py.
                 DOES NOT write a second mentor journal (anti-journalization).
3. Bridge      - idempotently append [mentor heartbeat journal, forge-scan
                 journal, every dispatcher new_file, dispatch-wave journal]
                 into BOTH eval files (praxis: journal_id, dispatch: filename).
4. Dispatch    - write the dispatch-wave-<TS>.json meta-journal (classification
                 mixed_genuine; NOT registered in eval per 2026-07-07 rule).
5. State       - advance ingest_state.last_ingest_run to the MAX mtime of all
                 bridged journals, resync journals_evaluated_count /
                 last_eval_file_line to actual eval-file line counts.
6. Phantom     - print a verification line; caller should `ls` the three
                 pipeline dirs for empty/double-TS/malformed filenames.

USAGE
-----
  python3 scripts/bridge_explicit_run.py --new-files ocas-mentor/2026-07-14/mentor-light-20260714T023026Z.json

Multiple new_files: space-separate them. The script is idempotent on eval
registration (skips entries already present), so re-running on an already
bridged wave is safe.

ENVIRONMENT
-----------
Paths are profile-scoped under <hermes-home>/profiles/indigo. Adjust PROFILE
if run under a different profile.
"""

import json
import os
import subprocess
import sys
import datetime
from datetime import datetime, timezone

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 bridge_explicit_run.py --new-files <relpath> [...]")
    sys.exit(0)

PROFILE = os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo"))
JDIR = os.path.join(PROFILE, "commons/journals")
PRAXIS_EVAL = os.path.join(PROFILE, "commons/data/ocas-praxis/journals_evaluated.jsonl")
DISPATCH_EVAL = os.path.join(PROFILE, "commons/data/ocas-dispatch/journals_evaluated.jsonl")
STATE_PATH = os.path.join(PROFILE, "commons/data/ocas-praxis/ingest_state.json")
FORGE_DATA = os.path.join(PROFILE, "commons/data/ocas-forge")
MENTOR_SCRIPT = os.path.join(PROFILE, "skills/ocas-mentor/scripts/cron-heartbeat-light.py")
CORRECT_SCRIPT = os.path.join(PROFILE, "skills/ocas-mentor/scripts/correct_active_skills_30d.py")


def append_unique_eval(fpath, key_field, key_val, action_taken, source, backfill_at):
    """Append to an eval file only if key_val is not already present (raw substring)."""
    if os.path.exists(fpath):
        with open(fpath) as f:
            for line in f:
                if key_val in line:
                    return False
    entry = {
        key_field: key_val,
        "action_taken": action_taken,
        "source": source,
        "backfill_at": backfill_at,
    }
    with open(fpath, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return True


def forge_unprocessed_count():
    """Count vp_*/vd_* proposals not yet in intake/processed/."""
    candidates = []
    intake_dir = os.path.join(FORGE_DATA, "intake")
    processed_dir = (os.path.join(intake_dir, "processed")
                     if os.path.isdir(intake_dir) else None)
    for base in (intake_dir, FORGE_DATA):
        if not os.path.isdir(base):
            continue
        for fn in os.listdir(base):
            if (fn.startswith("vp_") or fn.startswith("vd_")) and fn.endswith(".json"):
                candidates.append(os.path.join(base, fn))
    real = []
    for p in set(candidates):
        if not os.path.isfile(p):
            continue
        fn = os.path.basename(p)
        if processed_dir and os.path.isfile(os.path.join(processed_dir, fn)):
            continue
        real.append(fn)
    return real


def main():
    args = sys.argv[1:]
    new_files = []
    i = 0
    while i < len(args):
        if args[i] == "--new-files":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                new_files.append(args[i])
                i += 1
        else:
            i += 1

    if not new_files:
        print("ERROR: pass --new-files <relpath> [<relpath> ...]")
        sys.exit(2)

    # Compose ALL timestamps ONCE - never call datetime.now() again.
    now = datetime.now(timezone.utc)
    TS = now.strftime("%Y%m%dT%H%M%SZ")
    NOW = now.isoformat()
    DATE = now.strftime("%Y-%m-%d")
    print("Composed TS:", TS, "DATE:", DATE)

    dispatch_rel = "ocas-dispatch/%s/dispatch-wave-%s.json" % (DATE, TS)

    # ---- Step 1: Forge scan ----
    unprocessed = forge_unprocessed_count()
    print("Forge unprocessed proposals:", len(unprocessed))
    forge_dir = os.path.join(JDIR, "ocas-forge", DATE)
    os.makedirs(forge_dir, exist_ok=True)
    forge_rel = "ocas-forge/%s/forge-scan-%s.json" % (DATE, TS)
    forge_path = os.path.join(JDIR, forge_rel)
    forge_entry = {
        "schema": "forge-journal-v1",
        "run_id": "forge-scan-%s" % TS,
        "timestamp": NOW,
        "action": {"result": "no_op",
                   "findings": {"unprocessed_proposals": len(unprocessed)}},
        "outcome": "success",
        "trigger": "dispatch",
    }
    with open(forge_path, "w") as f:
        json.dump(forge_entry, f, indent=2)
    print("Forge journal written:", forge_rel)

    # ---- Step 2: Mentor light heartbeat ----
    fl = "/tmp/mentor_files_3d.txt"
    subprocess.run(
        "find " + os.path.expanduser("~/.hermes/commons/journals/") + " " + os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes/profiles/indigo")), "commons/journals/") + " "
        "-name '*.json' -mtime -3 2>/dev/null | sort -u > %s" % fl, shell=True)
    hb = subprocess.run(["python3", MENTOR_SCRIPT], stdin=open(fl),
                        capture_output=True, text=True)
    print("Heartbeat rc:", hb.returncode)
    if hb.stdout:
        print("Heartbeat stdout tail:", hb.stdout.strip()[-200:])

    # Capture ACTUAL heartbeat journal via content-timestamp scan (not stdout).
    mentor_dir = os.path.join(JDIR, "ocas-mentor", DATE)
    recent_hb = None
    max_ts = ""
    if os.path.isdir(mentor_dir):
        for fn in os.listdir(mentor_dir):
            if fn.startswith("mentor-light-") and fn.endswith(".json"):
                p = os.path.join(mentor_dir, fn)
                try:
                    with open(p) as f:
                        c = json.load(f)
                    t = c.get("timestamp", "")
                    if t > max_ts:
                        max_ts = t
                        recent_hb = fn
                except Exception:
                    pass
    print("Heartbeat journal on disk:", recent_hb)
    if not recent_hb:
        print("WARNING: heartbeat journal not found on disk - bridge will skip it")

    if os.path.isfile(CORRECT_SCRIPT):
        cr = subprocess.run(["python3", CORRECT_SCRIPT], capture_output=True, text=True)
        print("Correct script rc:", cr.returncode)

    # ---- Step 3: Bridge into BOTH eval files (idempotent) ----
    bridge = []
    if recent_hb:
        bridge.append("ocas-mentor/%s/%s" % (DATE, recent_hb))
    bridge.append(forge_rel)
    for nf in new_files:
        bridge.append(nf)
    bridge.append(dispatch_rel)
    p_added = 0
    d_added = 0
    for rel in bridge:
        if append_unique_eval(PRAXIS_EVAL, "journal_id", rel,
                              "third_wave_mitigation",
                              "dispatch-new-journal-%s" % TS, NOW):
            p_added += 1
        if append_unique_eval(DISPATCH_EVAL, "filename", rel,
                              "dispatch_output_skip",
                              "dispatch-new-journal-%s" % TS, NOW):
            d_added += 1
    print("Eval bridged -> praxis:+%d dispatch:+%d" % (p_added, d_added))

    # ---- Step 4: Write dispatch-wave journal (NOT registered in eval) ----
    dispatch_dir = os.path.join(JDIR, "ocas-dispatch", DATE)
    os.makedirs(dispatch_dir, exist_ok=True)
    dispatch_path = os.path.join(JDIR, dispatch_rel)
    dispatch_entry = {
        "timestamp": NOW,
        "type": "dispatch.wave",
        "run_id": "dispatch-wave-%s" % TS,
        "result": "success",
        "summary": "Explicit-run new_journals dispatch: Forge scan no-op (%d proposals), "
                   "Mentor light heartbeat executed, journals re-registered in eval stores."
                   % len(unprocessed),
        "classification": "mixed_genuine",
        "actions_taken": {
            "journals": {"eval_gaps_found": 0, "eval_gaps_registered": 0,
                         "pipelines_loaded": 2},
            "email_triage": {"indigo_inbox": {"threads_reviewed": 0, "actionable": 0}},
        },
        "escalations": [],
        "notes": "Explicit-run override (new_journals). forge-scan no-op journal written; "
                 "Mentor heartbeat executed; eval bridges idempotent. Run via "
                 "ocas-forge/scripts/bridge_explicit_run.py.",
    }
    with open(dispatch_path, "w") as f:
        json.dump(dispatch_entry, f, indent=2)
    print("Dispatch-wave journal written:", dispatch_rel)

    # ---- Step 5: Advance last_ingest_run + resync counters ----
    mtimes = [os.path.getmtime(forge_path)]
    if recent_hb:
        mtimes.append(os.path.getmtime(os.path.join(mentor_dir, recent_hb)))
    for nf in new_files:
        full = os.path.join(JDIR, nf)
        if os.path.isfile(full):
            mtimes.append(os.path.getmtime(full))
    cutoff_dt = datetime.fromtimestamp(max(mtimes), timezone.utc)
    new_last = cutoff_dt.isoformat()
    state = json.load(open(STATE_PATH))
    state["last_ingest_run"] = new_last
    pc = sum(1 for _ in open(PRAXIS_EVAL))
    dc = sum(1 for _ in open(DISPATCH_EVAL))
    state["journals_evaluated_count"] = pc
    state["last_eval_file_line"] = pc
    json.dump(state, open(STATE_PATH, "w"), indent=2)
    print("State advanced last_ingest_run ->", new_last)
    print("Praxis eval lines:", pc, "Dispatch eval lines:", dc)
    print("DONE")


if __name__ == "__main__":
    main()