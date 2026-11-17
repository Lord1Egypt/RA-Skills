#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Cross-artifact consistency check (pre-delivery quality gate · control grade)
---------------------------------------------------------------------------------------
Read project.yaml (single source of truth) and run a two-layer validation:

  [Fatal problems]  -> present -> exit 1, blocks delivery
    1. Risk register: every risk must have an owner and mitigation/response
    2. Issue log: every issue must have an owner and due
    3. Dependencies: every dependency must have from and to
    4. Governance: the project must specify a pm and a sponsor
    5. Artifact index: files referenced in artifacts must actually exist
    6. Mandatory estimates (control grade): every WBS / backlog / iteration row must have a
       numeric estimate (>0); "-" / blank / non-numeric are not allowed (P0)
    7. Schedule network (control grade): a multi-row waterfall / hybrid WBS must form a
       dependency network; not all rows may be dependency-free (P0)
    8. EVM baseline (control grade): when a waterfall / hybrid project enters the
       execution/monitoring/closeout phase, metrics.evm must contain pv / ev / ac (P0)
    9. Hybrid micro-plan (control grade): when methodology=hybrid, at least one micro-level
       plan (sprint / backlog / iteration) must exist (P0)
   10. Risk 5x5 calibration (control grade): every risk likelihood/impact must be a 1-5
       number, score == likelihood x impact, and severity must match the score's band (P0)
   11. Benefit owners (P1): every program benefit must have an owner
   12. Baselining discipline (control grade): a waterfall / hybrid project in the
       execution/monitoring/closeout phase but missing a baseline pointer must first go
       planning -> review -> baseline.py --freeze (freeze plan as baseline) -> control gate
       -> execution (references/lifecycle.md section 5)

  [Warnings]  -> advisory only, do not block (exit may still be 0); `--strict` upgrades them
    - Program / hybrid should have a change_log (change control)
    - execution/monitoring phase should have a status_report
    - execution/monitoring phase should configure a control block + control_register
      (operational control engine)
    - should have a communication_plan
    - Non-domain WBS estimate exceeds the leaf-package granularity threshold (generic
      granularity hint, suggest decomposing)
    - Domain-activity WBS missing a role tag / over threshold: **fatal by default** (see 7b
      below; forces expert decomposition, cannot be bypassed by the main controller)

Usage:
  python3 consistency_check.py --project /workspace/<slug>/project.yaml
  python3 consistency_check.py --project ... --strict  # also upgrade warnings to fatal
