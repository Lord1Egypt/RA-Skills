#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Operational Artifact Guardrail (OAG)
================================================

Enforced (executable): during the operational / monitoring phases, any change to
project.yaml (the single source of truth) must be accompanied by a refresh of the
corresponding deliverable (artifact). Otherwise it counts as a guardrail breach.

This closes the root cause of the "facts changed, docs didn't follow" drift that
occurs in the manual/execution phase. A previous example client project suffered
from this guardrail being ignored during operations, leaving raid_log /
risk_register / portfolio_dashboard behind the source of truth until manually caught.

Judgment logic (content hashing, not mtime tricks):
  1. Compute the "required artifacts" set = all keys registered in artifacts
     union the mandatory keys derived from data presence
     (raid present -> raid_log / risk_register; metrics/actuals present ->
      status_report; program type with metrics/actuals present -> additionally
      portfolio_dashboard; wbs present -> wbs, etc.).
  2. For each required artifact:
     - Must be registered in artifacts and the file must exist; otherwise breach.
     - If artifacts_meta.<key>.source_hash exists: recompute the dependency hash
       from current data; match = fresh, mismatch = drift (breach).
     - If artifacts_meta.<key>.source_hash is missing (legacy docs produced before
       this guardrail): cannot judge, emit an ADVISORY (suggest re-render to enable
       drift detection), do not count as breach (avoid killing legacy docs).
  3. Any breach -> exit 1 and list details; all pass -> exit 0.

Can be used as:
  - A hard gate after every operational action by the orchestrator (post-Step-4 /
    pre-delivery);
  - An item in control_engine.py periodic inspection (artifact drift, RED escalation);
  - A check in gate_engine.py monitoring gate.

Usage:
  python3 artifact_guard.py --project <yaml> [--json]
  python3 artifact_guard.py --project <yaml> --stamp status_report portfolio_dashboard
      # For manually written / externally rendered docs, call after production to
      # record source_hash and enable drift detection
