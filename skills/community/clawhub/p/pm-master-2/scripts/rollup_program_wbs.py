#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Program WBS two-tier rollup (tagged single-source model)
============================================================

Refactor the single-source project.yaml wbs into a two-tier structure, satisfying the
granularity convention "program tier = milestone level, component tier = leaf work-package level":

  - SOW summary package (id has no '.' or summary:true)        -> tier: program, summary: true
  - A milestone summary package per SOW / P0 phase             -> tier: program, milestone: true
  - All leaf work packages (id contains '.')                   -> tier: component, component: <slug>

The component view (build_wbs.py --view component --component <slug>) filters only tier:component leaves;
the program view (build_wbs.py --view program) filters only tier!=component summary + milestone packages.

`--derive-actuals`: roll up leaf actual progress (weighted by estimate) into each milestone's actual %,
writing it into project.yaml's actuals.wbs_progress (keyed by milestone id), so the program-tier
progress control table (control_engine) can present at milestone granularity directly.

Only rewrites project.yaml's `wbs:` block (and optionally `actuals.wbs_progress:`) while preserving all
other sections and comments; a backup <project.yaml>.bak-<date> is made automatically before execution.

> The component / phase mapping (COMPONENT_MAP / PHASE_NAME) are example defaults (taken from the sample project).
> For production, provide `program.components` (SOW id -> component slug) and `governance.waves`
> (phase key -> phase name) in project.yaml; the engine prefers project-level config and falls back to
> the example with a warning when absent.

Usage:
  python3 rollup_program_wbs.py <program/project.yaml>
  python3 rollup_program_wbs.py <program/project.yaml> --derive-actuals
"""
import os
import sys
import shutil
import datetime
import collections
import yaml

# Example defaults (taken from the sample project). For production, use project.yaml's
# program.components / governance.waves; see COMPONENT_MAP_EFF / PHASE_NAME_EFF below.
COMPONENT_MAP = {
    'P0': 'pmo-program-management',
    'SOW1': 'sow1',
    'SOW2': 'sow2',
    'SOW3': 'sow3',
    'SOW4': 'sow4',
    'SOW5': 'sow5',
    'SOW6': 'sow6',
    'SOW7': 'sow7',
    'SOW8': 'sow8',
    'SOW9': 'sow9',
    'EXT-PII': 'ext-pii',
}
PHASE_NAME = {
    'M0': 'M0 Mobilization and Readiness',
    'W1': 'Stream 1 Foundation Modeling',
    'W2': 'Stream 2 Protocol Processing',
    'W3': 'Stream 3 Analysis Structure',
    'W4': 'Stream 4 Archiving and Integration',
}
# Effective mapping at runtime: overridden by main() per project.yaml; falls back to the example when absent.
COMPONENT_MAP_EFF = dict(COMPONENT_MAP)
PHASE_NAME_EFF = dict(PHASE_NAME)
P0_KEYWORD = [
    ('Charter', 'Charter'), ('Method', 'Charter'),
    ('Governance', 'Governance'), ('RACI', 'Governance'),
    ('Stage Gate', 'StageGate'),
    ('IMS', 'IMS Baseline'), ('Master Schedule', 'IMS Baseline'),
    ('Steering Committee', 'Steering'), ('Regular Meeting', 'Steering'),
]


def parse_date(s):
    if not s:
        return None
    for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.datetime.strptime(str(s), fmt).date()
        except ValueError:
            continue
    return None


def dur_str(s, e):
    if not s or not e:
        return None
    d = (e - s).days
    return f"{d}d" if d >= 0 else None


def clean(row):
    return {k: v for k, v in row.items() if v is not None}


# Cancelled/terminated states: the milestone row should also carry the cancelled status
# to avoid the control engine falsely reporting it as overdue.
_CANCELLED_LEAF_STATES = {'cancelled', 'canceled', 'descoped', 'out-of-scope', 'terminated'}


def _rollup_status(items):
    """Roll up milestone status from leaf-package statuses: all cancelled/terminated -> cancelled;
    otherwise unset (derived from progress %)."""
    if not items:
        return None
    sts = {str(i.get('status', '')).lower() for i in items}
    if sts and sts <= _CANCELLED_LEAF_STATES:
        return 'cancelled'
    return None


def build_milestone(top, phase, items, prev_id, label=None):
    ests = [float(i.get('estimate') or 0) for i in items]
    est = round(sum(ests), 1)
    starts = [parse_date(i.get('start')) for i in items]
    ends = [parse_date(i.get('end')) for i in items]
    s = min([x for x in starts if x], default=None)
    e = max([x for x in ends if x], default=None)
    name = label if label else PHASE_NAME_EFF.get(phase, phase)
    mid = f"{top}-{label}" if label else f"{top}-{phase}"
    dlv = ' / '.join(str(i.get('deliverable', '')) for i in items[:3] if i.get('deliverable'))
    row = {
        'id': mid,
        'name': f"{top} · {name}",
        'level': 2,
        'milestone': True,
        'tier': 'program',
        'summary': False,
        'component': COMPONENT_MAP_EFF.get(top, top.lower()),
        'deliverable': dlv[:160],
        'owner': items[0].get('owner', ''),
        'estimate': est,
        'duration': dur_str(s, e),
        'start': s.isoformat() if s else None,
        'end': e.isoformat() if e else None,
    }
    if prev_id:
        row['dependsOn'] = prev_id
    rolled = _rollup_status(items)
    if rolled:
        row['status'] = rolled
    return clean(row), [i['id'] for i in items]


def find_block(path, key_line):
    """Return (start_idx, end_idx) covering the whole block starting at key_line (until the next top-level key)."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.rstrip('\n') == key_line:
            start = i
            break
    if start is None:
        for i, ln in enumerate(lines):
            if ln.strip() == key_line:
                start = i
                break
    if start is None:
        return None, None, lines
    end = len(lines)
    for i in range(start + 1, len(lines)):
        stripped = lines[i].lstrip(' ')
        if lines[i][:1] not in (' ', '\t', '\n', '#') and stripped and not stripped.startswith('- '):
            end = i
            break
    return start, end, lines