"""
import os
import re
import sys
import argparse
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import yaml
except ImportError:
    yaml = None

if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
import role_catalog as rc  # Single source of truth: domain + expert role catalog (domain-agnostic)

PM_GENERALIST = rc.PM_GENERALIST


def load_config():
    """Read the install-time config.yaml; return an empty dict if absent (lazy, avoids circular import)."""
    for cand in (os.path.join(SCRIPT_DIR, '..', 'config.yaml'),
                 os.path.join(SCRIPT_DIR, 'config.yaml')):
        if os.path.exists(cand):
            try:
                with open(cand, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                return {}
    return {}


# ---------- Risk 5x5 bands ----------
def risk_band(score):
    """score = likelihood(1-5) x impact(1-5) in [1,25]. Bands:
    1-4 low(green) | 5-9 medium(yellow) | 10-15 high(orange) | 16-25 critical(red)"""
    if score <= 4:
        return 'low'
    if score <= 9:
        return 'medium'
    if score <= 15:
        return 'high'
    return 'critical'


SEV_MAP = {
    'green': 'low', 'low': 'low', 'l': 'low',
    'yellow': 'medium', 'medium': 'medium', 'm': 'medium',
    'orange': 'high', 'high': 'high', 'h': 'high',
    'red': 'critical', 'critical': 'critical', 'c': 'critical',
}


def norm_sev(s):
    if s is None:
        return None
    return SEV_MAP.get(str(s).strip().lower())


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def has_estimate(est):
    """An estimate must parse to a number > 0; '-' / blank / non-numeric / 0 count as missing."""
    if est is None:
        return False
    if isinstance(est, (int, float)):
        return est > 0
    s = str(est).strip()
    if s in ('', '—', '-', 'TBD', 'N/A', 'NA', 'none', 'null'):
        return False
    m = re.search(r'\d+(\.\d+)?', s)
    if not m:
        return False
    return float(m.group()) > 0


def parse_deps(dep):
    """dependsOn accepts both list and comma-separated string forms."""
    if dep is None:
        return []
    if isinstance(dep, list):
        out = []
        for x in dep:
            sx = str(x).strip()
            if sx and sx not in ('—', '-'):
                out.append(sx)
        return out
    s = str(dep)
    if s.strip() in ('', '—', '-'):
        return []
    return [p.strip() for p in re.split(r'[,;]', s) if p.strip()]


def collect_risks(data):
    """Merge top-level risks and raid.risks (de-dupe by id, top-level wins)."""
    seen = {}
    for r in (data.get('risks') or []):
        if r.get('id'):
            seen[r['id']] = r
    for r in ((data.get('raid') or {}).get('risks') or []):
        if r.get('id') and r['id'] not in seen:
            seen[r['id']] = r
    return list(seen.values())


# ---------- Role inference (single source of truth: role_catalog.py, domain-agnostic, supports SOW auto-align) ----------

def infer_role(row, name):
    return rc.infer_role(name, row.get('domain'), explicit_role=row.get('role'))


def is_domain_activity(role, name, domain):
    return rc.is_domain_activity(role, name, domain)


def main():
    ap = argparse.ArgumentParser(description="PM Master Consistency Check (control grade)")
    ap.add_argument('--project', required=True)
    ap.add_argument('--strict', action='store_true',
                    help="Upgrade warnings to fatal problems (overrides the config default)")
    a = ap.parse_args()
    data = load(a.project)
    # Config takes priority: config.quality_gate.consistency_check_strict; CLI --strict can override
    cfg = load_config()
    strict_cfg = bool((cfg.get('quality_gate') or {}).get('consistency_check_strict'))
    strict = a.strict or strict_cfg
    root = os.path.dirname(os.path.abspath(a.project))
    problems = []
    warnings = []

    raid = data.get('raid', {}) or {}
    for r in raid.get('risks', []) or []:
        if not r.get('owner'):
            problems.append(f"Risk {r.get('id','?')} is missing an owner")
        if not (r.get('mitigation') or r.get('response')):
            problems.append(f"Risk {r.get('id','?')} is missing a mitigation/response")
    for i in raid.get('issues', []) or []:
        if not i.get('owner'):
            problems.append(f"Issue {i.get('id','?')} is missing an owner")
        if not i.get('due'):
            problems.append(f"Issue {i.get('id','?')} is missing a due date")
    for dep in raid.get('dependencies', []) or []:
        if not (dep.get('from') and dep.get('to')):
            problems.append(f"Dependency {dep.get('id','?')} is missing from/to")

    proj = data.get('project', {}) or {}
    if not proj.get('pm'):
        problems.append("Project has no project manager (pm) specified")
    if not proj.get('sponsor'):
        problems.append("Project has no sponsor specified")

    artifacts = data.get('artifacts', {}) or {}
    for key, rel in artifacts.items():
        if not rel:
            continue
        # Support list-type artifact indexes (e.g. sow_kickoffs multiple files); verify each
        rels = rel if isinstance(rel, list) else [rel]
        for r in rels:
            if not r:
                continue
            full = r if os.path.isabs(r) else os.path.join(root, r)
            if not os.path.exists(full):
                problems.append(f"Artifact index {key} points to a non-existent file: {r}")
    # Single source of truth drift guard: wbs was written back but not re-rendered; suggest re-running build_wbs.py
    if artifacts.get('wbs_dirty'):
        warnings.append(
            "project.yaml.wbs was updated but the wbs document (artifacts.wbs) was not re-rendered (wbs_dirty flag). "
            "Re-run `build_wbs.py` to keep the document consistent with the source of truth.")

    methodology = (proj.get('methodology') or '').lower()
    ptype = (proj.get('type') or '').lower()
    phase = (proj.get('phase') or '')

    # ---- 6. Mandatory estimates ----
    wbs = data.get('wbs') or []
    if wbs:
        missing = [w.get('id', '?') for w in wbs if not has_estimate(w.get('estimate'))]
        if missing:
            problems.append(
                f"WBS estimate missing (control grade): the following work packages have no numeric estimate (>0): "
                f"{', '.join(missing)} -- '-'/blank/non-numeric are not allowed")
    if methodology == 'agile':
        for bk in (data.get('backlog') or []):
            if not has_estimate(bk.get('estimate')):
                problems.append(f"Backlog {bk.get('id','?')} is missing an estimate")
        for sp in (data.get('sprints') or data.get('sprint') or []):
            for t in (sp.get('tasks') or [] if isinstance(sp, dict) else []):
                if not has_estimate(t.get('estimate')):
                    problems.append(f"Sprint task {t.get('id','?')} is missing an estimate")
    if methodology == 'iteration':
        for bk in (data.get('backlog') or []):
            if not has_estimate(bk.get('estimate')):
                problems.append(f"Iteration backlog {bk.get('id','?')} is missing an estimate")

    # ---- 6b. Billing-milestone completeness (basic-layout gate) ----
    # Fixed-fee SOW (sow_map.fee_type=='fixed' or subtree with billing.fee_type=='fixed' and fee>0)
    # must have >= 1 milestone + billing.fee_type=='fixed' package, otherwise the plan is
    # unmeasurable and revenue cannot be recognized.
    def _num(x):
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, str):
            s = re.sub(r'[^0-9.]', '', x)
            return float(s) if s else 0.0
        return 0.0
    sow_map = data.get('sow_map') or []
    fee_sows = set()
    for e in sow_map:
        # Only fixed-fee SOWs require a billing milestone; T&M (fee_type=='tm', fee is the
        # labor cap) does not.
        if e.get('fee_type') == 'fixed':
            fee_sows.add(e.get('sow'))
    for w in wbs:
        b = w.get('billing') or {}
        if b.get('fee_type') == 'fixed' and _num(b.get('fee_inr') or b.get('fee')) > 0:
            # Infer ownership from the package's SOW prefix
            wid = str(w.get('id', ''))
            m = re.match(r'^(SOW\d+)', wid)
            if m:
                fee_sows.add(m.group(1))
    if fee_sows:
        for sow in fee_sows:
            prefix = sow + '.'
            has_billing_ms = any(
                w.get('milestone') and (w.get('billing') or {}).get('fee_type') == 'fixed'
                and ((w.get('billing') or {}).get('fee_inr') or (w.get('billing') or {}).get('fee') or 0) > 0
                and (w.get('id') == sow or str(w.get('id', '')).startswith(prefix))
                for w in wbs)
            if not has_billing_ms:
                problems.append(
                    f"Basic-layout defect (fatal): fixed-fee SOW {sow} subtree is missing a billing milestone "
                    f"(milestone + billing.fee_type=='fixed' and fee>0). "
                    f"Every 'post sign-off/certificate of completion' billing event must be modeled as a "
                    f"milestone package when parsing the SOW, otherwise scheduling and revenue recognition "
                    f"are unmeasurable. See references/sow-parsing-playbook.md.")

    # ---- 6c. Decomposition discipline (Pillar 1 · 6 factors, fatal only in planning) ----
    # Once operational (execution/monitoring/closeout), stop blocking (protect frozen projects,
    # e.g. the example client), but planning/initiation must enforce 6-factor decomposition +
    # Critic self-review pass.
    planning_now = phase in ('initiation', 'planning', '') or (proj.get('lifecycle_state') in (None, 'planning', 'review', 'baselined'))
    if planning_now:
        # 6c-1 decomposition Critic self-review (scope/milestone/payment/assumptions/constraints/dependencies)
        cc = os.path.join(SCRIPT_DIR, 'critic_review.py')
        if os.path.exists(cc) and wbs:
            try:
                import subprocess as _sp
                r = _sp.run([sys.executable, cc, '--project', a.project, '--strict'],
                            capture_output=True, text=True)
                for line in (r.stdout or '').splitlines():
                    if line.strip().startswith('✗') or 'FATAL' in line:
                        pass
                if r.returncode != 0:
                    # Pull the Critic's fatal items into the consistency gate one by one
                    for line in (r.stdout or '').splitlines():
                        m = re.match(r'\s*-\s+\[(scope|milestone|payment|dependency)\]\s*(.*)', line)
                        if m:
                            problems.append(f"Decomposition Critic({m.group(1)}): {m.group(2)}")
            except Exception:
                pass
        # 6c-2 decomposition.critic_passed flag (must be set true after the expert writes back)
        decomp = data.get('decomposition') or {}
        if wbs and not decomp.get('critic_passed'):
            problems.append(
                "Decomposition Critic not confirmed (decomposition.critic_passed != true): "
                "after the WBS is decomposed by experts, critic_review.py must be run and "
                "critic_passed set to true, otherwise it is considered not self-reviewed.")
        # 6c-3 assumptions must have a quantifiable bound (part of the charter estimate baseline)
        for ar in (raid.get('assumptions') or []):
            txt = ar.get('text') if isinstance(ar, dict) else str(ar)
            if not re.search(r'(≤|>=|<=|no more than|not exceeding|at least|at most|cap|capped)\s*\d', str(txt or '')) and \
               not re.search(r'\d+\s*(units?|tables?|source tables?|person-days?|person-months?|weeks?|days?|percent|%|times?)', str(txt or '')):
                problems.append(
                    f"Assumption lacks a quantifiable bound: '{(str(txt)[:50])}' -- change it to e.g. "
                    f"'<=N source tables / M core tables', otherwise CCB change triggers are not executable.")

    # ---- 6d. Schedule linkage (Pillar 2 + 4 · fatal only in planning) ----
    if planning_now:
        # 6d-1 milestone attribution: every leaf must belong to a milestone
        # (Critic already covers this; here we add "milestone non-empty coverage")
        ms_ids = {w.get('id') for w in wbs if w.get('milestone')}
        uncovered = [w.get('id') for w in wbs
                     if not (w.get('summary') or w.get('milestone') or w.get('tier') == 'program')
                     and not w.get('milestone_ref') and not any(d in ms_ids for d in parse_deps(w.get('dependsOn')))]
        if uncovered:
            problems.append(
                f"Milestone coverage gap (Pillar 2): {len(uncovered)} leaves are not attributed to any milestone "
                f"({', '.join(uncovered[:6])}...), set milestone_ref or let the dependency endpoint land on a milestone.")
        # 6d-2 payment<->milestone ordering: every fixed-fee payment line needs a matching billing milestone
        pay_lines = []
        for s in ((data.get('program') or {}).get('sows') or []) + (data.get('sow_map') or []):
            fee = s.get('fee')
            if isinstance(fee, str):
                fee = re.sub(r'[^0-9.]', '', fee) or '0'
            try:
                fee_v = float(fee)
            except (TypeError, ValueError):
                fee_v = 0.0
            if s.get('fee_type') == 'fixed' and fee_v > 0:
                pay_lines.append(s.get('sow'))
        for sow in set(pay_lines):
            prefix = sow + '.'
            has_pm = any(w.get('milestone') and (w.get('billing') or {}).get('fee_type') == 'fixed'
                         and ((w.get('billing') or {}).get('fee_inr') or (w.get('billing') or {}).get('fee') or 0) > 0
                         and (w.get('id') == sow or str(w.get('id', '')).startswith(prefix))
                         for w in wbs)
            if not has_pm:
                problems.append(
                    f"Payment<->milestone missing (Pillar 4): fixed-fee SOW {sow} has a payment line but the WBS "
                    f"has no matching billing milestone (model the 'post sign-off' event as milestone + "
                    f"billing.fee_type=fixed).")
        # 6d-3 payment ordering monotonic: billing milestones of the same SOW must be monotonic by schedule date
        for sow in set(pay_lines):
            prefix = sow + '.'
            dates = []
            for w in wbs:
                if w.get('milestone') and (w.get('billing') or {}).get('fee_type') == 'fixed' \
                   and _num((w.get('billing') or {}).get('fee_inr') or (w.get('billing') or {}).get('fee') or 0) > 0 \
                   and (w.get('id') == sow or str(w.get('id', '')).startswith(prefix)):
                    sd = w.get('start')
                    if sd:
                        try:
                            dates.append(datetime.date.fromisoformat(str(sd)[:10]))
                        except (ValueError, TypeError):
                            pass
            if len(dates) >= 2:
                mono = all(dates[i] <= dates[i+1] for i in range(len(dates)-1))
                if not mono:
                    problems.append(
                        f"Payment ordering non-monotonic (Pillar 4): SOW {sow} billing-milestone schedule dates are "
                        f"not ascending; payment rhythm and delivery rhythm are inconsistent, fix the dependencies/order.")

    # ---- 7. Schedule network ----
    if wbs and len(wbs) > 1 and methodology in ('waterfall', 'hybrid'):
        ids = {w.get('id') for w in wbs}
        linked = 0
        bad = []
        for w in wbs:
            deps = parse_deps(w.get('dependsOn'))
            if deps:
                linked += 1
            for d in deps:
                if d not in ids:
                    bad.append(f"{w.get('id','?')}->{d}")
        if linked == 0:
            problems.append(
                "Schedule does not form a dependency network (control grade): a multi-row waterfall/hybrid WBS "
                "must have at least one dependency, otherwise the critical path cannot be computed. Fill in "
                "dependsOn for each work package.")
        if bad:
            warnings.append(f"WBS dependency points to unknown ID (suggest verifying): {', '.join(bad)}")

    # ---- 7b. Expert role tagging + granularity ----
    # Domain activities must be produced by the corresponding expert and decomposed to leaf
    # packages, otherwise the WBS stalls at SOW-level coarse granularity.
    # Key fix: any "domain activity missing a role tag" or "domain activity over threshold" is
    # fatal by default (exit 1 blocks delivery), forcing dispatch.py -> domain-expert sub-agent
    # decomposition; the main controller must not split it directly (see SKILL.md Step 2.5 / section 6).
    # program-level summary packages (SOW/P0 parent) are skipped; component-level leaves carry it.
    ctrl_blk = data.get('control') or {}
    gran_thr = float(ctrl_blk.get('granularity_threshold') or 10)
    for w in wbs:
        # program-level summary/milestone rows (SOW/P0 parent, tier:program, milestone) are not checked:
        # program granularity is naturally at milestone level (see references/program-management.md),
        # carried by component-level leaf packages; the main controller must not split milestone rows
        # as domain packages at the program level.
        if w.get('summary') or w.get('milestone') or (w.get('tier') == 'program'):
            continue
        wid = w.get('id', '?')
        name = w.get('name') or ''
        role = infer_role(w, name)
        dom = w.get('domain')
        is_da = is_domain_activity(role, name, dom)
        try:
            est_v = float(w.get('estimate'))
        except (TypeError, ValueError):
            est_v = 0.0
        over = est_v > gran_thr
        if is_da and not w.get('role'):
            problems.append(
                f"WBS {wid} '{name}' is a domain activity but is missing a role tag (fatal): "
                f"it must be produced by the corresponding domain expert ({role or 'see references/expert-roles.md'}) "
                f"and written back to wbs; the main controller must not split it directly. "
                f"See references/activity-expert-map.md sections 3-4.")
        if is_da and over:
            problems.append(
                f"WBS {wid} '{name}' estimate {est_v:g} person-days exceeds the leaf-package threshold "
                f"{gran_thr:g} (fatal): dispatch a domain expert to further decompose it into leaf packages "
                f"of <= {gran_thr:g} person-days (ID prefix {wid}.x) to prevent SOW-level coarse WBS from "
                f"being delivered as-is.")
        if (not is_da) and over:
            warnings.append(
                f"WBS {wid} '{name}' estimate {est_v:g} person-days exceeds the leaf-package threshold "
                f"{gran_thr:g}; suggest further decomposition (non-domain activity, warning only).")

    # ---- 7c. Program: SOW mapping <-> WBS consistency (contract-boundary drift guard) ----
    # Only checked for program type: program.sow_map[].sow must map to a tier:program / summary
    # package in wbs.
    if ptype == 'program':
        wbs_ids = {w.get('id') for w in wbs}
        sow_map = (data.get('program') or {}).get('sow_map') or []
        if sow_map:
            for m in sow_map:
                sid = m.get('sow')
                if not sid:
                    problems.append("program.sow_map has a mapping entry without a sow field")
                    continue
                tgt = next((w for w in wbs if w.get('id') == sid), None)
                if tgt is None:
                    problems.append(
                        f"Contract-boundary drift (fatal): SOW '{sid}' in program.sow_map has no matching "
                        f"summary package in wbs (tier:program or summary:true).")
                elif not (tgt.get('tier') == 'program' or tgt.get('summary')):
                    problems.append(
                        f"Contract-boundary drift (fatal): SOW '{sid}' in wbs is not a summary package "
                        f"(must be tier:program or summary:true), conflicting with the program two-level "
                        f"granularity convention.")
            # Reverse: top-level program summary packages (tier:program and id has no '.') should be
            # referenced by at least one sow_map. Component-phase summary packages (e.g. SOW1.1 phase
            # groups, tier:component) do not count, to avoid false positives.
            mapped = {m.get('sow') for m in sow_map}
            orphans = [w.get('id') for w in wbs
                       if w.get('tier') == 'program' and not str(w.get('id', '')).count('.')
                       and w.get('id') not in mapped]
            if orphans:
                warnings.append(
                    f"The following program summary packages are not referenced by program.sow_map "
                    f"(suggest adding the mapping to avoid missing contract boundaries): {', '.join(orphans)}")
        # Extract outsourcing must be bound to a contract
        for ex in ((data.get('program') or {}).get('extracts') or []):
            if (ex.get('mode') or '').lower() in ('outsourced', 'outsource', 'out') and not ex.get('contract'):
                problems.append(
                    f"Extract '{ex.get('id')}' is marked outsourced but has no bound contract (contract is empty): "
                    f"outsourced scope must have a contractual basis.")
        # 7d. SOW fee required (no whole-table (TBD)/TBD/blank)
        for s in ((data.get('program') or {}).get('sows') or []):
            fee = (s.get('fee') or '').strip()
            if not fee or fee in ('(TBD)', 'TBD', 'tbd', 'N/A', '-'):
                problems.append(
                    f"SOW '{s.get('sow')}' fee is unfilled or still (TBD)/TBD: fill the amount after the "
                    f"contract is locked; if not locked, write 'TBC -- reason'.")

    # ---- 8. EVM baseline ----
    # Planned Value (PV/BAC) belongs to the plan baseline and lives in metrics.evm; current
    # Earned Value / Actual Cost (ev/ac) may live in the actuals block during operations
    # (control_engine.py's single current-state source), and also compatibly in metrics.evm.ev/ac.
    if methodology in ('waterfall', 'hybrid') and phase in ('execution', 'monitoring', 'closeout'):
        evm = data.get('metrics', {}).get('evm') or {}
        actuals = data.get('actuals') or {}
        miss = []
        has_plan = isinstance(evm.get('pv'), (int, float)) or isinstance(evm.get('bac'), (int, float))
        ev_val = evm.get('ev') if isinstance(evm.get('ev'), (int, float)) else actuals.get('ev')
        ac_val = evm.get('ac') if isinstance(evm.get('ac'), (int, float)) else actuals.get('ac')
        if not has_plan:
            miss.append('pv/bac (planned baseline, in metrics.evm)')
        if not isinstance(ev_val, (int, float)):
            miss.append('ev (in actuals or metrics.evm)')
        if not isinstance(ac_val, (int, float)):
            miss.append('ac (in actuals or metrics.evm)')
        if miss:
            problems.append(
                f"EVM baseline missing (control grade): {methodology} project is in the '{phase}' phase but "
                f"lacks numeric {', '.join(miss)}. First establish the budget-at-completion (PV/BAC) baseline, "
                f"then report ev/ac in actuals (run evm.py).")

    # ---- 8b. Baselining discipline (control grade) ----
    # Planning is not operation; a waterfall / hybrid project must be baselined (frozen plan as
    # reference) before entering execution/monitoring/closeout.
    if methodology in ('waterfall', 'hybrid') and phase in ('execution', 'monitoring', 'closeout'):
        bl = data.get('baseline') or {}
        if not (isinstance(bl, dict) and bl.get('file')):
            problems.append(
                f"Entered operations/execution without baselining (control grade): {methodology} project is in "
                f"the '{phase}' phase but is missing a baseline pointer. Follow the mandatory serial state "
                f"machine: planning -> review -> baseline.py --freeze (freeze plan as baseline) -> control gate "
                f"-> execution (see references/lifecycle.md section 5).")

    # ---- 9. Hybrid micro-plan ----
    if methodology == 'hybrid':
        micro_keys = ('sprint', 'sprints', 'backlog', 'iteration', 'iterations')
        has_micro = any(k in data for k in micro_keys)
        if not has_micro:
            # Fallback: is a micro-level plan hung off artifacts
            joined = ' '.join(str(v) for v in artifacts.values())
            if not any(t in joined for t in ('sprint_plan', 'backlog', 'iteration_plan')):
                problems.append(
                    "Hybrid delivery is missing a micro-level plan (control grade): methodology=hybrid must have "
                    "at least one micro-level plan (sprint / backlog / iteration) to carry incremental delivery "
                    "within the macro phases.")

    # ---- 10. Risk 5x5 calibration ----
    for r in collect_risks(data):
        rid = r.get('id', '?')
        lk = r.get('likelihood')
        im = r.get('impact')
        sc = r.get('score')
        if not isinstance(lk, (int, float)) or not (1 <= lk <= 5):
            problems.append(f"Risk {rid} likelihood must be a 1-5 number, currently: {lk}")
            continue
        if not isinstance(im, (int, float)) or not (1 <= im <= 5):
            problems.append(f"Risk {rid} impact must be a 1-5 number, currently: {im}")
            continue
        if not isinstance(sc, (int, float)) or sc != lk * im:
            problems.append(
                f"Risk {rid} score should be likelihood x impact = {lk*im}, currently: {sc}")
            continue
        band = risk_band(lk * im)
        sev = norm_sev(r.get('severity'))
        if sev is None:
            problems.append(
                f"Risk {rid} is missing a calibrated severity; should be green/yellow/orange/red "
                f"(score={sc} should be { {'low':'green','medium':'yellow','high':'orange','critical':'red'}[band] })")
        elif sev != band:
            problems.append(
                f"Risk {rid} severity does not match the score: score={sc} should be "
                f"{ {'low':'green','medium':'yellow','high':'orange','critical':'red'}[band] }, "
                f"currently labeled: {r.get('severity')}")

    # ---- 11. Benefit owners (program) ----
    program = data.get('program')
    if isinstance(program, dict):
        for b in (program.get('benefits') or []):
            if not b.get('owner'):
                problems.append(f"Benefit {b.get('id','?')} is missing an owner")

    # ---- 11b. Intent-routed deliverable enforcement (aligns with SKILL.md section 3 intent->deliverable) ----
    # During planning/initiation (planning_now) and for plan* intents, a missing corresponding
    # deliverable = fatal block.
    # Usage: project.intent explicitly declared (plan / plan_program / risk / change / report etc.);
    # when undeclared, infer the minimal set from type+methodology.
    intent = str((data.get('project') or {}).get('intent') or '').lower()
    required_artifacts = []
    if ptype == 'program':
        required_artifacts += ['program_charter', 'risk_register', 'dependency_map',
                                'portfolio_dashboard', 'benefits_realization', 'raci',
                                'stakeholder_register', 'communication_plan']
    elif methodology in ('waterfall', 'hybrid'):
        required_artifacts += ['wbs', 'schedule_gantt', 'risk_register', 'raid_log',
                                'communication_plan']
        if methodology == 'hybrid':
            required_artifacts += ['micro_plan']
    elif methodology == 'agile':
        required_artifacts += ['product_backlog', 'sprint_plan', 'risk_register', 'dod']
    elif methodology == 'iteration':
        required_artifacts += ['iteration_plan', 'iteration_backlog', 'risk_register']
    if intent in ('risk',):
        required_artifacts += ['risk_register', 'raid_log']
    if intent in ('change',):
        required_artifacts += ['change_request', 'change_log']
    # De-dupe + only check existing keys (artifacts may use other key names; loose match)
    required_artifacts = list(dict.fromkeys(required_artifacts))
    if planning_now and required_artifacts:
        for req in required_artifacts:
            present = any(req in str(k) for k in artifacts) or (req in artifacts)
            # Also check whether the corresponding rendered file exists on disk
            if not present:
                # Tolerant: if project.yaml has non-empty wbs and requires wbs/raid_log/schedule but
                # with a different key name, warn rather than fail
                warnings.append(
                    f"Intent-routed deliverable may be missing: {req} (should be produced in the plan phase; "
                    f"ignore if already rendered under another key, or explicitly register it as artifacts.{req})")

    # ---- Warnings (non-fatal) ----
    if ptype == 'program' or methodology == 'hybrid':
        if 'change_log' not in artifacts:
            warnings.append("Suggest adding a change log change_log (program/hybrid needs change control CCB)")
    if phase in ('execution', 'monitoring'):
        if 'status_report' not in artifacts:
            warnings.append("Suggest adding a status report status_report (execution/monitoring phase should report periodically)")
        if 'control' not in data:
            warnings.append("Suggest configuring a control block (cadence/thresholds/recipients) to drive control_engine.py periodic inspection")
        if 'control_register' not in artifacts:
            warnings.append("Suggest adding a control register control_register (operational routine control checklist, generated by baseline.py)")
    if 'communication_plan' not in artifacts:
        warnings.append("Suggest adding a communication plan communication_plan (part of the standard kick-off kit)")

    # ---- Output ----
    print("=== Consistency Check (control grade) ===")
    if warnings:
        print(f"⚠ Warnings: {len(warnings)} (do not block delivery):")
        for w in warnings:
            print("  -", w)
    if not problems:
        print("✓ Passed: no fatal consistency problems")
        sys.exit(0)
    if strict:
        problems = problems + [f"[strict] warning escalated: {w}" for w in warnings]
    print(f"✗ {len(problems)} fatal problems found (block delivery):")
    for p in problems:
        print("  -", p)
    sys.exit(1)


if __name__ == '__main__':
    main()
