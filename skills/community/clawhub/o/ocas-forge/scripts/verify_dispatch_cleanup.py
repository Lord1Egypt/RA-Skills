#!/usr/bin/env python3
"""
Post-dispatch cleanup verifier for multi-skill dispatch pipelines.
Usage: python3 <hermes-home>/profiles/<profile>/skills/ocas-forge/scripts/verify_dispatch_cleanup.py

Checks:
1. All .json files with mtime > last_ingest_run are in journals_evaluated.jsonl
2. No phantom files (empty timestamps, double timestamps, literal placeholders)
3. Reports gaps with timestamps for manual review

Exit code: 0 if clean, 1 if gaps found.
"""
import os
import sys
import json
import datetime

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 verify_dispatch_cleanup.py")
    sys.exit(0)

JOURNALS_DIR = "<hermes-home>/profiles/<profile>/commons/journals"
EVAL_FILE = os.path.join(JOURNALS_DIR, "ocas-praxis", "journals_evaluated.jsonl")
STATE_FILE = "<hermes-home>/profiles/<profile>/commons/data/ocas-praxis/ingest_state.json"

def main():
    # Load state
    if not os.path.exists(STATE_FILE):
        print("ERROR: State file not found")
        sys.exit(1)
    
    with open(STATE_FILE) as f:
        state = json.load(f)
    
    last_ingest_run = state.get("last_ingest_run", "2026-01-01T00:00:00+00:00")
    last_ingest_dt = datetime.datetime.fromisoformat(
        last_ingest_run.replace("Z", "+00:00")
    )
    
    # Load eval set
    eval_set = set()
    if os.path.exists(EVAL_FILE):
        with open(EVAL_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        eval_set.add(entry.get("filename", entry.get("journal", "")))
                    except json.JSONDecodeError:
                        pass
    
    # Scan for gaps and phantom files
    gaps = []
    phantoms = []
    all_skills = ["ocas-forge", "ocas-mentor", "ocas-praxis", "ocas-dispatch"]
    
    for skill in all_skills:
        skill_dir = os.path.join(JOURNALS_DIR, skill)
        if not os.path.isdir(skill_dir):
            continue
        for root, dirs, files in os.walk(skill_dir):
            for fname in files:
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, JOURNALS_DIR)
                
                # Phantom checks
                basename = fname.replace(".json", "")
                if "{now" in basename or "PLACEHOLDER" in basename or "TS_PLACEHOLDER" in basename:
                    phantoms.append(rel)
                    continue
                # Check for empty timestamp: forge-scan-.json pattern
                if basename.endswith("-") or basename.endswith("_"):
                    phantoms.append(rel)
                    continue
                # Check for double timestamp: ...T20260626T...T...
                import re
                ts_pattern = re.findall(r'\d{8}T\d{6}', basename)
                if len(ts_pattern) > 1:
                    phantoms.append(rel)
                    continue
                
                # Mtime check
                mtime = os.path.getmtime(fpath)
                mdt = datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc)
                if mdt > last_ingest_dt:
                    if rel not in eval_set:
                        gaps.append((rel, mdt.isoformat()))
    
    # Report
    print(f"Dispatch Cleanup Verification")
    print(f"  last_ingest_run: {last_ingest_run}")
    print(f"  eval entries: {len(eval_set)}")
    print(f"  gaps: {len(gaps)}")
    print(f"  phantoms: {len(phantoms)}")
    
    if phantoms:
        print(f"\n⚠ PHANTOM FILES (delete immediately):")
        for p in phantoms:
            print(f"  {p}")
    
    if gaps:
        print(f"\n⚠ EVAL GAPS (add to journals_evaluated.jsonl):")
        for g, ts in sorted(gaps, key=lambda x: x[1]):
            print(f"  {ts}: {g}")
        sys.exit(1)
    else:
        print(f"\n✓ All clean. Dispatch complete.")
        sys.exit(0)

if __name__ == "__main__":
    main()