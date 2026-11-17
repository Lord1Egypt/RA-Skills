#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · SOW / Contract parser (foundation layout hardening v2.2)

Convert the comprehension record (spec, JSON) into WBS packages.

Persisting is a DESTRUCTIVE, explicit action: the old SOW subtree is deleted and
replaced. It is gated behind the `--apply` flag (a dated backup of project.yaml is
written first). `--dry-run` (or running with neither flag) only prints the packages
that would be written. The spec must pass the (a) text-extraction + (c) guided-Q&A
double confirmation BEFORE `--apply` is used.

Behavior:
  - Idempotent: delete the SOW's old subtree (id==SOWn or id starts with "SOWn.")
    then append new packages.
  - Bottom-up rollup of summary/milestone estimates; estimate defaults to duration_days.
  - Default dependency chain: entry_gate -> Wave1 -> leaf chain -> W1 milestone -> Wave2 ... -> delivery milestone.
  - Write/update fee / fee_type / methodology / status in sow_map.
  - At the end, automatically run consistency_check.py (a fixed-fee SOW must have a
    billing milestone, otherwise it fails fatally).

Usage:
  python3 parse_sow.py --emit-spec-template
  python3 parse_sow.py --project <program/project.yaml> --spec <sowN.spec.json>
  python3 parse_sow.py --project <program/project.yaml> --spec <sowN.spec.json> --dry-run