"""
import os
import sys
import json
import hashlib
import datetime
import argparse

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))


# artifact key -> the project.yaml top-level keys this deliverable depends on
# (any change to any of them should trigger a re-render)
DEPS = {
    'raid_log': ['raid'],
    'risk_register': ['risks', 'raid'],
    'status_report': ['metrics', 'actuals', 'progress', 'risks', 'raid', 'program'],
    'portfolio_dashboard': ['metrics', 'actuals', 'program', 'sows', 'project'],
    'wbs': ['wbs'],
    'program_charter': ['program', 'project'],
    'schedule_gantt': ['schedule', 'wbs'],
    'closure_report': ['actuals', 'metrics'],
    'lessons_learned': ['actuals', 'metrics'],
    'control_report': [],  # depends on everything; handled via advisory (no meta = suggest re-render)
}


def _cond_required(data):
    """Derive mandatory artifact keys from data presence."""
    req = set()
    if data.get('raid') or data.get('risks'):
        req.add('raid_log')
        req.add('risk_register')
    if data.get('metrics') or data.get('actuals'):
        req.add('status_report')
        if str(data.get('project', {}).get('type', '')).lower() == 'program':
            req.add('portfolio_dashboard')
    if data.get('wbs'):
        req.add('wbs')
    if str(data.get('project', {}).get('type', '')).lower() == 'program':
        req.add('program_charter')
    return req


def _hash_deps(data, keys):
    """Compute a stable hash over the relevant data slices (key presence included,
    so missing/new keys are also detectable)."""
    slices = [(k, data.get(k)) for k in keys]
    blob = json.dumps(slices, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()[:16]


def check_artifacts(project_yaml, data=None, quiet=False):
    """Return (ok:bool, violations:list, details:list[dict])."""
    if yaml is None:
        return False, ['PyYAML required'], []
    if data is None:
        with open(project_yaml, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    root = os.path.dirname(os.path.abspath(project_yaml))
    arts = data.get('artifacts', {}) or {}
    meta = data.get('artifacts_meta', {}) or {}
    registered = set(arts.keys())
    required = _cond_required(data) | registered

    violations = []
    details = []
    for key in sorted(required):
        rel = arts.get(key)
        if not rel:
            violations.append(f"[UNREGISTERED] {key}: required deliverable is not registered in artifacts")
            details.append({'key': key, 'status': 'MISSING_REG', 'path': ''})
            continue
        # Multi-file deliverables (e.g. sow_kickoffs: [...]) — check each file's existence
        if isinstance(rel, list):
            missing = []
            for r in rel:
                if not isinstance(r, str):
                    continue
                rp = r if os.path.isabs(r) else os.path.join(root, r)
                if not os.path.exists(rp):
                    missing.append(r)
            if missing:
                violations.append(f"[MISSING FILE] {key}: {', '.join(missing)} does not exist")
                details.append({'key': key, 'status': 'MISSING_FILE', 'path': ','.join(missing)})
            else:
                details.append({'key': key, 'status': 'OK', 'path': f'{len(rel)} files'})
            continue
        if not isinstance(rel, str):
            details.append({'key': key, 'status': 'ADVISORY_NO_META', 'path': ''})
            continue
        path = rel if os.path.isabs(rel) else os.path.join(root, rel)
        if not os.path.exists(path):
            violations.append(f"[MISSING FILE] {key}: {rel} does not exist")
            details.append({'key': key, 'status': 'MISSING_FILE', 'path': rel})
            continue
        m = meta.get(key) or {}
        if m.get('source_hash'):
            cur = _hash_deps(data, DEPS.get(key, []))
            if cur != m.get('source_hash'):
                violations.append(f"[DATA DRIFT] {key}: source data changed ({rel}) but not re-rendered")
                details.append({'key': key, 'status': 'STALE_HASH', 'path': rel})
            else:
                details.append({'key': key, 'status': 'OK', 'path': rel})
        else:
            # Legacy docs (produced before this guardrail) — cannot judge; emit advisory, do not count as breach
            details.append({'key': key, 'status': 'ADVISORY_NO_META', 'path': rel})
    return (len(violations) == 0), violations, details


def stamp(project_yaml, keys):
    """Record source_hash for the given artifact key (call after producing a
    manually written / externally rendered document)."""
    if yaml is None:
        raise RuntimeError("PyYAML required")
    with open(project_yaml, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    meta = data.setdefault('artifacts_meta', {})
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    stamped = []
    for key in keys:
        deps = DEPS.get(key)
        if deps is None:
            print(f"  ⚠ {key}: DEPS not defined, skipped (register it in artifact_guard.DEPS to enable detection)")
            continue
        h = _hash_deps(data, deps)
        meta[key] = {'source_hash': h, 'rendered_at': now}
        stamped.append(f"{key} -> {h}")
    with open(project_yaml, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    return stamped


def main():
    ap = argparse.ArgumentParser(description="PM Master · Operational Artifact Guardrail (OAG)")
    ap.add_argument('--project', required=True)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--stamp', nargs='+', metavar='KEY',
                    help="Record source_hash for the given artifact key (call after producing a manually written / externally rendered document)")
    a = ap.parse_args()

    if a.stamp:
        stamped = stamp(a.project, a.stamp)
        print("=== source_hash recorded ===")
        for s in stamped:
            print("  -", s)
        return

    ok, violations, details = check_artifacts(a.project)
    if a.json:
        print(json.dumps({'ok': ok, 'violations': violations, 'details': details},
                         ensure_ascii=False, indent=2))
    else:
        print("=== Operational Artifact Guardrail (OAG) ===")
        for d in details:
            icon = '✓' if d['status'] == 'OK' else ('ℹ' if d['status'] == 'ADVISORY_NO_META' else '✗')
            print(f"  {icon} {d['key']:20s} {d['status']}")
        if violations:
            print(f"\nGuardrail breaches: {len(violations)} (exit 1):")
            for v in violations:
                print("  -", v)
        else:
            adv = [d for d in details if d['status'] == 'ADVISORY_NO_META']
            if adv:
                print(f"\n✓ All tracked deliverables are consistent with the source of truth (exit 0)")
                print(f"  ℹ {len(adv)} legacy documents have not enabled drift detection (re-render to record source_hash)")
            else:
                print("\n✓ All deliverables are consistent with the source of truth (exit 0)")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