def rewrite_wbs_block(path, new_wbs):
    start, end, lines = find_block(path, 'wbs:')
    if start is None:
        # When the skeleton has no wbs: block (e.g. legacy init output), append at end of file for compatibility
        lines.append('\nwbs:\n')
        start = len(lines) - 1
        end = len(lines) - 1
    dumped = yaml.safe_dump(new_wbs, allow_unicode=True, sort_keys=False,
                            default_flow_style=False)
    block = ['wbs:\n'] + [dumped]
    lines[start:end] = block
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def inject_milestone_actuals(path, ms_actuals):
    """Insert milestone actual-% keys at the end of the actuals.wbs_progress block (before ev:)."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # locate the wbs_progress: line
    wp = None
    for i, ln in enumerate(lines):
        if ln.rstrip('\n') == '  wbs_progress:':
            wp = i
            break
    if wp is None:
        print("[warn] actuals.wbs_progress: not found, skipping milestone actual% injection")
        return
    # find the first 2-space top-level key after it (ev: / ac:) as the insertion point
    insert_at = None
    for i in range(wp + 1, len(lines)):
        if lines[i].startswith('  ') and not lines[i].startswith('    ') and lines[i].strip():
            insert_at = i
            break
    if insert_at is None:
        insert_at = len(lines)
    new_lines = [f"    {mid}: {val:.1f}\n" for mid, val in ms_actuals]
    lines[insert_at:insert_at] = new_lines
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="PM Master program WBS two-tier rollup")
    ap.add_argument('project')
    ap.add_argument('--derive-actuals', action='store_true',
                    help="Roll up leaf actual%% weighted into milestone actual%%, writing into actuals.wbs_progress")
    a = ap.parse_args()

    path = os.path.abspath(a.project)
    if not os.path.exists(path):
        print(f"✗ file not found: {path}")
        sys.exit(2)
    backup = f"{path}.bak-{datetime.date.today().isoformat()}"
    shutil.copy(path, backup)

    doc = yaml.safe_load(open(path, encoding='utf-8'))
    wbs = doc.get('wbs', [])

    # Component / phase mapping: prefer project-level config, fall back to the example with a warning
    # (decoupling from hard-coded values)
    prog = doc.get('program') or {}
    gov = doc.get('governance') or {}
    comp_override = prog.get('components') if isinstance(prog.get('components'), dict) else None
    wave_override = (gov.get('waves') if isinstance(gov.get('waves'), dict) else None) or \
                    (prog.get('waves') if isinstance(prog.get('waves'), dict) else None)
    if comp_override:
        COMPONENT_MAP_EFF.update(comp_override)
    else:
        print("[rollup] Warning: program.components not provided, using the built-in example COMPONENT_MAP "
              "(sample project). For production, configure program.components in project.yaml "
              "(SOW id -> component slug).", file=sys.stderr)
    if wave_override:
        PHASE_NAME_EFF.update(wave_override)
    else:
        print("[rollup] Warning: governance.waves not provided, using the built-in example PHASE_NAME. "
              "For production, configure governance.waves in project.yaml (phase key -> phase name).", file=sys.stderr)

    # Idempotency guard: if a tier:program milestone summary package already exists, treat it as already
    # two-tiered and do not regenerate (avoids duplication / mis-classifying a milestone as a summary).
    already = any(w.get('milestone') and w.get('tier') == 'program' for w in wbs)

    summaries = []
    leaves = []
    existing_ms = []
    for w in wbs:
        wid = str(w.get('id', ''))
        if w.get('milestone') and w.get('tier') == 'program':
            existing_ms.append(w)
            continue
        if w.get('summary') or ('.' not in wid):
            w['tier'] = 'program'
            w['summary'] = True
            top = wid.split('.')[0]
            w['component'] = COMPONENT_MAP_EFF.get(top, top.lower())
            summaries.append(w)
        else:
            top = wid.split('.')[0]
            w['tier'] = 'component'
            w['component'] = COMPONENT_MAP_EFF.get(top, top.lower())
            leaves.append(w)

    by_top = collections.OrderedDict()
    for w in leaves:
        top = str(w['id']).split('.')[0]
        by_top.setdefault(top, []).append(w)

    # Always rebuild the milestone -> leaf mapping by deterministic rules (used by --derive-actuals)
    ms_leaves = {}
    ms_est = {}
    milestone_rows = existing_ms[:] if already else []
    for top, lvs in by_top.items():
        phases = collections.OrderedDict()
        unphased = []
        for w in lvs:
            segs = str(w['id']).split('.')
            if len(segs) >= 3:
                phases.setdefault(segs[1], []).append(w)
            else:
                unphased.append(w)
        prev_id = None
        for ph, items in phases.items():
            m, lids = build_milestone(top, ph, items, prev_id)
            ms_leaves[m['id']] = lids
            ms_est[m['id']] = m.get('estimate', 0)
            if not already:
                milestone_rows.append(m)
            prev_id = m['id']
        if unphased:
            if top == 'P0':
                kg = collections.OrderedDict()
                for w in unphased:
                    label = 'PMO'
                    for kw, lab in P0_KEYWORD:
                        if kw in str(w.get('name', '')):
                            label = lab
                            break
                    kg.setdefault(label, []).append(w)
                for lab, items in kg.items():
                    m, lids = build_milestone(top, lab, items, prev_id, label=lab)
                    ms_leaves[m['id']] = lids
                    ms_est[m['id']] = m.get('estimate', 0)
                    if not already:
                        milestone_rows.append(m)
                    prev_id = m['id']
            else:
                m, lids = build_milestone(top, 'DELIVERY', unphased, prev_id,
                                          label=f"{top} Delivery")
                ms_leaves[m['id']] = lids
                ms_est[m['id']] = m.get('estimate', 0)
                if not already:
                    milestone_rows.append(m)
                prev_id = m['id']

    new_wbs = summaries + milestone_rows + leaves
    rewrite_wbs_block(path, new_wbs)
    print(f"[rollup] backup -> {backup}")
    print(f"[rollup] summaries={len(summaries)} milestones={len(milestone_rows)} "
          f"leaves={len(leaves)} -> program wbs total={len(new_wbs)}")

    if a.derive_actuals:
        actuals = (doc.get('actuals') or {})
        prog = actuals.get('wbs_progress') or {}
        ms_actuals = []
        for mid, lids in ms_leaves.items():
            num = 0.0
            den = 0.0
            for lid in lids:
                la = float(prog.get(lid, 0) or 0)
                le = float(ms_est.get(lid) or 0) or 1.0  # fallback weight
                num += la * le
                den += le
            val = round(num / den, 1) if den else 0.0
            ms_actuals.append((mid, val))
        inject_milestone_actuals(path, ms_actuals)
        print(f"[rollup] derived {len(ms_actuals)} milestone actual% -> actuals.wbs_progress")


if __name__ == '__main__':
    main()
