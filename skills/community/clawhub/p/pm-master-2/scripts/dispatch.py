#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Expert Dispatch Planner
-----------------------------------
Read project.yaml and audit every WBS work package:
  - Is it a domain activity but missing a role tag (should be produced by an expert)?
  - Is the granularity too coarse (estimate > granularity_threshold) -> needs expert decomposition?
Based on project.domain / project.product, specialize the role_id into a recommended expert
name, and output a "dispatch plan" (Markdown + JSON), where each item carries a brief that can
be handed directly to a sub-Agent.

The actual decomposition is done by the main controller dispatching domain-expert sub-Agents
per the plan (see references/expert-roles.md / activity-expert-map.md). This script only audits
and plans; it does not modify project.yaml.

Role/domain routing comes from `role_catalog.py` (single source of truth, domain-agnostic, with
auto-alignment from contract/SOW).
"""
import os
import sys
import json
import argparse

try:
    import yaml
except ImportError:
    yaml = None

# Single source of truth: domain + expert role catalog (domain-agnostic, auto-aligned from SOW/contract)
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import role_catalog as rc

PM_GENERALIST = rc.PM_GENERALIST


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def infer_role(row, name):
    """Take the explicit role first; otherwise infer by name keywords (domain-specific -> cross-domain -> neutral fallback)."""
    return rc.infer_role(name, row.get('domain'), explicit_role=row.get('role'))


def is_domain_activity(role, name, domain):
    return rc.is_domain_activity(role, name, domain)


def specialize(role, domain, product):
    return rc.specialize(role, domain, product)


def build_plan(data, threshold):
    proj = data.get('project', {}) or {}
    domain = proj.get('domain')
    product = proj.get('product') or proj.get('name')
    wbs = data.get('wbs') or []
    plan = []
    for w in wbs:
        name = w.get('name') or ''
        est = to_float(w.get('estimate'))
        role = infer_role(w, name)
        dom = w.get('domain')
        actions = []
        if role and role not in PM_GENERALIST and not w.get('role'):
            actions.append('tag_role')
        if est > threshold:
            actions.append('decompose')
        if is_domain_activity(role, name, dom) and not role:
            actions.append('dispatch_expert')
        if not actions:
            continue
        expert = specialize(role, domain, product)
        pid = w.get('id')
        # Idempotent: role already present and within threshold -> treat as resolved, mark done
        already_done = bool(w.get('role')) and est <= threshold and not (is_domain_activity(role, name, dom) and not role)
        if already_done:
            brief = (f"'{name}' already has role={role} and is within granularity ({est:g}<={threshold:g} person-days); "
                     f"no further dispatch needed; if further refinement is required, an expert can decompose incrementally.")
            plan.append({
                'id': pid, 'name': name, 'estimate': est,
                'domain': dom, 'role': role, 'expert': expert,
                'actions': ['done'], 'brief': brief,
            })
            continue
        brief = (f"Dispatch {expert or 'domain expert'}: decompose '{name}' (currently {est:g} person-days) into leaf "
                 f"work packages (each <= {threshold:g} person-days), including unique ID (prefix {pid}.x), deliverable, "
                 f"responsible-role, estimate, acceptance criteria (DoD), and dependencies (dependsOn); write back to "
                 f"the wbs list in project.yaml.")
        plan.append({
            'id': pid, 'name': name, 'estimate': est,
            'domain': dom, 'role': role, 'expert': expert,
            'actions': actions, 'brief': brief,
        })
    return plan, domain, product


def render_md(plan, domain, product, threshold):
    lines = []
    lines.append("# Expert Dispatch Plan")
    lines.append("")
    lines.append(f"> Specialized based on `project.domain={domain}` / `product={product}`; "
                 f"leaf-package threshold = {threshold:g} person-days.")
    lines.append("")
    if not plan:
        lines.append("✓ No dispatch needed: all WBS packages are role-tagged and within granularity.")
        return "\n".join(lines)
    # Group by role
    by_role = {}
    for it in plan:
        by_role.setdefault(it['role'] or 'unset', []).append(it)
    for role, items in by_role.items():
        lines.append(f"## Role: {role}")
        lines.append("")
        lines.append("| WBS ID | Name | Estimate (person-days) | Domain | Action | Recommended Expert |")
        lines.append("|--------|------|------------------------|--------|--------|--------------------|")
        for it in items:
            acts = ", ".join(it['actions'])
            lines.append(f"| {it['id']} | {it['name']} | {it['estimate']:g} | {it['domain'] or '—'} "
                         f"| {acts} | {it['expert'] or '—'} |")
        lines.append("")
        for it in items:
            lines.append(f"- **{it['id']} {it['name']}**: {it['brief']}")
        lines.append("")
    lines.append("---")
    lines.append("*Generated by `dispatch.py`; for the actual decomposition, dispatch a sub-Agent using the "
                 "system_prompt of the corresponding role in `expert-roles.md` (or route to the matching expert "
                 "installed in the WorkBuddy Expert Center).*")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="PM Master Expert Dispatch Plan generator")
    ap.add_argument('--project', required=True)
    ap.add_argument('--threshold', type=float, default=10.0,
                    help="Leaf-package person-day threshold; above this, decompose (default 10)")
    ap.add_argument('--out', default=None, help="Output Markdown plan path")
    ap.add_argument('--json', action='store_true', help="Output JSON only")
    a = ap.parse_args()

    data = load(a.project)
    ctrl = data.get('control') or {}
    threshold = float(ctrl.get('granularity_threshold') or a.threshold)
    plan, domain, product = build_plan(data, threshold)

    if a.json:
        print(json.dumps({'threshold': threshold, 'domain': domain, 'product': product,
                          'plan': plan}, ensure_ascii=False, indent=2))
        return

    md = render_md(plan, domain, product, threshold)
    pending = [p for p in plan if 'done' not in p['actions']]
    done = [p for p in plan if 'done' in p['actions']]
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"[dispatch] Plan written to {a.out} ({len(pending)} pending / {len(done)} already within granularity)")
    else:
        print(md)
    print(f"\nTotal {len(pending)} work packages need expert dispatch (threshold {threshold:g} person-days), "
          f"{len(done)} already within granularity and skippable.", file=sys.stderr)


if __name__ == '__main__':
    main()
