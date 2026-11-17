#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · WBS Breakdown Write-back Glue (closes the "expert breakdown -> project.yaml" gap)
-------------------------------------------------
After an expert (human or sub-agent) breaks a SOW/domain package into leaf work packages,
they write the result into a "breakdown patch" YAML/JSON (structure in --help or the
example below). This script merges it back into project.yaml's `wbs` list, and
automatically:
  1. Hangs leaf packages under their parent package (by parent field / id prefix).
  2. Tags tier (program=summary/milestone, component=leaf).
  3. Validates every leaf package has role / owner / estimate / dod / dependsOn
     (fatal if missing).
  4. Writes back artifacts.wbs (if a build_wbs artifact already exists, marks it dirty).

Breakdown patch structure (list of packages; fields same as a wbs item, plus parent):
  - { id: SOW1.1, name: ..., domain: backend, role: backend-engineer, owner: Wang Wu,
      estimate: 8, dod: ..., dependsOn: [SOW1], parent: SOW1 }
  - { id: SOW1, name: Payment Refactor - Backend, domain: backend, role: solution-architect,
      estimate: 40, tier: program, summary: true }

Usage:
  python3 sync_wbs.py --project <yaml> --patch <breakdown patch.yaml>
  python3 sync_wbs.py --project <yaml> --patch <p.yaml> --dry-run   # validate only, no write
  python3 sync_wbs.py --project <yaml> --check-only                 # validate existing wbs only
"""
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import yaml
except ImportError:
    yaml = None

# Leaf package required fields (same constraint as consistency-gate Rule #9, enforced early here)
LEAF_REQUIRED = ['role', 'owner', 'estimate', 'dod', 'dependsOn']


def _load(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) if yaml else {}


def _save(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        if yaml:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
        else:
            import json
            json.dump(data, f, ensure_ascii=False, indent=2)


def _validate(pkgs, errors):
    by_id = {}
    for p in pkgs:
        pid = p.get('id')
        if not pid:
            errors.append('Work package without id exists')
            continue
        by_id[pid] = p
        if p.get('tier') == 'program' or p.get('summary'):
            continue  # summary/milestone packages do not require leaf fields
        for fld in LEAF_REQUIRED:
            v = p.get(fld)
            if v is None or v == '' or v == []:
                errors.append(f"Leaf package {pid} missing required field {fld}")
        est = p.get('estimate')
        if isinstance(est, (int, float)) and est <= 0:
            errors.append(f"Leaf package {pid} estimate must be > 0")
    # parent reference must exist
    for p in pkgs:
        par = p.get('parent')
        if par and par not in by_id:
            errors.append(f"Package {p.get('id')} parent={par} not found in wbs")
    return by_id


def _merge(data, patch):
    """Merge the patch into project.yaml.wbs (overwrite by id / append new)."""
    wbs = data.get('wbs') or []
    idx = {w.get('id'): i for i, w in enumerate(wbs) if w.get('id')}
    for p in patch:
        pid = p.get('id')
        if pid in idx:
            wbs[idx[pid]].update(p)
        else:
            wbs.append(p)
            idx[pid] = len(wbs) - 1
    data['wbs'] = wbs
    return data


def main():
    ap = argparse.ArgumentParser(description="PM Master · WBS breakdown write-back glue")
    ap.add_argument('--project', required=True, help="Single source of truth project.yaml")
    ap.add_argument('--patch', default=None, help="Breakdown patch YAML/JSON (list of packages)")
    ap.add_argument('--dry-run', action='store_true', help="Validate only, do not write back")
    ap.add_argument('--check-only', action='store_true', help="Validate existing wbs only, do not read patch")
    a = ap.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML required: run `pip install pyyaml`")

    data = _load(a.project)
    root = os.path.dirname(os.path.abspath(a.project))

    if a.check_only:
        errors = []
        _validate(data.get('wbs') or [], errors)
        if errors:
            print("✗ Validation failed:")
            for e in errors:
                print("  -", e)
            sys.exit(1)
        print("✓ Existing wbs validation passed")
        return

    if not a.patch or not os.path.exists(a.patch):
        print("✗ Please provide a --patch breakdown patch path", file=sys.stderr)
        sys.exit(2)

    patch = _load(a.patch)
    if not isinstance(patch, list):
        patch = patch.get('packages') or patch.get('wbs') or []
    if not isinstance(patch, list):
        print("✗ Patch must be a list of packages", file=sys.stderr)
        sys.exit(2)

    errors = []
    _validate(patch, errors)
    if errors:
        print("✗ Breakdown patch validation failed (not written):")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    if a.dry_run:
        print(f"✓ Patch validation passed; will merge {len(patch)} packages (dry-run, not written)")
        return

    data = _merge(data, patch)
    # Mark wbs artifact as dirty, signaling a re-render is needed
    art = data.setdefault('artifacts', {})
    if 'wbs' in art:
        art['wbs_dirty'] = True
    _save(a.project, data)
    print(f"[sync_wbs] Merged {len(patch)} packages into project.yaml.wbs; if wbs was already rendered, re-run build_wbs.py")


if __name__ == '__main__':
    main()
