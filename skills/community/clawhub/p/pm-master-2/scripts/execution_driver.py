#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master v2 · Execution Driver
==============================
Core execution-phase driver script. Closes the gap in v1.x where "planning-phase
automation was strong but the execution phase relied entirely on the Agent's own
reasoning".

Responsibilities:
  1. Read project.yaml and determine the work packages that should execute now
  2. Generate an execution checklist (filtered by priority, dependencies, status)
  3. Track Sprint/iteration progress (agile/iteration/hybrid)
  4. Auto-trigger control_engine.py inspection (if cadence since last inspection elapsed)
  5. Produce an execution status summary

Usage:
  python3 execution_driver.py --project /workspace/<slug>/project.yaml
  python3 execution_driver.py --project <yaml> --sprint 3           # specify a sprint
  python3 execution_driver.py --project <yaml> --check-control       # only check whether inspection is needed
  python3 execution_driver.py --project <yaml> --json                # JSON output
"""
import os
import sys
import argparse
import datetime
import subprocess

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTROL_ENGINE = os.path.join(SCRIPT_DIR, 'control_engine.py')
CONSISTENCY_CHECK = os.path.join(SCRIPT_DIR, 'consistency_check.py')


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def parse_deps(dep):
    """Parse the dependsOn field."""
    if dep is None:
        return []
    if isinstance(dep, list):
        return [str(x).strip() for x in dep if str(x).strip() and str(x).strip() not in ('—', '-')]
    s = str(dep).strip()
    if s in ('', '—', '-'):
        return []
    import re
    return [p.strip() for p in re.split(r'[,;]', s) if p.strip()]


def get_wbs_status(w):
    """Infer the WBS work-package status."""
    status = (w.get('status') or '').lower()
    if status in ('done', 'completed'):
        return 'done'
    if status in ('in_progress', 'in progress'):
        return 'in_progress'
    if status in ('blocked',):
        return 'blocked'
    return 'pending'


def is_ready(w, wbs_map, done_ids):
    """Check whether a work package is ready (all dependencies completed)."""
    deps = parse_deps(w.get('dependsOn'))
    if not deps:
        return True
    return all(d in done_ids for d in deps)


def get_executable_work(wbs, methodology):
    """Get the list of work packages executable right now."""
    wbs_map = {w.get('id'): w for w in wbs if w.get('id')}
    done_ids = {wid for wid, w in wbs_map.items() if get_wbs_status(w) == 'done'}
    in_progress_ids = {wid for wid, w in wbs_map.items() if get_wbs_status(w) == 'in_progress'}

    executable = []
    blocked = []

    for w in wbs:
        wid = w.get('id', '?')
        status = get_wbs_status(w)

        # Skip summary/milestone/done
        if w.get('summary') or w.get('milestone'):
            continue
        if status == 'done':
            continue

        if is_ready(w, wbs_map, done_ids):
            entry = {
                'id': wid,
                'name': w.get('name', ''),
                'status': status,
                'estimate': w.get('estimate', 0),
                'owner': w.get('owner', ''),
                'domain': w.get('domain', ''),
                'deliverable': w.get('deliverable', ''),
            }
            if status == 'blocked':
                blocked.append(entry)
            else:
                executable.append(entry)
        else:
            blocked.append({
                'id': wid,
                'name': w.get('name', ''),
                'status': 'waiting_deps',
                'estimate': w.get('estimate', 0),
                'owner': w.get('owner', ''),
                'domain': w.get('domain', ''),
                'deliverable': w.get('deliverable', ''),
            })

    return executable, blocked, in_progress_ids


def check_control_needed(project_yaml_path, data):
    """Check whether control_engine inspection should run.
    Prefer reading data['last_control_check'] (consistent with the project_state convention),
    otherwise fall back to control.last_control_check."""
    ctrl = data.get('control') or {}
    cadence_days = ctrl.get('cadence_days', 7)
    last_check = data.get('last_control_check') or ctrl.get('last_control_check')
    if last_check:
        if isinstance(last_check, str):
            try:
                last_check = datetime.date.fromisoformat(last_check)
            except ValueError:
                last_check = None
        if last_check:
            days_since = (datetime.date.today() - last_check).days
            if days_since < cadence_days:
                return False, days_since
    return True, 0


def stamp_control_check(data, path):
    """After inspection, write last_control_check to avoid redundant inspections (E4)."""
    data['last_control_check'] = datetime.date.today().isoformat()
    save(data, path)


def main():
    ap = argparse.ArgumentParser(description="PM Master v2 Execution Driver")
    ap.add_argument('--project', required=True, help="Path to project.yaml")
    ap.add_argument('--sprint', type=int, default=None, help="Specify sprint number (agile)")
    ap.add_argument('--check-control', action='store_true', help="Only check whether inspection is needed")
    ap.add_argument('--json', action='store_true', help="Output JSON")
    a = ap.parse_args()

    data = load(a.project)
    root = os.path.dirname(os.path.abspath(a.project))
    proj = data.get('project', {})
    methodology = (proj.get('methodology') or '').lower()
    lifecycle = (proj.get('lifecycle_state') or '')

    # State-machine check
    if lifecycle not in ('operational',):
        print(f"[execution_driver] Project is not in the operational state (current: {lifecycle}); cannot drive execution")
        print("  First complete: planning -> review -> baseline.py --freeze -> gate_engine.py --to execution")
        sys.exit(1)

    wbs = data.get('wbs') or []

    if a.check_control:
        needed, days = check_control_needed(a.project, data)
        if needed:
            print(f"[execution_driver] Need to run control_engine inspection")
            print(f"  python3 {CONTROL_ENGINE} --project {a.project}")
            sys.exit(0)
        else:
            print(f"[execution_driver] {days} days since last inspection; no inspection needed")
            sys.exit(0)

    # Get executable work
    executable, blocked, in_progress = get_executable_work(wbs, methodology)

    # Check whether inspection is needed
    ctrl_needed, days_since = check_control_needed(a.project, data)

    # SECURITY (ClawHub SDI-4): execution_driver never writes last_control_check.
    # The timestamp is stamped ONLY by control_engine.py after a genuine inspection
    # (control_engine.py:631). Previously this driver stamped it the moment an
    # inspection was *deemed necessary*, which let a deemed-necessary-but-not-run
    # inspection suppress the next real control check. We only report here.

    # Output
    if a.json:
        import json as _json
        result = {
            'project': proj.get('name'),
            'lifecycle_state': lifecycle,
            'methodology': methodology,
            'executable_count': len(executable),
            'in_progress_count': len(in_progress),
            'blocked_count': len(blocked),
            'control_check_needed': ctrl_needed,
            'executable': executable[:20],  # limit output
            'blocked': blocked[:20],
        }
        print(_json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== Execution Driver Report ===")
        print(f"Project: {proj.get('name')} | Methodology: {methodology} | State: {lifecycle}")
        print(f"Executable: {len(executable)} | In progress: {len(in_progress)} | Blocked: {len(blocked)}")
        if ctrl_needed:
            print(f"⚠ Need to run control_engine.py inspection ({days_since} days since last)")

        if executable:
            print(f"\n## Executable work packages (prioritize)")
            for i, w in enumerate(executable[:10]):
                status_tag = '🆕' if w['status'] == 'pending' else '🔄'
                print(f"  {i+1}. [{w['id']}] {w['name']} ({w['estimate']} person-days) - {w['owner'] or '(unassigned)'} {status_tag}")

        if blocked:
            print(f"\n## Blocked items")
            for i, w in enumerate(blocked[:10]):
                reason = 'waiting for dependencies' if w['status'] == 'waiting_deps' else w['status']
                print(f"  {i+1}. [{w['id']}] {w['name']} - {reason}")


if __name__ == '__main__':
    main()
