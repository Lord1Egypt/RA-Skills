#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · WBS renderer (two-level granularity view)
----------------------------------------------------
`templates/waterfall/wbs.md` needs data keys such as `wbs_groups` / `view_label` /
`view_note` / `view_group_note` (derived by this script from project.yaml's wbs),
and cannot be rendered directly with render.py.

What it does:
  1. Read wbs from project.yaml.
  2. Filter by view + group by domain (domain), building wbs_groups (each group has
     name + items, each item carries a gantt_name for the mermaid Gantt).
  3. Render templates/waterfall/wbs.md -> <project root>/plans/wbs.md and write back artifacts.wbs.

Views (--view):
  - full (default): all work packages, grouped by domain.
  - program: program milestone level only (tier: program summary/milestone rows), grouped by domain.
  - component: component-tier finest leaves only (non-program tier), grouped by domain.

Usage:
  python3 build_wbs.py --project /workspace/<slug>/project.yaml
  python3 build_wbs.py --project <yaml> --view program
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


def _group_by_domain(rows):
    groups = []
    seen = {}
    for w in rows:
        dom = w.get('domain') or '(uncategorized)'
        if dom not in seen:
            seen[dom] = len(groups)
            groups.append({'name': dom, 'items': []})
        item = dict(w)
        item['gantt_name'] = w.get('name', w.get('id', ''))
        groups[seen[dom]]['items'].append(item)
    return groups


def _build_tree(rows):
    """Build the flat wbs into a hierarchical decomposition tree (parent field or
    id prefix 'X.Y' determines parent-child). Return a list of nodes:
    {id, name, role, domain, children:[...]}. Used by the template to render the
    mermaid decomposition tree (graph TD)."""
    nodes = {}
    for w in rows:
        pid = w.get('id')
        if not pid:
            continue
        nodes[pid] = {
            'id': pid,
            'name': w.get('name', pid),
            'role': w.get('role') or '',
            'domain': w.get('domain') or '',
            'tier': w.get('tier', ''),
            'parent': w.get('parent'),
            'children': [],
        }
    roots = []
    for pid, n in nodes.items():
        par = n.get('parent')
        # When no parent, try to infer from id prefix (e.g. SOW1.1 -> SOW1)
        if not par and '.' in pid:
            cand = pid.rsplit('.', 1)[0]
            par = cand if cand in nodes else None
        if par and par in nodes:
            n['parent_id'] = par
            nodes[par]['children'].append(n)
        else:
            roots.append(n)
    return roots


def main():
    ap = argparse.ArgumentParser(description="PM Master · WBS renderer (two-level granularity)")
    ap.add_argument('--project', required=True, help="Single source of truth: project.yaml")
    ap.add_argument('--view', default='full', choices=['full', 'program', 'component'],
                    help="View: full=all / program=program milestone level / component=component leaf level")
    ap.add_argument('--out', default=None, help="Output .md path (default <project root>/plans/wbs.md)")
    ap.add_argument('--template', default=None, help="WBS template path (default skill templates/waterfall/wbs.md)")
    a = ap.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML required: run `pip install pyyaml`")

    data = _load(a.project)
    wbs = data.get('wbs') or []
    if not wbs:
        raise SystemExit("⚠ No wbs found in project.yaml; cannot render WBS (complete the WBS decomposition first).")

    if a.view == 'program':
        rows = [w for w in wbs if w.get('tier') == 'program']
        view_label = 'Program milestone level'
        view_note = 'Shows only each SOW summary package + each phase milestone summary package (component leaf packages are held in their respective component projects)'
        view_group_note = 'Domain (program milestone level)'
    elif a.view == 'component':
        rows = [w for w in wbs if w.get('tier') != 'program']
        view_label = 'Component leaf level'
        view_note = 'Shows the finest leaf work-package level (including domain-expert decomposition packages)'
        view_group_note = 'Domain (component leaf level)'
    else:
        rows = list(wbs)
        view_label = 'All work packages'
        view_note = 'Work packages across the project lifecycle (summary + leaf)'
        view_group_note = 'Domain'

    wbs_groups = _group_by_domain(rows)
    wbs_tree = _build_tree(rows)

    tpl_path = a.template or os.path.join(SCRIPT_DIR, '..', 'templates', 'waterfall', 'wbs.md')
    tpl_path = os.path.abspath(tpl_path)
    if not os.path.exists(tpl_path):
        raise SystemExit(f"WBS template not found: {tpl_path}")
    with open(tpl_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    from render import render
    rendered = render(tpl, {
        'project': data.get('project', {}),
        'view_label': view_label,
        'view_note': view_note,
        'view_group_note': view_group_note,
        'wbs_groups': wbs_groups,
        'wbs_tree': wbs_tree,
    })

    root = os.path.dirname(os.path.abspath(a.project))
    out_path = a.out or os.path.join(root, 'plans', 'wbs.md')
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    rel = os.path.relpath(out_path, root)
    if 'artifacts' not in data or not isinstance(data['artifacts'], dict):
        data['artifacts'] = {}
    data['artifacts']['wbs'] = rel
    _save(a.project, data)

    print(f"[wbs] WBS rendered ({a.view} view, {len(wbs_groups)} domain groups, {len(rows)} packages): {out_path}")
    print(f"[wbs] artifacts.wbs = {rel}")


if __name__ == '__main__':
    main()
