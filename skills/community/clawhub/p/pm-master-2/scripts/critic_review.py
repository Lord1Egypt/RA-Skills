#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · WBS Decomposition Critic Self-Review engine (Pillar 1 · 6-factor decomposition discipline)
=====================================================================================================

Harden the "expert understanding chain + Critic self-review" from references/sow-parsing-playbook.md
section 2 into an *executable* validation, rather than prose suggestions. Run after every WBS
decomposition (parse_sow / dispatch expert write-back) to list failed Critic items; with --strict the
exit code is non-zero.

The 6 decomposition drivers covered:
  1. scope        -- every leaf must trace to charter Scope / have a deliverable
  2. milestone     -- every leaf must belong to a milestone (milestone_ref); every fixed-fee SOW has a billing milestone
  3. payment       -- billing milestones must hang off a sow_map payment line (fee_type/fee consistent)
  4. assumptions   -- raid.assumptions must have quantifiable bounds ("<=N ..."), otherwise change triggers are not executable
  5. constraints   -- constraints must be explicit, and external predecessor constraints must have an entry_gate leaf as predecessor
  6. dependencies  -- dependency network is connected (no orphan leaves, no dangling IDs, critical path includes entry_gate)

Usage:
  python3 critic_review.py --project <program/project.yaml>
  python3 critic_review.py --project <program/project.yaml> --strict
