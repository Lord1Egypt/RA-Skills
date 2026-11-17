#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Project scaffolding
-------------------------------------------------
Create the standard directory structure under /workspace/<slug>/ and write a
project.yaml skeleton (single source of truth).

Usage:
  python3 init_project.py "Payment re-platforming" --type project --methodology agile --framework scrum
  python3 init_project.py "Digital transformation program" --type program --methodology hybrid

Generated structure:
  <slug>/
  ├── project.yaml          # single source of truth
  ├── docs/                 # charter, scope, requirements documents
  ├── plans/                # WBS, schedule, iteration plan
  ├── risks/                # risk register, RAID
  ├── reports/              # status reports, retrospectives
  └── artifacts/            # rendered formal documents
"""
import os
import sys
import argparse
import datetime

try:
    import yaml
except ImportError:
    yaml = None

BASE = "/workspace"


def slugify(name):
    s = name.strip().lower()
    s = ''.join(c if (c.isalnum() or c in '-_') else '-' for c in s)
    return s.strip('-') or 'project'


def build_skeleton(name, ptype, methodology, framework, domain='', product=''):
    today = datetime.date.today().isoformat()
    return {
        'schema_version': 2,
        '_checkpoint': {'step': 'init', 'at': today, 'phase': 'initiation' if ptype == 'project' else 'program-definition'},
        'project': {
            'id': slugify(name),
            'name': name,
            'type': ptype,
            'methodology': methodology,
            'framework': framework if methodology == 'agile' else None,
            'phase': 'initiation' if ptype == 'project' else 'program-definition',
            'status': 'planning',
            'lifecycle_state': 'planning',
            'baselined_on': None,
            'domain': domain,
            'product': product,
            'created': today,
            'start_date': None,
            'target_end': None,
            'objectives': [],
            'scope': '',
            'out_of_scope': '',
            'sponsor': '',
            'pm': '',
            'team': [],
        },
        'governance': {'stage_gates': [], 'cadence': ''},
        'artifacts': {},
        'raid': {'risks': [], 'assumptions': [], 'issues': [], 'dependencies': []},
        'metrics': {'evm': {}, 'burndown': []},
        'wbs': [],
        'milestones': [],
        'actuals': {},
        'control': {
            'leaf_granularity': 'fortnight',  # Pillar 3: leaf packages default to fortnight granularity
            'granularity_threshold': 10,     # = 10 person-days (approx fortnight)
            'cadence': '',
        },
        'program': (
            {'projects': [], 'dependencies': [], 'benefits': []}
            if ptype == 'program' else None
        ),
    }


def main():
    ap = argparse.ArgumentParser(description="PM Master project scaffolding")
    ap.add_argument('name', help="Project/program name")
    ap.add_argument('--type', default='project', choices=['project', 'program'])
    ap.add_argument('--methodology', default='agile',
                    choices=['waterfall', 'agile', 'iteration', 'hybrid'])
    ap.add_argument('--framework', default='scrum', choices=['scrum', 'kanban'])
    ap.add_argument('--domain', default='', help="Domain tag, e.g. insurance-data-lake / payments, used for domain specialization in expert dispatch")
    ap.add_argument('--product', default='', help="Product name, used for expert dispatch specialization (fallback when domain is absent)")
    ap.add_argument('--base', default=BASE, help="Workspace root directory")
    ap.add_argument('--parent', default=None, help="Parent project/program project.yaml (fill in when creating a subproject)")
    ap.add_argument('--sow', default=None, help="Related parent program SOW id (e.g. SOW1), written into program.projects")
    ap.add_argument('--slug', default=None, help="Subproject directory slug (defaults to slugify(name))")
    a = ap.parse_args()

    # Subproject mode: create an independent project.yaml under parent_root/subprojects/<slug>/
    if a.parent:
        parent_path = os.path.abspath(a.parent)
        if not os.path.exists(parent_path):
            print(f"[init] Parent project does not exist: {parent_path}"); sys.exit(2)
        parent_dir = os.path.dirname(parent_path)
        slug = a.slug or slugify(a.name)
        root = os.path.join(parent_dir, 'subprojects', slug)
        if os.path.exists(root):
            print(f"[init] Subproject already exists, skipping: {root}"); return
        os.makedirs(os.path.join(root, 'docs'))
        os.makedirs(os.path.join(root, 'plans'))
        os.makedirs(os.path.join(root, 'risks'))
        os.makedirs(os.path.join(root, 'reports'))
        os.makedirs(os.path.join(root, 'artifacts'))
        skeleton = build_skeleton(a.name, a.type, a.methodology, a.framework,
                                  domain=a.domain, product=a.product)
        skeleton['parent'] = {
            'project': os.path.relpath(parent_path, root),
            'sow': a.sow,
        }
        with open(os.path.join(root, 'project.yaml'), 'w', encoding='utf-8') as f:
            yaml.safe_dump(skeleton, f, allow_unicode=True, sort_keys=False)
        # Write back the program.projects index
        pdoc = yaml.safe_load(open(parent_path, encoding='utf-8'))
        pdoc.setdefault('program', {})
        pdoc['program'].setdefault('projects', [])
        entry = {'id': slug, 'name': a.name, 'sow': a.sow, 'slug': slug,
                 'methodology': a.methodology, 'status': 'planning',
                 'path': os.path.relpath(root, parent_dir)}
        if not any(e.get('id') == slug for e in pdoc['program']['projects']):
            pdoc['program']['projects'].append(entry)
        yaml.safe_dump(pdoc, open(parent_path, 'w', encoding='utf-8'),
                       allow_unicode=True, sort_keys=False)
        print(f"[init] Subproject created (from project): {root}")
        print(f"[init] program.projects indexed: {slug} -> {a.sow or '(no SOW specified)'}")
        return

    root = os.path.join(a.base, slugify(a.name))
    if os.path.exists(root):
        print(f"[init] Already exists, skipping: {root}")
        return
    os.makedirs(os.path.join(root, 'docs'))
    os.makedirs(os.path.join(root, 'plans'))
    os.makedirs(os.path.join(root, 'risks'))
    os.makedirs(os.path.join(root, 'reports'))
    os.makedirs(os.path.join(root, 'artifacts'))

    skeleton = build_skeleton(a.name, a.type, a.methodology, a.framework,
                              domain=a.domain, product=a.product)
    with open(os.path.join(root, 'project.yaml'), 'w', encoding='utf-8') as f:
        if yaml:
            yaml.safe_dump(skeleton, f, allow_unicode=True, sort_keys=False)
        else:
            import json
            json.dump(skeleton, f, ensure_ascii=False, indent=2)

    print(f"[init] Project workspace created: {root}")
    print(f"       type={a.type}  methodology={a.methodology}"
          + (f"  framework={a.framework}" if a.methodology == 'agile' else ""))


if __name__ == '__main__':
    main()