"""
import argparse
import json
import os
import re
import subprocess
import sys
import datetime

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))

if HERE not in sys.path:
    sys.path.insert(0, HERE)
import role_catalog as rc  # single source of truth: domain + expert role catalog (domain-agnostic)


def _emit_template():
    tpl = {
        "sow": "SOW1",
        "name": "Example SOW name",
        "methodology": "waterfall",
        "objective": "Objective extracted verbatim from SOW text",
        "scope": "in-scope (verbatim)",
        "out_of_scope": "out-of-scope (verbatim)",
        "assumptions": ["Assumption 1 (change trigger)", "Assumption 2"],
        "roles": ["ba", "solution-architect"],
        "entry_gates": [
            {"id": "SOW1.0", "name": "Entry condition / data readiness gate", "role": "ba",
             "duration_days": 10, "estimate": 8, "acceptance": "SME + real data + interface docs ready",
             "dependsOn": []}
        ],
        "waves": [
            {
                "id": "SOW1.W1", "name": "Wave 1",
                "billing": {"event": "Wave 1 Design Document post sign-off",
                            "fee": 11645092, "currency": "INR", "fee_type": "fixed"},
                "leaves": [
                    {"id": "SOW1.W1.1", "name": "Source analysis", "role": "ba",
                     "duration_days": 8, "estimate": 6, "acceptance": "Source interface docs ready"},
                    {"id": "SOW1.W1.2a", "name": "Logical model", "role": "solution-architect",
                     "duration_days": 8, "estimate": 6, "acceptance": "Logical ERD review passed"}
                ]
            }
        ],
        "deliverables_non_billing": [
            {"id": "SOW1.AR", "name": "Non-billing deliverable",
             "billing": {"event": "Deliverable sign-off", "fee": 0, "fee_type": "none"},
             "leaves": [
                 {"id": "SOW1.AR.1a", "name": "Design", "role": "solution-architect",
                  "duration_days": 9, "estimate": 7, "acceptance": "Design document review"}]}
        ]
    }
    print(json.dumps(tpl, ensure_ascii=False, indent=2))


def _default_methodology_chain(spec, byid):
    """Generate the default dependency chain for packages that do not specify dependsOn explicitly."""
    sow = spec['sow']
    gates = spec.get('entry_gates') or []
    gate_ids = [g['id'] for g in gates]
    first_prev = gate_ids[0] if gate_ids else None

    def chain_leaves(wid, leaves):
        # Leaf chain: leaf[i] dependsOn leaf[i-1]; the first leaf depends on its Wave summary.
        # Must write back into the real package in byid (when add_wave builds the package its
        # dependsOn is still empty), otherwise dependencies are lost.
        prev = wid
        for lf in leaves:
            pkg = byid.get(lf['id'])
            if pkg is None:
                continue
            deps = lf.get('dependsOn')
            if deps is None:
                deps = [prev]
            pkg['dependsOn'] = deps
            lf['dependsOn'] = deps  # sync spec for easier auditing
            prev = lf['id']
        return prev  # last leaf id

    # waves
    prev_wave_tail = first_prev
    wave_ms = []
    for w in spec.get('waves') or []:
        wp = byid[w['id']]
        if wp.get('dependsOn') is None:
            wp['dependsOn'] = [prev_wave_tail] if prev_wave_tail else []
        tail = chain_leaves(w['id'], w.get('leaves') or [])
        # milestone
        mid = w['id'] + '.M'
        m = byid.get(mid)
        if m is not None:
            if m.get('dependsOn') is None:
                m['dependsOn'] = [tail]
            wave_ms.append(mid)
        prev_wave_tail = mid if mid in byid else tail
    # non-billing deliverables
    for dl in spec.get('deliverables_non_billing') or []:
        dlp = byid[dl['id']]
        if dlp.get('dependsOn') is None:
            dlp['dependsOn'] = [first_prev] if first_prev else []
        tail = chain_leaves(dl['id'], dl.get('leaves') or [])
        mid = dl['id'] + '.M'
        m = byid.get(mid)
        if m is not None:
            if m.get('dependsOn') is None:
                m['dependsOn'] = [tail]


def build_packages(spec):
    """Return (packages list, sow_summary_id).
    Roles no longer default to the data domain: summary/wave default to solution-architect,
    leaves default to the SOW-inferred domain via role_catalog.infer_role, falling back to domain-sme.
    """
    sow = spec['sow']
    pkgs = []
    meth = spec.get('methodology', 'waterfall')
    # Auto-align domain + recommended roles from SOW extraction (domain-agnostic)
    aligned = rc.align_from_sow(spec)
    domain = aligned['domain']
    product = aligned['product']

    def P(id, name, **kw):
        o = {'id': id, 'name': name}
        o.update(kw)
        return o

    def role_or_default(role, name):
        # Explicit role takes priority; otherwise infer by domain; otherwise neutral fallback domain-sme
        r = rc.infer_role(name, domain, explicit_role=role)
        return r or 'domain-sme'

    # summary
    summary = P(sow, spec.get('name', sow),
                tier='program', summary=True, component='sow' + sow.replace('SOW', '').lower(),
                role=spec.get('summary_role') or 'solution-architect',
                domain=domain,
                objective=spec.get('objective', ''),
                scope=spec.get('scope', ''),
                out_of_scope=spec.get('out_of_scope', ''),
                assumptions=spec.get('assumptions', []),
                owner=spec.get('owner', 'SOW Project Manager'),
                methodology=meth,
                dependsOn=spec.get('dependsOn', []))
    pkgs.append(summary)

    byid = {}
    # entry gates
    _first_wave = (spec.get('waves') or [{}])[0]
    _first_mid = (_first_wave.get('id') + '.M') if _first_wave.get('id') else None
    for g in spec.get('entry_gates') or []:
        p = P(g['id'], g['name'], tier='component', component=summary.get('component'),
              role=g.get('role', 'ba'),
              domain=domain,
              duration=(str(g.get('duration_days', g.get('estimate', 0))) + 'd') if g.get('duration_days') or g.get('estimate') else None,
              estimate=g.get('estimate', 0),
              acceptance=g.get('acceptance', ''),
              owner=g.get('owner', ''),
              deliverable=g.get('deliverable'),
              scope=g.get('scope'),
              dependsOn=g.get('dependsOn', []),
              milestone_ref=g.get('milestone_ref', _first_mid))  # Pillar 2: entry gate belongs to first-wave milestone
        pkgs.append(p); byid[g['id']] = p

    def add_wave(w, is_billing=True, pay_index=None):
        billing = w.get('billing') or {}
        mid = w['id'] + '.M'  # Pillar 2: leaf milestone_ref target (must be defined before the leaf loop)
        p = P(w['id'], w['name'], tier='component', component=summary.get('component'),
              summary=True, role=w.get('role', 'solution-architect'),
              domain=domain,
              methodology=meth,
              objective=w.get('objective', ''),
              dependsOn=w.get('dependsOn'))  # filled by default chain when None
        pkgs.append(p); byid[w['id']] = p
        for lf in w.get('leaves') or []:
            lp = P(lf['id'], lf['name'], tier='component', component=summary.get('component'),
                   role=role_or_default(lf.get('role'), lf['name']),
                   domain=domain,
                   duration=(str(lf.get('duration_days', lf.get('estimate', 0))) + 'd') if (lf.get('duration_days') or lf.get('estimate')) else None,
                   estimate=lf.get('estimate', 0),
                   acceptance=lf.get('acceptance', ''),
                   owner=lf.get('owner', ''),
                   deliverable=lf.get('deliverable'),
                   scope=lf.get('scope'),
                   dependsOn=lf.get('dependsOn', []),
                   milestone_ref=mid)  # Pillar 2: each leaf belongs to its Wave milestone
            pkgs.append(lp); byid[lf['id']] = lp
        # milestone
        mid = w['id'] + '.M'
        pay_id = (f"{sow}-P{pay_index}" if (is_billing and pay_index) else None)
        mp = P(mid, (billing.get('event') or (w['name'] + ' sign-off')),
               tier='program', milestone=True, component=summary.get('component'),
               methodology=meth,
               billing={'event': billing.get('event'),
                        'fee_inr': billing.get('fee'),
                        'currency': billing.get('currency', 'INR'),
                        'fee_type': billing.get('fee_type', 'fixed'),
                        'payment_id': pay_id,  # Pillar 4: payment line <-> milestone mapping
                        'status': 'planned'},
               dependsOn=None)
        pkgs.append(mp); byid[mid] = mp

    for i, w in enumerate(spec.get('waves') or [], start=1):
        add_wave(w, True, pay_index=i)
    for dl in spec.get('deliverables_non_billing') or []:
        add_wave(dl, False, pay_index=None)

    _default_methodology_chain(spec, byid)

    # rollup estimates bottom-up
    children = {}
    for p in pkgs:
        did = p['id']
        for c in pkgs:
            cid = c['id']
            if cid.startswith(did + '.') and '.' not in cid[len(did) + 1:]:
                children.setdefault(did, []).append(cid)
    for p in sorted(pkgs, key=lambda x: -x['id'].count('.')):
        i = p['id']
        if i in children and children[i]:
            s = sum((byid[c].get('estimate') or 0) for c in children[i])
            if s:
                p['estimate'] = s
    # milestones: ensure small positive sign-off effort
    for p in pkgs:
        if p.get('milestone') and not p.get('estimate'):
            p['estimate'] = 2

    return pkgs, sow


def main():
    ap = argparse.ArgumentParser(description="PM Master · SOW/contract parser (spec -> WBS auto-write)")
    ap.add_argument('--project', help="program/project.yaml (single source of truth)")
    ap.add_argument('--spec', help="Comprehension record JSON (generated from text extraction + Q&A)")
    ap.add_argument('--emit-spec-template', action='store_true', help="Print a blank spec template")
    ap.add_argument('--dry-run', action='store_true', help="Only print the packages to be written, do not persist")
    ap.add_argument('--apply', action='store_true',
                    help="PERSIST: delete the old SOW subtree and write the new WBS to project.yaml "
                         "(a dated backup is written first). Required to modify project.yaml.")
    args = ap.parse_args()

    if args.emit_spec_template:
        _emit_template(); return

    if not args.project or not args.spec:
        ap.error("Provide --project and --spec (or --emit-spec-template)")

    spec = json.load(open(args.spec, encoding='utf-8'))
    pkgs, sow = build_packages(spec)

    # Compute the diff against the current project.yaml (read-only, no write yet)
    removed_count = 0
    if args.project and os.path.exists(args.project) and yaml is not None:
        d0 = yaml.safe_load(open(args.project, encoding='utf-8')) or {}
        wbs0 = d0.get('wbs') or []
        prefix = sow + '.'
        removed_count = len([w for w in wbs0
                             if w.get('id') == sow or str(w.get('id', '')).startswith(prefix)])

    if args.dry_run:
        print(json.dumps(pkgs, ensure_ascii=False, indent=2))
        print(f"[parse_sow] DRY RUN: {removed_count} existing package(s) for {sow} would be "
              f"replaced; {len(pkgs)} package(s) would be written. No changes made.",
              file=sys.stderr)
        return

    if not args.apply:
        # Safe default: neither --apply nor --dry-run -> preview only, no write.
        print(f"[parse_sow] SAFE PREVIEW (no changes written). This script defaults to a "
              f"non-destructive preview.\n"
              f"  - Re-run with --dry-run to print the {len(pkgs)} package(s) that would be written, or\n"
              f"  - Re-run with --apply to persist ({removed_count} existing package(s) for {sow} will\n"
              f"    be deleted and replaced; a dated backup of project.yaml is written first).",
              file=sys.stderr)
        return

    # ---- Persist (only reached with --apply) ----
    if yaml is None:
        print("ERROR: PyYAML is required to write project.yaml", file=sys.stderr); sys.exit(5)
    d = yaml.safe_load(open(args.project, encoding='utf-8'))
    wbs = d.get('wbs') or []
    prefix = sow + '.'
    wbs = [w for w in wbs if w.get('id') != sow and not str(w.get('id', '')).startswith(prefix)]
    wbs.extend(pkgs)
    d['wbs'] = wbs

    # update sow_map
    sm = d.get('sow_map') or []
    fee = 0
    for w in spec.get('waves') or []:
        fee += (w.get('billing') or {}).get('fee') or 0
    feetype = 'fixed' if any((w.get('billing') or {}).get('fee_type') == 'fixed' for w in spec.get('waves') or []) else ('tm' if any((w.get('billing') or {}).get('fee_type') == 'tm' for w in spec.get('waves') or []) else 'none')
    found = False
    for e in sm:
        if e.get('sow') == sow:
            e['fee'] = fee
            e['fee_type'] = feetype
            e['methodology'] = spec.get('methodology', e.get('methodology'))
            e['status'] = e.get('status', 'planning')
            found = True
    if not found:
        sm.append({'sow': sow, 'name': spec.get('name', sow), 'contract': 'C1',
                   'component': 'sow' + sow.replace('SOW', '').lower(),
                   'milestone': (spec.get('waves') or [{}])[0].get('billing', {}).get('event', ''),
                   'fee': fee, 'fee_type': feetype, 'methodology': spec.get('methodology', 'waterfall'),
                   'status': 'planning'})
    d['sow_map'] = sm

    # defensive backup (dated) before the destructive replacement
    import shutil
    shutil.copy(args.project, args.project + '.bak-' + datetime.date.today().isoformat())
    yaml.safe_dump(d, open(args.project, 'w', encoding='utf-8'), allow_unicode=True, sort_keys=False)
    print(f"[parse_sow] SOW {sow} WBS written to {args.project} ({len(pkgs)} packages added, "
          f"{removed_count} replaced, total fee {fee} "
          f"{((spec.get('waves') or [{}])[0].get('billing') or {}).get('currency','INR')})")

    # run consistency gate
    cc = os.path.join(HERE, 'consistency_check.py')
    if os.path.exists(cc):
        print("--- consistency_check ---")
        r = subprocess.run([sys.executable, cc, '--project', args.project])
        sys.exit(r.returncode)


if __name__ == '__main__':
    main()