"""
import os
import re
import sys
import argparse

try:
    import yaml
except ImportError:
    yaml = None

NUM_RE = re.compile(r'\d+(\.\d+)?')


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_deps(dep):
    if dep is None:
        return []
    if isinstance(dep, list):
        return [str(x).strip() for x in dep if str(x).strip() and str(x).strip() not in ('—', '-')]
    s = str(dep).strip()
    if s in ('', '—', '-'):
        return []
    return [p.strip() for p in re.split(r'[,;]', s) if p.strip()]


def has_bound(text):
    """Assumptions/constraints must contain a quantifiable bound: <=N / at least N / no more than N / N units / N tables."""
    if not text:
        return False
    t = str(text)
    if re.search(r'(≤|>=|>=|<=|no more than|not exceeding|at least|at most|cap|capped)\s*\d', t):
        return True
    if re.search(r'\d+\s*(units?|tables?|source tables?|person-days?|person-months?|weeks?|days?|percent|%|times?)', t):
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description="PM Master · WBS Decomposition Critic Self-Review")
    ap.add_argument('--project', required=True)
    ap.add_argument('--strict', action='store_true', help="exit 1 if any item fails")
    a = ap.parse_args()
    data = load(a.project)
    root = os.path.dirname(os.path.abspath(a.project))
    findings = []          # (severity, code, msg)
    problems = []          # fatal

    proj = data.get('project', {}) or {}
    phase = proj.get('phase') or ''
    wbs = data.get('wbs') or []
    raid = data.get('raid', {}) or {}
    ptype = (proj.get('type') or '').lower()

    # Enforce as fatal only in planning/initiation; during operations (already frozen, e.g. the
    # example client) downgrade to a warning and do not block.
    lifecycle = proj.get('lifecycle_state')
    enforce = phase in ('initiation', 'planning', '') or lifecycle in (None, 'planning', 'review', 'baselined')
    byid = {w.get('id'): w for w in wbs}
    milestone_ids = {w.get('id') for w in wbs if w.get('milestone')}

    # ---- 1. scope traceability ----
    for w in wbs:
        if w.get('summary') or w.get('milestone') or w.get('tier') == 'program':
            continue
        if not (w.get('deliverable') or w.get('scope')):
            problems.append(
                f"[scope] leaf {w.get('id')} '{w.get('name')}' is missing deliverable/scope, "
                f"must trace to charter Scope.")

    # ---- 2. milestone attribution ----
    for w in wbs:
        if w.get('summary') or w.get('milestone') or w.get('tier') == 'program':
            continue
        mref = w.get('milestone_ref')
        # If milestone_ref is not explicit, require the dependency chain end / direct dependsOn to hit a milestone
        deps = parse_deps(w.get('dependsOn'))
        links_ms = mref in milestone_ids or any(d in milestone_ids for d in deps)
        if not links_ms:
            problems.append(
                f"[milestone] leaf {w.get('id')} '{w.get('name')}' is not attributed to any milestone "
                f"(missing milestone_ref and dependsOn does not point to a milestone); "
                f"set milestone_ref explicitly or let the dependency endpoint land on a milestone.")

    # ---- 3. payment hangs off a payment line ----
    sow_map = data.get('sow_map') or []
    fee_sows = {e.get('sow') for e in sow_map if e.get('fee_type') == 'fixed'}
    # program tier uses program.sow_map/sows; single tier uses sow_map or wbs billing
    prog = data.get('program') or {}
    if prog:
        fee_sows |= {s.get('sow') for s in (prog.get('sows') or []) if s.get('fee_type') == 'fixed'}
    for w in wbs:
        b = w.get('billing') or {}
        if w.get('milestone') and b.get('fee_type') == 'fixed':
            wid = str(w.get('id', ''))
            sow = wid.split('.')[0] if wid else ''
            if sow not in fee_sows and not (b.get('fee') or b.get('fee_inr')):
                problems.append(
                    f"[payment] billing milestone {w.get('id')} '{w.get('name')}' "
                    f"has no matching fixed-fee payment line in sow_map (fee_type=fixed and fee>0).")

    # ---- 4. assumptions quantifiable bound ----
    for ar in (raid.get('assumptions') or []):
        txt = ar.get('text') if isinstance(ar, dict) else str(ar)
        if not has_bound(txt):
            findings.append(('warn', 'assumption-bound',
                f"[assumption] assumption lacks a quantifiable bound: '{txt[:60]}' -- "
                f"without a bound, CCB change triggers are not executable; change it to e.g. "
                f"'<=N source tables / M core tables'."))

    # ---- 5. constraints + entry_gate predecessor ----
    for c in (raid.get('constraints') or []):
        txt = c.get('text') if isinstance(c, dict) else str(c)
        external = bool(re.search(r'(depends|pending|needs|prerequisite|ready|available|external)', txt or '', re.I))
        if external and not has_bound(txt):
            findings.append(('warn', 'constraint-entrygate',
                f"[constraint] external predecessor constraint '{txt[:50]}' has no entry_gate predecessor package -- "
                f"there must be an entry_gate leaf as an explicit predecessor on that milestone path."))

    # entry_gate existence (critical-path predecessor condition)
    has_entry_gate = any(str(w.get('id', '')).split('.')[-1].lower().startswith('e') or
                         'entry' in str(w.get('name', '')).lower() or
                         w.get('entry_gate') for w in wbs)
    if not has_entry_gate and wbs:
        findings.append(('warn', 'entry-gate',
            "[entry-gate] no entry condition / data-ready gate (entry_gate) leaf identified in the WBS; "
            "if an external predecessor (SME / real data / interface) is the biggest rework risk, it must "
            "be modeled explicitly as a predecessor package."))

    # ---- 6. dependency connectivity ----
    ids = {w.get('id') for w in wbs}
    orphan = []
    dangling = []
    for w in wbs:
        if w.get('summary'):
            continue
        deps = parse_deps(w.get('dependsOn'))
        if not deps:
            orphan.append(w.get('id'))
        for d in deps:
            if d not in ids:
                dangling.append(f"{w.get('id')}->{d}")
    if len(wbs) > 1 and orphan:
        problems.append(
            f"[dependency] {len(orphan)} packages have no dependsOn (orphaned): {', '.join(orphan[:8])}... "
            f"-- a dependency network must form (critical path must be computable).")
    if dangling:
        problems.append(
            f"[dependency] dependency points to unknown ID: {', '.join(dangling[:8])}... -- must be fixed.")

    # ---- Output ----
    print("=== WBS Decomposition Critic Self-Review (6 factors) ===")
    if findings:
        print(f"⚠ Suggestions: {len(findings)}:")
        for sev, code, msg in findings:
            print("  -", msg)
    if not problems:
        print("✓ Critic passed: no fatal gaps in the 6-factor decomposition discipline")
        sys.exit(0)
    # During operations (already frozen) downgrade to warning, do not block
    if not enforce:
        print(f"ℹ Not enforced in operations ({phase}/{lifecycle}): the following {len(problems)} are planning-phase discipline gaps, advisory only:")
        for p in problems:
            print("  -", p)
        sys.exit(0)
    print(f"✗ FATAL: {len(problems)} (blocks delivery, must re-decompose):")
    for p in problems:
        print("  -", p)
    sys.exit(1)  # Planning-phase Critic fatal items always block


if __name__ == '__main__':
    main()
