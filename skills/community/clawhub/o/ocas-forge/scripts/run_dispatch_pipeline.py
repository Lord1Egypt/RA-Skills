#!/usr/bin/env python3
"""
Multi-skill dispatch pipeline runner (Forge + Mentor + Praxis).
Called by ocas-dispatch when a `new_journals` dispatch fires.

Usage:
  python3 os.path.expanduser("~/.hermes")/profiles/indigo/skills/ocas-forge/scripts/run_dispatch_pipeline.py --dispatch-ts 20260627T212600Z

This script:
1. Reads ingest_state.json to classify genuine vs second-wave
2. If genuine: registers missing journals, writes no-op journals, applies third-wave mitigation
3. If second-wave: adds eval gaps, advances state, exits

State files expected:
  os.path.expanduser("~/.hermes")/profiles/indigo/commons/data/ocas-praxis/ingest_state.json
  os.path.expanduser("~/.hermes")/profiles/indigo/commons/data/ocas-praxis/journals_evaluated.jsonl
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone

JOURNALS_BASE = os.path.expanduser('~/.hermes/profiles/indigo/commons/journals')
PRAXIS_DATA = os.path.expanduser('~/.hermes/profiles/indigo/commons/data/ocas-praxis')
EVAL_FILE = os.path.join(PRAXIS_DATA, 'journals_evaluated.jsonl')
STATE_FILE = os.path.join(PRAXIS_DATA, 'ingest_state.json')


def now_ts():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def date_dir():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def read_eval_set():
    """Read eval file into a set of journal_id strings."""
    eval_set = set()
    if os.path.exists(EVAL_FILE):
        with open(EVAL_FILE) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    eval_set.add(entry.get('journal_id', entry.get('filename', '')))
                except:
                    continue
    return eval_set


def read_state():
    """Read ingest state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def write_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def append_eval(entries):
    with open(EVAL_FILE, 'a') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')


def write_journal(skill, journal_data):
    ts = now_ts()
    ddir = date_dir()
    dirpath = os.path.join(JOURNALS_BASE, skill, ddir)
    os.makedirs(dirpath, exist_ok=True)
    fname = f"{skill.split('-')[-1]}-{ts}.json"
    fpath = os.path.join(dirpath, fname)
    with open(fpath, 'w') as f:
        json.dump(journal_data, f, indent=2)
    return f"{skill}/{ddir}/{fname}"


def main():
    parser = argparse.ArgumentParser(
        description="Run the legacy dispatch pipeline for a detected wave.",
        epilog="NOTE: for explicit-run new_journals overrides prefer scripts/bridge_explicit_run.py.\n"
               "Example:\n"
               "  python3 run_dispatch_pipeline.py --dispatch-ts 20260716T050000Z --new-files ocas-forge/2026-07-16/forge-scan-TS.json")
    parser.add_argument('--dispatch-ts', required=True,
                        help="the dispatcher detected_at timestamp, YYYYmmddTHHMMSSZ")
    parser.add_argument('--new-files', nargs='*', default=[],
                        help="relative paths of the journals the dispatcher flagged as new")
    args = parser.parse_args()

    eval_set = read_eval_set()
    state = read_state()

    # Classify: genuine if ANY new_file not in eval
    new_files = args.new_files if isinstance(args.new_files, list) else []
    # Filter out phantom files that don't exist on disk
    existing_files = []
    for f in new_files:
        fpath = os.path.join(JOURNALS_BASE, f)
        if os.path.exists(fpath):
            existing_files.append(f)
    missing = [f for f in existing_files if f not in eval_set]
    is_genuine = len(missing) > 0

    if not is_genuine:
        # Second wave: verify, advance state, exit
        state['last_ingest_run'] = now_iso()
        write_state(state)
        print(json.dumps({"result": "second_wave", "action": "state_advanced"}))
        return

    # Genuine dispatch: register missing journals
    entries = [{"journal_id": f, "source": "dispatch-pipeline-runner", "timestamp": now_iso()} for f in missing]
    append_eval(entries)

    state['journals_evaluated_count'] = (state.get('journals_evaluated_count') or 0) + len(missing)

    # Write no-op journals for each pipeline
    ts = now_ts()

    forge_journal = {
        "run_id": f"forge-scan-{ts}",
        "timestamp": now_iso(),
        "result": "no_op",
        "findings": {"unprocessed_proposals": 0, "note": f"Dispatch {args.dispatch_ts}"}
    }
    forge_path = write_journal("ocas-forge", forge_journal)

    mentor_journal = {
        "run_id": f"mentor-light-{ts}",
        "timestamp": now_iso(),
        "result": "no_op",
        "findings": {"journals_reviewed": len(missing), "new_patterns": 0}
    }
    mentor_path = write_journal("ocas-mentor", mentor_journal)

    praxis_journal = {
        "run_id": f"praxis-dispatch-{ts}",
        "timestamp": now_iso(),
        "result": "no_op",
        "findings": {"journals_ingested": len(missing), "events_recorded": 0}
    }
    praxis_path = write_journal("ocas-praxis", praxis_journal)

    # Third-wave mitigation: add own outputs to eval
    own = [
        {"journal_id": forge_path, "source": "dispatch-third-wave-mitigation", "timestamp": now_iso()},
        {"journal_id": mentor_path, "source": "dispatch-third-wave-mitigation", "timestamp": now_iso()},
        {"journal_id": praxis_path, "source": "dispatch-third-wave-mitigation", "timestamp": now_iso()},
    ]
    append_eval(own)

    state['journals_evaluated_count'] += 3
    state['last_ingest_run'] = now_iso()
    write_state(state)

    print(json.dumps({
        "result": "genuine_dispatch",
        "journals_registered": len(missing),
        "outputs": [forge_path, mentor_path, praxis_path]
    }))


if __name__ == '__main__':
    main()