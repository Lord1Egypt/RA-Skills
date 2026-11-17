#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master - Phase Gate Engine
==============================

Reads project.yaml (single source of truth) and, following the
"phase (label) <-> lifecycle_state (state machine)" model, validates the
**Entry Criteria** required to enter a target phase. After an authorized
approval it flips project.phase and lifecycle_state, writes a stage-gate
record to governance.stage_gates, and emits a stage-gate review report (Markdown).

Hard gates reuse existing engines to avoid logic duplication:
  - Before entering execution/monitoring (operational): consistency_check.py must exit 0
  - Before entering closeout (closed): control_engine.py must exit 0

Phase gates (aligned with references/phases/* and lifecycle.md sec.5/6):
  G0->1  Initiation -> Planning   (light gate, sets phase only)
  G1->2  Planning   -> Execution  (control gate: serial; baseline + consistency exit 0; sponsor approves)
  G2->3  Execution  -> Monitoring (soft gate: parallel within operational; PM marks monitoring cadence)
  G3->4  Monitoring -> Closeout   (closeout gate: control_engine exit 0 + acceptance/lessons/benefits; sponsor approves)

Usage:
  # Evaluate whether we can enter "execution" (dry-run, no state change)
  python3 gate_engine.py --project /workspace/<slug>/project.yaml --to execution

  # Evaluate closeout and list gaps
  python3 gate_engine.py --project /workspace/<slug>/project.yaml --to closeout

  # Authorized approval: flip state + record gate + produce report
  python3 gate_engine.py --project /workspace/<slug>/project.yaml --to execution \
      --approve "lisi(sponsor)" --requester "agent"

  # View current state and available gates only
  python3 gate_engine.py --project /workspace/<slug>/project.yaml --status
"""
import os
import re
import sys
import argparse
import subprocess
import datetime
import uuid

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------- Phase / state-machine model (English only) ----------
PROJECT_PHASES = ['initiation', 'planning', 'execution', 'monitoring', 'closeout']
PROGRAM_PHASES = ['program-definition', 'program-delivery', 'program-closeout']

# Normalize --to input tokens to internal English phase keys.
PHASE_ALIASES = {
    'initiation': 'initiation', 'initiate': 'initiation', 'init': 'initiation',
    'planning': 'planning', 'plan': 'planning',
    'execution': 'execution', 'execute': 'execution', 'exec': 'execution',
    'monitoring': 'monitoring', 'monitor': 'monitoring', 'control': 'monitoring',
    'closeout': 'closeout', 'closure': 'closeout', 'close': 'closeout',
    'program-definition': 'program-definition', 'program_definition': 'program-definition',
    'portfolio-definition': 'program-definition',
    'program-delivery': 'program-delivery', 'program_delivery': 'program-delivery',
    'portfolio-delivery': 'program-delivery',
    'program-closeout': 'program-closeout', 'program_closeout': 'program-closeout',
    'portfolio-closeout': 'program-closeout',
}


def normalize_phase(token):
    """Normalize --to English/lowercase aliases to the internal English phase key."""
    if not token:
        return token
    t = token.strip()
    return PHASE_ALIASES.get(t.lower(), t)


# Target phase -> gate definition
#   requires_state: lifecycle_state values permitted before this gate
#   set_state:      lifecycle_state after an authorized approval
#   hard:           hard gate (True = must pass automated checks or it blocks)
#   approver:       approval role
#   gate:           gate name
GATES = {
    'initiation': dict(requires_state={'planning'}, set_state='planning', hard=False, approver='PM',
                       gate='G0 Initiation'),
    'planning':   dict(requires_state={'planning', 'review'}, set_state='planning', hard=False, approver='PM',
                       gate='G0->1 Initiation->Planning'),
    'execution':  dict(requires_state={'planning', 'review', 'baselined'}, set_state='operational', hard=True, approver='sponsor',
                       gate='G1->2 Planning->Execution (Control Gate)'),
    'monitoring': dict(requires_state={'operational'}, set_state='operational', hard=False, approver='PM',
                       gate='G2->3 Execution->Monitoring (Soft Gate)'),
    'closeout':   dict(requires_state={'operational'}, set_state='closed', hard=True, approver='sponsor',
                       gate='G3->4 Monitoring->Closeout (Closeout Gate)'),
    # Program synonyms
    'program-delivery': dict(requires_state={'planning', 'review', 'baselined'}, set_state='operational', hard=True, approver='sponsor',
                             gate='G1->2 Program-Definition->Delivery (Control Gate)'),
    'program-closeout': dict(requires_state={'operational'}, set_state='closed', hard=True, approver='sponsor',
                             gate='G3->4 Program-Delivery->Closeout (Closeout Gate)'),
}


def load_config():
    """Read install-time config.yaml (the stage_gates block controls hard/soft gates)."""
    for cand in (os.path.join(SCRIPT_DIR, '..', 'config.yaml'),
                 os.path.join(SCRIPT_DIR, 'config.yaml')):
        if os.path.exists(cand):
            try:
                with open(cand, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                return {}
    return {}


def apply_stage_gate_config():
    """Override GATES hard flags from config.stage_gates so the config knobs take effect.
    Hard-gate strings look like 'G1->2' / 'G3->4'; soft gates 'G0->1' / 'G2->3'."""
    cfg = load_config()
    sg = cfg.get('stage_gates') or {}
    hard = set(sg.get('hard_gates') or [])
    soft = set(sg.get('soft_gates') or [])
    if not hard and not soft:
        return
    for g in GATES.values():
        gate_name = g['gate']
        prefix = gate_name.split()[0] if gate_name else ''
        if prefix in hard:
            g['hard'] = True
        elif prefix in soft:
            g['hard'] = False


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def has(path):
    return os.path.exists(path)


def run_script(name, project):
    """Run a sibling engine; return (returncode, stdout)."""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, name), '--project', project]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return p.returncode, p.stdout + p.stderr
    except Exception as e:  # noqa
        return 2, f"Could not run {name}: {e}"


# ---------- Single-criterion checks ----------
def chk_consistency(project):
    rc, _ = run_script('consistency_check.py', project)
    return rc == 0, ('consistency_check.py exit 0' if rc == 0 else 'consistency_check.py found fatal issues (exit!=0)')


def chk_baseline(data):
    bl = (data.get('baseline') or {}) if isinstance(data.get('baseline'), dict) else {}
    ok = bool(bl.get('file'))
    return ok, ('baseline pointer present (frozen baseline)' if ok
                else 'missing baseline pointer (run baseline.py --freeze first)')


def chk_control(data, project):
    rc, _ = run_script('control_engine.py', project)
    return rc == 0, ('control_engine.py exit 0 (no RED escalation)' if rc == 0 else 'control_engine.py has RED escalation (exit!=0)')


def chk_artifact(data, key):
    arts = data.get('artifacts') or {}
    return key in arts, f'artifacts.{key} registered' if key in arts else f'missing artifacts.{key} (deliverable not produced/registered)'


def chk_artifact_fresh(data, project):
    """OAG: are deliverables consistent with the source of truth (content-hash drift)?"""
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from artifact_guard import check_artifacts
        ok, viol, _ = check_artifacts(project, data)
        if ok:
            return True, 'all deliverables consistent with source of truth (OAG passed)'
        return False, f'{len(viol)} deliverable(s) not refreshed from source: {"; ".join(viol[:2])}'
    except Exception as e:
        return True, f'OAG check skipped ({e})'


def chk_program_benefits(data):
    prog = data.get('program')
    if not isinstance(prog, dict):
        return True, 'not a program, benefit verification not required'
    benefits = prog.get('benefits') or []
    if not benefits:
        return False, 'program defines no benefits (run benefits_realization first)'
    realized = {'realized', 'closed', 'done', 'completed'}
    open_b = [b.get('id', '?') for b in benefits
              if str(b.get('status', '')).strip().lower() not in realized]
    ok = not open_b
    return ok, ('all benefits realized/closed' if ok else f'unrealized benefits: {", ".join(open_b)}')


# ---------- Entry criteria (by target phase) ----------
def entry_criteria(target, data, project):
    """Return [(name, ok, detail), ...]."""
    methodology = ((data.get('project', {}) or {}).get('methodology') or '').lower()
    crit = []
    if target in ('execution', 'program-delivery'):
        crit.append(('Plan-baseline consistency', *chk_consistency(project)))
        if methodology in ('waterfall', 'hybrid'):
            crit.append(('Baseline frozen', *chk_baseline(data)))
        else:
            crit.append(('Baseline (agile/iterative waived; backlog/sprint is the baseline)', True,
                         'methodology=%s, agile/iterative convention waives forced baseline' % methodology))
    elif target in ('closeout', 'program-closeout'):
        crit.append(('Operational control has no RED', *chk_control(data, project)))
        crit.append(('Acceptance deliverable', *chk_artifact(data, 'closure_report')))
        crit.append(('Lessons learned captured', *chk_artifact(data, 'lessons_learned')))
        crit.append(('Deliverables consistent with source (OAG)', *chk_artifact_fresh(data, project)))
        if target == 'program-closeout':
            crit.append(('Benefits verified/closed', *chk_program_benefits(data)))
    # Soft gates (monitoring/planning/initiation) have no hard criteria
    return crit


def phase_label_for_state(data, state, target):
    """project.phase label to write after an authorized approval.
    Prefer the target phase itself when it is a valid phase label; otherwise fall back by state."""
    if target in PROJECT_PHASES:
        return target
    if target in PROGRAM_PHASES:
        return target
    ptype = (data.get('project', {}) or {}).get('type', 'project')
    mapping = {
        'operational': 'program-delivery' if ptype == 'program' else 'execution',
        'closed': 'program-closeout' if ptype == 'program' else 'closeout',
        'planning': 'planning',
    }
    return mapping.get(state, target)


def current_state(data):
    proj = data.get('project', {}) or {}
    return proj.get('lifecycle_state', 'planning'), proj.get('phase', 'initiation')


def _base_identity(value):
    """Normalize a stakeholder identity: drop a trailing (ROLE) qualifier and lowercase.

    'ZhangSan(PM)' -> 'zhangsan'  |  'LiSi(sponsor)' -> 'lisi'  |  'PM' -> 'pm'
    """
    text = re.sub(r'\(.*?\)', '', (value or '')).strip()
    return text.lower()


def resolve_approver(approve_arg, cfg, requester, data=None):
    """Enforce the allowlist-based authorization boundary (ClawHub T09-2).

    Returns the normalized approver string, or None when no approval was given
    (the caller treats None as "evaluate only" / denied).

    The authorized approver set is the union of:
      * config.governance.approver_identities (admin-declared allowlist), and
      * the project's own declared authorities (project.yaml: project.pm, project.sponsor).

    Membership is matched on the normalized base identity: a trailing "(ROLE)"
    qualifier is ignored, so "ZhangSan(PM)" matches a declared "ZhangSan".
    Self-approval is forbidden by default. If no authority can be derived at all
    the transition is rejected (fail-closed) instead of accepting any string.
    Records carry requester, approver, nonce and timestamp so the transition is
    attributable and non-replayable at the audit layer.
    """
    approver = (approve_arg or '').strip()
    if not approver:
        return None
    gov = (cfg.get('governance') or {}) if isinstance(cfg, dict) else {}
    allow = [_base_identity(x) for x in (gov.get('approver_identities') or [])]
    if isinstance(data, dict):
        proj = data.get('project') or {}
        for role_key in ('pm', 'sponsor'):
            declared = proj.get(role_key)
            if declared:
                allow.append(_base_identity(declared))
    allow = [x for x in allow if x]
    if not allow:
        die("No authorized approver can be derived (set config.governance.approver_identities "
            "or declare project.pm/project.sponsor). Refusing an unverifiable approval.")
    if _base_identity(approver) not in allow:
        die(f"Approver '{approver}' is not an authorized project authority "
            f"(config.governance.approver_identities or project.pm/project.sponsor)")
    if (gov.get('forbid_self_approval', True) and requester
            and _base_identity(approver) == (requester or '').strip().lower()):
        die("Self-approval forbidden: approver must differ from requester")
    return approver


def die(msg, code=1):
    print(f"x {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(description="PM Master Phase Gate Engine")
    ap.add_argument('--project', required=True)
    ap.add_argument('--to', help='Target phase: initiation/planning/execution/monitoring/closeout '
                                 '(program: program-definition/program-delivery/program-closeout)')
    ap.add_argument('--approve', metavar='APPROVER', default=None,
                    help='Approver identity (must be in config.governance.approver_identities). Given -> authorized transition; otherwise evaluate only (dry-run)')
    ap.add_argument('--requester', default=None,
                    help='Identity that requested the transition (defaults to $PM_MASTER_REQUESTER); recorded separately')
    ap.add_argument('--status', action='store_true', help='View current state and available gates only')
    a = ap.parse_args()

    if not has(a.project):
        print(f"x project.yaml not found: {a.project}", file=sys.stderr)
        sys.exit(2)
    data = load(a.project)
    root = os.path.dirname(os.path.abspath(a.project))
    cfg = load_config()

    # OAG: operational deliverable guardrail (informational; visible on every gate evaluation)
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from artifact_guard import check_artifacts as _chk
        _ok, _viol, _ = _chk(a.project, data)
        if _ok:
            print("i Deliverable guardrail (OAG): all deliverables consistent with source of truth")
        else:
            print(f"! Deliverable guardrail (OAG): {len(_viol)} violation(s) (refresh before delivery: {', '.join(_viol[:2])})")
    except Exception:
        pass
    state, phase = current_state(data)

    # ---- Status view ----
    if a.status or not a.to:
        print("=== Phase Gate Status ===")
        print(f"Current lifecycle_state: {state}")
        print(f"Current project.phase:   {phase}")
        print("Available gates (by target phase):")
        for t, g in GATES.items():
            ok_states = '/'.join(sorted(g['requires_state']))
            print(f"  -> {t:18s} | gate {g['gate']:42s} | prior state {ok_states} | {'hard gate' if g['hard'] else 'soft gate'} | approver {g['approver']}")
        if a.status:
            return
        if not a.to:
            return

    target = normalize_phase(a.to)
    if target not in GATES:
        print(f"x Unknown target phase: {a.to} (options: {', '.join(GATES.keys())}; aliases like execution/closeout accepted)", file=sys.stderr)
        sys.exit(2)

    apply_stage_gate_config()
    g = GATES[target]
    # Prior-state check
    if state not in g['requires_state']:
        print(f"x Gate rejected: current lifecycle_state={state}; entering '{target}' requires {sorted(g['requires_state'])}")
        sys.exit(1)

    # Entry criteria
    crit = entry_criteria(target, data, a.project)
    print(f"=== Phase Gate Evaluation: {g['gate']} -> '{target}' ===")
    passed = True
    for name, ok, detail in crit:
        mark = 'v' if ok else 'x'
        if not ok:
            passed = False
        print(f"  {mark} {name}: {detail}")

    if not passed:
        print("\nx Entry criteria not met; cannot enter this phase. Fix the above x items first (hard gates are not skippable; see lifecycle.md sec.5).")
        sys.exit(1)

    # dry-run: evaluate only
    if not a.approve:
        print(f"\nV Entry criteria all satisfied; can enter this phase. Approval required from {g['approver']}:")
        print(f"    python3 gate_engine.py --project {a.project} --to {target} --approve \"<approver>\"")
        sys.exit(0)

    # ---- Authorized approval: flip state + record + report ----
    # Requester attribution: only trust the environment if an admin explicitly
    # opts in (LP1 hardening); otherwise use --requester or the 'agent' default.
    # The requester is an untrusted audit label and never affects authorization.
    _trust_env = ((cfg.get('email') or {}).get('trust_env_requester', False))
    if _trust_env:
        requester = (a.requester or os.environ.get('PM_MASTER_REQUESTER') or 'agent').strip().lower()
    else:
        requester = (a.requester or 'agent').strip().lower()
    approver = resolve_approver(a.approve, cfg, requester, data)
    if approver is None:
        die("Approval required before transitioning (no authorized approver supplied)")

    new_state = g['set_state']
    new_phase = phase_label_for_state(data, new_state, target)
    today = datetime.date.today().isoformat()
    nonce = uuid.uuid4().hex

    # Update project
    proj = data.setdefault('project', {})
    prev_phase = proj.get('phase')
    proj['lifecycle_state'] = new_state
    proj['phase'] = new_phase
    if new_state == 'operational' and not proj.get('baselined_on'):
        proj['baselined_on'] = today

    # Stage-gate record
    gov = data.setdefault('governance', {})
    gates = gov.setdefault('stage_gates', [])
    record = {
        'gate': g['gate'],
        'from_phase': prev_phase,
        'to_phase': new_phase,
        'on': today,
        'by': approver,
        'requested_by': requester,
        'nonce': nonce,
        'decision': 'approved',
        'lifecycle_before': state,
        'lifecycle_after': new_state,
        'criteria': [{'name': n, 'pass': ok, 'detail': d} for n, ok, d in crit],
    }
    gates.append(record)

    # Write back project.yaml atomically (re-validate the ON-DISK state right before commit).
    # `data` has already been mutated in memory above, so we must re-read from disk and
    # compare against the state this evaluation was approved against -- comparing the
    # mutated in-memory copy would always look "changed" and abort every transition.
    try:
        disk = load(a.project)
    except Exception:
        disk = None
    if isinstance(disk, dict) and current_state(disk)[0] != state:
        die("State changed concurrently before commit; aborting to prevent stale approval")
    save(a.project, data)

    # Stage-gate review report (Markdown)
    report_dir = os.path.join(root, 'docs', 'gate_reports')
    os.makedirs(report_dir, exist_ok=True)
    slug = (proj.get('id') or 'project')
    report_path = os.path.join(report_dir, f"gate_{new_phase}_{today}.md")
    lines = [
        f"# Phase Gate Review Report - {proj.get('name', slug)}",
        "",
        f"- **Phase gate**: {g['gate']}",
        f"- **From -> To**: {prev_phase} -> {new_phase}",
        f"- **State machine**: {state} -> {new_state}",
        f"- **Approver**: {approver}",
        f"- **Requester**: {requester}",
        f"- **Date**: {today}",
        f"- **Decision**: Approved",
        f"- **Nonce**: {nonce}",
        "",
        "## Entry Criteria Verification",
        "",
        "| Criterion | Result | Detail |",
        "|-----------|--------|--------|",
    ]
    for n, ok, d in crit:
        lines.append(f"| {n} | {'Pass' if ok else 'Fail'} | {d} |")
    lines += ["", "_Generated by PM Master - gate_engine.py_", ""]
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # Register in artifacts
    arts = data.get('artifacts') or {}
    arts[f'gate_{new_phase}'] = os.path.relpath(report_path, root)
    data['artifacts'] = arts
    save(a.project, data)

    print(f"\nV Phase gate approved: {prev_phase} -> {new_phase} ({state} -> {new_state})")
    print(f"   Approver: {approver} (requester: {requester})")
    print(f"   Stage-gate record written to governance.stage_gates ({len(gates)} entries)")
    print(f"   Review report: {arts[f'gate_{new_phase}']}")
    sys.exit(0)


if __name__ == '__main__':
    main()
