#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · SOW-level Kick-off batch generator
---------------------------------------------
Fixes the gap where "SOW-level individual kick-offs were not run and produced no
artifacts": each SOW (Statement of Work) level summary package should, during the
planning phase, produce a per-SOW kick-off artifact (templates/common/sow_kickoff.md)
via this script, aligning scope / deliverables / owners / first actions.

Identifying SOW-level packages:
  - Preferred: wbs rows with `summary: true` and tier != 'program' (i.e. SOW-level summary packages);
  - Fallback: if no explicit summary flag, take "top-level packages" (id has no '.' and has
    child packages prefixed with it, e.g. 'SOW1' has 'SOW1.1').

Each SOW package derives:
  - deliverables: names of its leaf packages (ids starting with '<sow_id>.');
  - experts: de-duplicated roles of leaf packages;
  - participants: SOW owner + domain experts + PM + sponsor;
  - kickoff_date: project.start_date or 'TBD'.

Output: <project root>/plans/kickoff/<sow_id>_kickoff.md, and write the path back to
        project.yaml's artifacts.sow_kickoffs (list).

Usage:
  python3 build_sow_kickoff.py --project /workspace/<slug>/project.yaml
  python3 build_sow_kickoff.py --project <yaml> --out-dir /custom/kickoff
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


def _load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _as_list(v):
    """Normalize a string/list into a list, for template {{#each}} rendering."""
    if v is None:
        return None
    if isinstance(v, list):
        return v
    return [v]


def _identify_sow_packages(wbs):
    """Return the list of SOW-level package ids.

    Only program-tier (tier=program) summary packages count as independent SOWs,
    to avoid misclassifying component-tier phase summary packages (e.g. SOW1.1 phase
    groups) as independent SOWs and opening redundant kick-offs.
    """
    explicit = [w.get('id') for w in wbs
                if w.get('summary') and w.get('tier') == 'program' and w.get('id')]
    if explicit:
        return explicit
    # Fallback: top-level packages that have children (and are program-tier)
    ids = [w.get('id') for w in wbs if w.get('id')]
    sows = []
    for w in wbs:
        wid = w.get('id')
        if not wid or '.' in wid:
            continue
        has_child = any(i != wid and i.startswith(wid + '.') for i in ids)
        if w.get('tier') == 'program' and has_child:
            sows.append(wid)
    return sows


def main():
    ap = argparse.ArgumentParser(description="PM Master · SOW Kick-off batch generator")
    ap.add_argument('--project', required=True, help="Single source of truth: project.yaml")
    ap.add_argument('--out-dir', default=None, help="Output directory (default <project root>/plans/kickoff)")
    ap.add_argument('--template', default=None, help="Kick-off template (default skill templates/common/sow_kickoff.md)")
    a = ap.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML required: run `pip install pyyaml`")

    data = _load(a.project)
    wbs = data.get('wbs') or []
    if not wbs:
        raise SystemExit("⚠ No wbs found in project.yaml; cannot generate SOW kick-offs (complete the WBS decomposition first).")

    sow_ids = _identify_sow_packages(wbs)
    if not sow_ids:
        print("[sow_kickoff] No SOW-level packages identified (summary: true or top-level packages with children); skipping.")
        return

    proj = data.get('project') or {}
    kickoff_date = proj.get('start_date') or 'TBD'
    pm = proj.get('pm') or '(TBD)'
    sponsor = proj.get('sponsor') or '(TBD)'

    tpl_path = a.template or os.path.join(SCRIPT_DIR, '..', 'templates', 'common', 'sow_kickoff.md')
    tpl_path = os.path.abspath(tpl_path)
    if not os.path.exists(tpl_path):
        raise SystemExit(f"Kick-off template not found: {tpl_path}")
    with open(tpl_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    from render import render

    root = os.path.dirname(os.path.abspath(a.project))

    if 'artifacts' not in data or not isinstance(data['artifacts'], dict):
        data['artifacts'] = {}
    data.setdefault('sow_kickoffs', [])

    produced = []
    for sow_id in sow_ids:
        sow = next((w for w in wbs if w.get('id') == sow_id), {})
        leaves = [w for w in wbs if str(w.get('id', '')).startswith(sow_id + '.')]
        deliverables = [{'id': w.get('id'), 'name': w.get('name', w.get('id'))} for w in leaves]
        experts = []
        for w in leaves:
            r = w.get('role')
            if r and r not in experts:
                experts.append(r)
        participants = [{'name': sow.get('owner') or '(TBD)', 'role': 'SOW Owner'}]
        for r in experts:
            participants.append({'name': f'({r} expert)', 'role': f'Domain expert ({r})'})
        participants.append({'name': pm, 'role': 'Project Manager (PM)'})
        participants.append({'name': sponsor, 'role': 'Sponsor'})

        ctx = {
            'project': proj,
            'sow': {
                'id': sow_id,
                'name': sow.get('name', sow_id),
                'domain': sow.get('domain') or '(TBD)',
                'owner': sow.get('owner') or '(TBD)',
                'objective': sow.get('objective') or sow.get('deliverable') or sow.get('name', sow_id),
                'scope': sow.get('scope') or sow.get('deliverable') or '(TBD)',
            },
            'deliverables': deliverables,
            'experts': experts,
            'participants': participants,
            'kickoff_date': kickoff_date,
            'decisions': sow.get('kickoff_decisions')
                or [{'id': 1, 'item': 'Confirm scope and deliverables', 'conclusion': '(TBD)'}],
            'assumptions': _as_list(sow.get('assumptions')) or ['(TBD)'],
            'next_actions': sow.get('next_actions')
                or [{'action': 'Decompose and dispatch leaf work packages', 'owner': sow.get('owner') or '(TBD)', 'due': '(TBD)'}],
            'artifacts': sow.get('artifacts') or ['(TBD)'],
            'status': sow.get('status') or 'planning',
        }
        rendered = render(tpl, ctx)
        slug = str(sow_id).replace('.', '_')
        if a.out_dir:
            out_path = os.path.join(a.out_dir, f'{slug}_kickoff.md')
        else:
            # Each SOW gets its own sub-plan folder (kickoff + schedule together),
            # executable independently and linked to the parent project
            out_dir = os.path.join(root, 'plans', slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, 'kickoff.md')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        rel = os.path.relpath(out_path, root)
        produced.append(rel)
        data['artifacts'][f'sow_kickoff_{slug}'] = rel
        data['artifacts'][f'sow_plan_{slug}'] = os.path.relpath(os.path.dirname(out_path), root)
        print(f"[sow_kickoff] Generated {sow_id} kick-off: {out_path}")

    data['artifacts']['sow_kickoffs'] = produced
    _save(a.project, data)
    print(f"[sow_kickoff] {len(produced)} SOW kick-offs generated; written to artifacts.sow_kickoffs")


if __name__ == '__main__':
    main()
