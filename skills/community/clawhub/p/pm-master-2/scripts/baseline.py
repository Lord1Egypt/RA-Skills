#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Baseline (Plan -> Baseline -> Control Gate)
======================================================

Freeze the "reviewed and approved" project plan into a baseline snapshot, used as
the reference benchmark for subsequent operational control.

Usage:
  # Freeze baseline (prerequisite: consistency gate exit 0)
  python3 baseline.py --freeze --project /workspace/<slug>/project.yaml

  # Show baseline status
  python3 baseline.py --status --project /workspace/<slug>/project.yaml

Discipline:
  --freeze first runs consistency_check.py; if it fails (the plan is not yet at
  control grade), baseline is refused.
  After baselining, write baselines/<YYYY-MM-DD>.yaml and record a pointer in
  project.yaml:
    baseline: {file: baselines/2026-07-15.yaml, on: 2026-07-15, by: <pm>}
    project.lifecycle_state: baselined
    project.baselined_on: 2026-07-15
  Also render baseline_record.md and control_register.md (operational control checklist).
"""
import os
import sys
import json
import subprocess
import datetime
import argparse

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, 'render.py')
CONSISTENCY = os.path.join(HERE, 'consistency_check.py')


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def collect_risks(data):
    seen = {}
    for r in (data.get('risks') or []):
        if r.get('id'):
            seen[r['id']] = r
    for r in ((data.get('raid') or {}).get('risks') or []):
        if r.get('id') and r['id'] not in seen:
            seen[r['id']] = r
    return list(seen.values())


def run(cmd):
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True)


def _date_integrity_ok(data):
    """P2-5: before freezing, validate that all WBS dates fall in a reasonable
    range and that dependencies are acyclic. Return (ok, messages). If there is a
    problem, refuse to freeze."""
    import datetime as _dt
    wbs = data.get('wbs') or []
    proj = data.get('project') or {}
    start = proj.get('start_date'); end = proj.get('target_end')
    msgs = []
    try:
        ps = _dt.date.fromisoformat(str(start)[:10]) if start else None
    except (ValueError, TypeError):
        ps = None
    try:
        pe = _dt.date.fromisoformat(str(end)[:10]) if end else None
    except (ValueError, TypeError):
        pe = None
    for w in wbs:
        s = w.get('start'); e = w.get('end')
        try:
            ws = _dt.date.fromisoformat(str(s)[:10]) if s else None
        except (ValueError, TypeError):
            ws = None
        try:
            we = _dt.date.fromisoformat(str(e)[:10]) if e else None
        except (ValueError, TypeError):
            we = None
        if ws and ps and ws < ps:
            msgs.append(f"{w.get('id')} start {ws} is earlier than project start {ps}")
        if we and pe and we > pe:
            msgs.append(f"{w.get('id')} end {we} is later than target completion {pe}")
        if ws and we and we < ws:
            msgs.append(f"{w.get('id')} end {we} is earlier than start {ws}")
    # Cycle detection
    ids = {w.get('id') for w in wbs}
    indeg = {w.get('id'): 0 for w in wbs}
    for w in wbs:
        for d in (w.get('dependsOn') or []):
            if d in ids:
                indeg[w['id']] += 1
    topo, q = [], [i for i in ids if indeg[i] == 0]
    while q:
        n = q.pop(0); topo.append(n)
        for w in wbs:
            if n in (w.get('dependsOn') or []):
                indeg[w['id']] -= 1
                if indeg[w['id']] == 0:
                    q.append(w['id'])
    cyclic = [i for i in ids if i not in topo]
    if cyclic:
        msgs.append(f"Cyclic dependency detected (cannot baseline): {', '.join(sorted(cyclic)[:10])}")
    return (len(msgs) == 0), msgs


def freeze(project_path, approve=False):
    root = os.path.dirname(os.path.abspath(project_path))
    data = load(project_path)
    proj = data.get('project', {}) or {}

    # ---- P2-5 date-integrity gate (before freezing) ----
    ok, msgs = _date_integrity_ok(data)
    if not ok:
        print("✗ Baseline rejected: date/dependency integrity check failed:")
        for m in msgs[:20]:
            print("  - " + m)
        sys.exit(6)

    # ---- Gate: plan must be at control grade before baselining ----
    chk = run([CONSISTENCY, '--project', project_path])
    if chk.returncode != 0:
        print("✗ Baseline rejected: consistency gate failed. Fix the following issues, then freeze:")
        print(chk.stdout)
        print(chk.stderr)
        sys.exit(2)

    today = datetime.date.today().isoformat()
    bdir = os.path.join(root, 'baselines')
    os.makedirs(bdir, exist_ok=True)
    bfile = os.path.join(bdir, today + '.yaml')

    snapshot = {
        'baselined_on': today,
        'by': proj.get('pm') or '(unspecified)',
        'project_id': proj.get('id'),
        'project_name': proj.get('name'),
        'methodology': proj.get('methodology'),
        'wbs': data.get('wbs') or [],
        'milestones': data.get('milestones') or [],
        'risks': collect_risks(data),
        'metrics': {'evm': (data.get('metrics') or {}).get('evm') or {}},
    }
    save(bfile, snapshot)

    # ---- Write back pointer to project.yaml (in place via project_state.py) ----
    rel = os.path.relpath(bfile, root)
    st = run([os.path.join(HERE, 'project_state.py'),
              'set', 'baseline.file', rel, '--file', project_path])
    run([os.path.join(HERE, 'project_state.py'),
         'set', 'baseline.on', today, '--file', project_path])
    run([os.path.join(HERE, 'project_state.py'),
         'set', 'baseline.by', str(proj.get('pm') or '(unspecified)'), '--file', project_path])
    run([os.path.join(HERE, 'project_state.py'),
         'set', 'project.lifecycle_state', 'baselined', '--file', project_path])
    run([os.path.join(HERE, 'project_state.py'),
         'set', 'project.baselined_on', today, '--file', project_path])

    # ---- Render baseline_record + control_register ----
    arts = data.get('artifacts', {}) or {}
    brec = arts.get('baseline_record') or 'artifacts/baseline_record.md'
    crec = arts.get('control_register') or 'artifacts/control_register.md'
    run([RENDER, '--template',
         os.path.join(HERE, '..', 'templates', 'common', 'baseline_record.md'),
         '--data', project_path, '--out', os.path.join(root, brec)])
    run([RENDER, '--template',
         os.path.join(HERE, '..', 'templates', 'common', 'control_register.md'),
         '--data', project_path, '--out', os.path.join(root, crec)])

    # ---- Register artifact pointers (for discovery + to satisfy the operational
    #      artifact requirement of the consistency gate) ----
    run([os.path.join(HERE, 'project_state.py'),
         'set', 'artifacts.baseline_record', brec, '--file', project_path])
    run([os.path.join(HERE, 'project_state.py'),
         'set', 'artifacts.control_register', crec, '--file', project_path])

    print(f"✓ Baseline completed ({today})")
    print(f"  Snapshot: {rel}")
    print(f"  WBS packages: {len(snapshot['wbs'])} | risks: {len(snapshot['risks'])} | "
          f"milestones: {len(snapshot['milestones'])}")
    print(f"  State: project.lifecycle_state = baselined")
    print(f"  Rendered: {brec}, {crec}")
    print(f"  Next: after passing the control gate (stage_gate_review), set lifecycle_state to "
          f"operational to enable periodic control_engine.py inspection.")
    if st.returncode != 0:
        print("[warn] project_state.py failed to write the pointer; please set baseline.file manually", file=sys.stderr)

    # ---- P1-2 hard-gate wiring: --freeze-and-approve auto-promotes to operational ----
    if approve:
        ge = run([os.path.join(HERE, 'gate_engine.py'), '--to', 'operational',
                  '--approve', '--project', project_path])
        if ge.returncode != 0:
            print("⚠ Control gate not passed; lifecycle_state remains baselined. See gate_engine output.")
            print(ge.stdout)
            print(ge.stderr)
        else:
            print("✓ Control gate passed and auto-promoted to operational. Run control_engine.py for periodic inspection.")


def status(project_path):
    data = load(project_path)
    proj = data.get('project', {}) or {}
    bl = data.get('baseline') or {}
    print("=== Baseline Status ===")
    print(f"Project: {proj.get('name')} ({proj.get('id')})")
    print(f"Lifecycle state: {proj.get('lifecycle_state', 'planning')}")
    print(f"Phase: {proj.get('phase')}")
    if bl.get('file'):
        print(f"Baseline file: {bl.get('file')}")
        print(f"Baseline date: {bl.get('on')}  baselined by: {bl.get('by')}")
    else:
        print("⚠ Not yet baselined (no baseline pointer). waterfall/hybrid must be baselined before entering execution/monitoring.")


def main():
    ap = argparse.ArgumentParser(description="PM Master Baseline")
    ap.add_argument('--project', required=True)
    ap.add_argument('--freeze', action='store_true', help="Freeze baseline (default action)")
    ap.add_argument('--freeze-and-approve', action='store_true',
                    help="Freeze baseline, pass the control gate, then auto-promote to operational (hard-gate wiring)")
    ap.add_argument('--status', action='store_true', help="Show baseline status")
    a = ap.parse_args()
    if a.status:
        status(a.project)
    elif a.freeze_and_approve:
        freeze(a.project, approve=True)
    else:
        freeze(a.project)


if __name__ == '__main__':
    main()
