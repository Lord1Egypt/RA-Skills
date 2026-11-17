#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · gate_engine.py unit test suite (standalone, no pytest needed)
============================================================
Two layers of coverage:
  A. Pure function/logic layer: directly import gate_engine, verify phase<->state
     routing, entry-criteria branches, chk_* helpers, and GATES table invariants
     (fast, deterministic, no subprocess).
  B. CLI integration layer: actually run gate_engine.py as a subprocess (along with
     its dependencies consistency_check.py / control_engine.py), covering 4
     methodologies x soft/hard gates, rejection, dry-run no-write, and --status.

Run:
  python3 scripts/test_gate_engine.py
Exit code: 0 = all pass; 1 = failures (can hook into CI gate).
"""
import os
import sys
import shutil
import subprocess
import tempfile
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gate_engine as G  # noqa

PASS = 0
FAIL = 0


def ok(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  \033[32m✓\033[0m {name}")
    else:
        FAIL += 1
        print(f"  \033[31m✗\033[0m {name}  {detail}")


def run_gate(project, to=None, approve=None, status=False):
    cmd = [sys.executable, os.path.join(HERE, 'gate_engine.py'), '--project', project]
    if status:
        cmd.append('--status')
    if to:
        cmd += ['--to', to]
    if approve:
        cmd += ['--approve', approve]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def write_yaml(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        import yaml
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


# ------------------------------------------------------------------ #
# Fixture construction
# ------------------------------------------------------------------ #
def make_project(slug, data, extra=None):
    root = os.path.join(_ROOT, slug)
    os.makedirs(root, exist_ok=True)
    proj = os.path.join(root, 'project.yaml')
    write_yaml(proj, data)
    for rel, content in (extra or {}).items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
    return proj


_WBS_WF = [
    # M1 is a milestone. It is also flagged `summary` because the Critic's orphan /
    # dependency check exempts only `summary` entries -- without it, a first-in-chain
    # milestone that has no dependsOn is reported as an orphaned package.
    {'id': 'M1', 'name': 'Design Approved', 'milestone': True, 'summary': True,
     'estimate': 1, 'start': '2026-01-01', 'end': '2026-01-10'},
    {'id': 'W1', 'name': 'Requirements', 'role': 'ba', 'estimate': 5,
     'start': '2026-01-01', 'end': '2026-01-10',
     'deliverable': 'Requirements specification', 'milestone_ref': 'M1', 'dependsOn': 'M1'},
    {'id': 'W2', 'name': 'Development', 'role': 'software-architect', 'estimate': 10,
     'start': '2026-01-11', 'end': '2026-02-10',
     'deliverable': 'Delivered module', 'milestone_ref': 'M1', 'dependsOn': 'W1'},
]

_BASELINE_WF = {
    'wbs': _WBS_WF,
    'metrics': {'evm': {'pv': 100}},
    'risks': [
        {'id': 'R1', 'likelihood': 2, 'impact': 2, 'score': 4, 'severity': 'green',
         'owner': 'WangWu', 'mitigation': 'early review'},
    ],
}

# artifact_guard (OAG) derives the required deliverable set from data presence:
#   risks/raid -> raid_log + risk_register;   metrics/actuals -> status_report;
#   wbs -> wbs;                               type=program -> portfolio_dashboard + program_charter.
# Each required key must be registered in `artifacts` AND exist on disk, so the
# fixtures must both register them and create the files; otherwise the
# "Deliverables consistent with source (OAG)" gate criterion fails.
_OAG_BASE_KEYS = ['wbs', 'raid_log', 'risk_register', 'status_report']


def _oag_artifacts(extra_keys=()):
    """Register + materialize the deliverables OAG requires for this fixture."""
    arts, files = {}, {}
    for k in list(_OAG_BASE_KEYS) + list(extra_keys):
        rel = f'artifacts/{k}.md'
        arts[k] = rel
        files[rel] = f'# {k}\n'
    return arts, files


def fixture_waterfall_planning():
    """Waterfall planning fixture: consistency exits 0 in planning state, usable for G1->2 hard gate."""
    arts, art_files = _oag_artifacts()
    data = {
        'project': {
            'id': 't-wf', 'name': 'test-waterfall', 'type': 'project', 'methodology': 'waterfall',
            'lifecycle_state': 'planning', 'phase': 'planning', 'pm': 'ZhangSan', 'sponsor': 'LiSi',
        },
        'wbs': _WBS_WF,
        'risks': [
            {'id': 'R1', 'likelihood': 2, 'impact': 2, 'score': 4, 'severity': 'green',
             'owner': 'WangWu', 'mitigation': 'early review'},
        ],
        'metrics': {'evm': {'pv': 100}},
        'decomposition': {'critic_passed': True},
        'baseline': {'file': 'baselines/2026-01-01.yaml', 'on': '2026-01-01'},
        'artifacts': arts,
    }
    extra = {'baselines/2026-01-01.yaml': _dump(_BASELINE_WF)}
    extra.update(art_files)
    return make_project('wf_plan', data, extra=extra)


def fixture_waterfall_operational():
    """Waterfall operational fixture: consistency exits 0 in execution state and control_engine exits 0, for G3->4 hard gate."""
    arts, art_files = _oag_artifacts()
    data = {
        'project': {
            'id': 't-wf2', 'name': 'test-waterfall-ops', 'type': 'project', 'methodology': 'waterfall',
            'lifecycle_state': 'operational', 'phase': 'execution', 'pm': 'ZhangSan', 'sponsor': 'LiSi',
        },
        'wbs': _WBS_WF,
        'risks': [
            {'id': 'R1', 'likelihood': 2, 'impact': 2, 'score': 4, 'severity': 'green',
             'owner': 'WangWu', 'mitigation': 'early review'},
        ],
        # ev/ac == pv keeps SPI/CPI at 1.0 so control_engine reports GREEN (no RED escalation)
        'metrics': {'evm': {'pv': 100, 'ev': 100, 'ac': 100}},
        'decomposition': {'critic_passed': True},
        'baseline': {'file': 'baselines/2026-01-01.yaml', 'on': '2026-01-01'},
        'actuals': {'as_of': '2026-02-01', 'ev': 100, 'ac': 100,
                    'wbs_progress': {'M1': 100, 'W1': 100, 'W2': 100}},
        'artifacts': dict(arts, closure_report='artifacts/closure_report.md',
                          lessons_learned='artifacts/lessons_learned.md'),
    }
    extra = {'baselines/2026-01-01.yaml': _dump(_BASELINE_WF),
             'artifacts/closure_report.md': '# Acceptance Deliverables\n',
             'artifacts/lessons_learned.md': '# Lessons Learned\n'}
    extra.update(art_files)
    return make_project('wf_op', data, extra=extra)


def fixture_agile_planning():
    data = {
        'project': {
            'id': 't-ag', 'name': 'test-agile', 'type': 'project', 'methodology': 'agile',
            'lifecycle_state': 'planning', 'phase': 'planning', 'pm': 'ZhangSan', 'sponsor': 'LiSi',
        },
        'backlog': [
            {'id': 'B1', 'name': 'Login', 'estimate': 3},
            {'id': 'B2', 'name': 'List', 'estimate': 5},
        ],
        'sprints': [
            {'id': 'S1', 'name': 'Sprint 1', 'tasks': [{'id': 'T1', 'name': 'Login', 'estimate': 3}]},
        ],
        'risks': [],
        'artifacts': {},
    }
    return make_project('ag_plan', data)


def fixture_program_operational():
    # program type additionally requires portfolio_dashboard + program_charter
    arts, art_files = _oag_artifacts(extra_keys=('portfolio_dashboard', 'program_charter'))
    data = {
        'project': {
            'id': 't-pg', 'name': 'test-program', 'type': 'program', 'methodology': 'waterfall',
            'lifecycle_state': 'operational', 'phase': 'program-delivery', 'pm': 'ZhangSan', 'sponsor': 'LiSi',
        },
        'wbs': _WBS_WF,
        'risks': [
            {'id': 'R1', 'likelihood': 2, 'impact': 2, 'score': 4, 'severity': 'green',
             'owner': 'WangWu', 'mitigation': 'early review'},
        ],
        # ev/ac == pv keeps SPI/CPI at 1.0 so control_engine reports GREEN (no RED escalation)
        'metrics': {'evm': {'pv': 100, 'ev': 100, 'ac': 100}},
        'decomposition': {'critic_passed': True},
        'baseline': {'file': 'baselines/2026-01-01.yaml', 'on': '2026-01-01'},
        'actuals': {'as_of': '2026-02-01', 'ev': 100, 'ac': 100,
                    'wbs_progress': {'M1': 100, 'W1': 100, 'W2': 100}},
        'program': {'benefits': [{'id': 'BN1', 'status': 'realized', 'owner': 'ZhaoLiu'}]},
        'artifacts': dict(arts, closure_report='artifacts/closure_report.md',
                          lessons_learned='artifacts/lessons_learned.md'),
    }
    extra = {'baselines/2026-01-01.yaml': _dump(_BASELINE_WF),
             'artifacts/closure_report.md': '# Acceptance Deliverables\n',
             'artifacts/lessons_learned.md': '# Lessons Learned\n'}
    extra.update(art_files)
    return make_project('pg_op', data, extra=extra)


def _dump(d):
    import yaml
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False)


# ------------------------------------------------------------------ #
# A. Pure function / logic layer
# ------------------------------------------------------------------ #
def test_logic_layer():
    print("\n[A] Pure function / logic layer")
    # GATES table invariants
    for t, g in G.GATES.items():
        ok(f"GATES[{t}] has required keys",
           all(k in g for k in ('requires_state', 'set_state', 'hard', 'approver', 'gate')),
           str(g))
    # Hard gates must be execution/closeout/program-delivery/program-closeout
    hard_targets = [t for t, g in G.GATES.items() if g['hard']]
    ok("Hard gates contain only control/closeout gates",
       set(hard_targets) == {'execution', 'closeout', 'program-delivery', 'program-closeout'}, str(hard_targets))
    # Soft gates must not block (entry_criteria returns empty criteria for initiation/planning/monitoring)
    for soft in ('initiation', 'planning', 'monitoring'):
        crit = G.entry_criteria(soft, {'project': {'methodology': 'waterfall'}}, 'x')
        ok(f"Soft gate {soft} has no hard criteria", crit == [], str(crit))
    # phase_label_for_state: target is a valid phase -> prefer target (monitoring fix)
    data_op = {'project': {'type': 'project'}}
    ok("execution->monitoring writes phase=monitoring (fix)",
       G.phase_label_for_state(data_op, 'operational', 'monitoring') == 'monitoring')
    ok("planning->execution writes phase=execution",
       G.phase_label_for_state(data_op, 'operational', 'execution') == 'execution')
    # Program synonym
    data_pg = {'project': {'type': 'program'}}
    ok("program program-closeout->program-closeout",
       G.phase_label_for_state(data_pg, 'closed', 'program-closeout') == 'program-closeout')
    # Fallback mapping (target invalid -> map by state)
    ok("fallback: operational->execution", G.phase_label_for_state(data_op, 'operational', 'ZZ') == 'execution')
    ok("fallback: closed->closeout", G.phase_label_for_state(data_op, 'closed', 'ZZ') == 'closeout')
    ok("fallback: planning->planning", G.phase_label_for_state(data_op, 'planning', 'ZZ') == 'planning')
    # chk_* helpers
    ok("chk_baseline has pointer=True", G.chk_baseline({'baseline': {'file': 'x.yaml'}})[0] is True)
    ok("chk_baseline no pointer=False", G.chk_baseline({'baseline': {}})[0] is False)
    ok("chk_artifact exists=True", G.chk_artifact({'artifacts': {'closure_report': 'p'}}, 'closure_report')[0] is True)
    ok("chk_artifact missing=False", G.chk_artifact({'artifacts': {}}, 'closure_report')[0] is False)
    ok("chk_program_benefits non-program=True", G.chk_program_benefits({'program': None})[0] is True)
    ok("chk_program_benefits all realized=True",
       G.chk_program_benefits({'program': {'benefits': [{'id': 'B1', 'status': 'realized'}]}})[0] is True)
    ok("chk_program_benefits has unrealized=False",
       G.chk_program_benefits({'program': {'benefits': [{'id': 'B1', 'status': 'open'}]}})[0] is False)
    # entry_criteria branch: closeout missing deliverables -> passed=False
    crit = G.entry_criteria('closeout', {'project': {'methodology': 'waterfall'}, 'artifacts': {}}, 'x')
    ok("closeout missing closure/lessons -> has unmet criteria", any(not ok_ for _, ok_, _ in crit), str(crit))
    # entry_criteria branch: agile into execution waives baseline
    crit = G.entry_criteria('execution', {'project': {'methodology': 'agile'}}, 'x')
    names = [n.lower() for n, _, _ in crit]
    ok("agile into execution excludes 'baseline frozen' criterion", 'baseline frozen' not in names, str(names))
    # waterfall into execution includes 'baseline frozen' criterion
    crit = G.entry_criteria('execution', {'project': {'methodology': 'waterfall'}}, 'x')
    names = [n.lower() for n, _, _ in crit]
    ok("waterfall into execution includes 'baseline frozen' criterion", 'baseline frozen' in names, str(names))


# ------------------------------------------------------------------ #
# B. CLI integration layer
# ------------------------------------------------------------------ #
def test_cli_layer():
    print("\n[B] CLI integration layer")

    # B1 soft gate G0->1 initiation->planning
    p = fixture_waterfall_planning()
    rc, out = run_gate(p, to='planning', approve='ZhangSan(PM)')
    ok("soft gate planning approve success (rc=0)", rc == 0, out)
    d = _load(p)
    ok("soft gate planning -> phase=planning", d['project']['phase'] == 'planning', d['project']['phase'])
    ok("soft gate planning state still planning", d['project']['lifecycle_state'] == 'planning')
    ok("soft gate planning wrote stage_gates", len(d.get('governance', {}).get('stage_gates', [])) == 1)

    # B2 soft gate G2->3 execution->monitoring (fix: must not be written as execution)
    p = fixture_waterfall_operational()
    rc, out = run_gate(p, to='monitoring', approve='ZhangSan(PM)')
    ok("soft gate monitoring approve success (rc=0)", rc == 0, out)
    d = _load(p)
    ok("soft gate monitoring -> phase=monitoring (fix)", d['project']['phase'] == 'monitoring', d['project']['phase'])
    ok("soft gate monitoring state still operational", d['project']['lifecycle_state'] == 'operational')

    # B3 hard gate G1->2 waterfall planning->execution (has baseline + consistency)
    p = fixture_waterfall_planning()
    rc, out = run_gate(p, to='execution', approve='LiSi(sponsor)')
    ok("hard gate execution (waterfall, baseline present) passes (rc=0)", rc == 0, out)
    d = _load(p)
    ok("hard gate execution -> phase=execution", d['project']['phase'] == 'execution', d['project']['phase'])
    ok("hard gate execution state=operational", d['project']['lifecycle_state'] == 'operational')
    ok("hard gate execution wrote stage_gates", len(d.get('governance', {}).get('stage_gates', [])) == 1)
    ok("hard gate execution produced report docs/gate_reports", os.path.exists(
        os.path.join(os.path.dirname(p), 'docs', 'gate_reports')))

    # B4 hard gate G1->2 waterfall missing baseline -> blocked (rc=1)
    p = fixture_waterfall_planning()
    # remove baseline pointer
    d = _load(p)
    d.pop('baseline', None)
    write_yaml(p, d)
    rc, out = run_gate(p, to='execution')
    ok("hard gate execution (waterfall, missing baseline) blocked (rc=1)", rc == 1, out)
    ok("hard gate execution block message mentions 'baseline'", 'baseline' in out.lower(), out)
    d2 = _load(p)
    ok("hard gate execution blocked phase unchanged", d2['project']['phase'] == 'planning', d2['project']['phase'])

    # B5 hard gate G1->2 agile waives baseline -> passes (rc=0)
    p = fixture_agile_planning()
    rc, out = run_gate(p, to='execution', approve='LiSi(sponsor)')
    ok("hard gate execution (agile, baseline waived) passes (rc=0)", rc == 0, out)
    d = _load(p)
    ok("hard gate execution (agile) -> phase=execution", d['project']['phase'] == 'execution', d['project']['phase'])
    ok("hard gate execution (agile) state=operational", d['project']['lifecycle_state'] == 'operational')

    # B6 hard gate G3->4 closeout (deliverables present + control exit 0)
    p = fixture_waterfall_operational()
    rc, out = run_gate(p, to='closeout', approve='LiSi(sponsor)')
    ok("hard gate closeout (complete) passes (rc=0)", rc == 0, out)
    d = _load(p)
    ok("hard gate closeout -> phase=closeout", d['project']['phase'] == 'closeout', d['project']['phase'])
    ok("hard gate closeout state=closed", d['project']['lifecycle_state'] == 'closed')

    # B7 hard gate G3->4 closeout missing deliverables -> blocked (rc=1)
    p = fixture_waterfall_operational()
    d = _load(p)
    d['artifacts'].pop('closure_report', None)
    write_yaml(p, d)
    rc, out = run_gate(p, to='closeout')
    ok("hard gate closeout (missing acceptance) blocked (rc=1)", rc == 1, out)
    ok("hard gate closeout block message mentions closure", 'closure' in out, out)
    d2 = _load(p)
    ok("hard gate closeout blocked state unchanged", d2['project']['lifecycle_state'] == 'operational')

    # B8 program program-closeout (benefits realized)
    p = fixture_program_operational()
    rc, out = run_gate(p, to='program-closeout', approve='LiSi(sponsor)')
    ok("hard gate program-closeout (benefits realized) passes (rc=0)", rc == 0, out)
    d = _load(p)
    ok("hard gate program-closeout -> phase=program-closeout", d['project']['phase'] == 'program-closeout', d['project']['phase'])
    ok("hard gate program-closeout state=closed", d['project']['lifecycle_state'] == 'closed')

    # B9 program program-closeout benefits unrealized -> blocked
    p = fixture_program_operational()
    d = _load(p)
    d['program']['benefits'][0]['status'] = 'open'
    write_yaml(p, d)
    rc, out = run_gate(p, to='program-closeout')
    ok("hard gate program-closeout (benefits unrealized) blocked (rc=1)", rc == 1, out)
    ok("hard gate program-closeout block message mentions 'benefit'", 'benefit' in out, out)

    # B10 prerequisite state mismatch -> rejected (rc=1)
    p = fixture_waterfall_operational()  # operational
    rc, out = run_gate(p, to='planning')       # planning requires planning/review/baselined
    ok("prerequisite state mismatch rejected (rc=1)", rc == 1, out)
    ok("rejection message mentions 'gate rejected'", 'gate rejected' in out.lower(), out)

    # B11 unknown target -> exit (rc=2)
    p = fixture_waterfall_planning()
    rc, out = run_gate(p, to='nonexistent-phase')
    ok("unknown target exit (rc=2)", rc == 2, out)

    # B12 dry-run no write (phase/state/stage_gates unchanged)
    p = fixture_waterfall_planning()
    before = _load(p)
    rc, out = run_gate(p, to='execution')  # no --approve
    ok("dry-run evaluation success (rc=0)", rc == 0, out)
    after = _load(p)
    ok("dry-run before phase=planning", before['project']['phase'] == 'planning')
    ok("dry-run after phase still=planning (not written)", after['project']['phase'] == 'planning')
    ok("dry-run did not write stage_gates",
       len(after.get('governance', {}).get('stage_gates', [])) == 0)

    # B13 --status normal output
    p = fixture_waterfall_planning()
    rc, out = run_gate(p, status=True)
    ok("--status success (rc=0)", rc == 0, out)
    low = out.lower()
    ok("--status contains available gates", 'available gates' in low, out)
    ok("--status contains hard/soft gate markers", 'hard gate' in low and 'soft gate' in low, out)


def _load(path):
    import yaml
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------------ #
def main():
    global _ROOT
    _ROOT = tempfile.mkdtemp(prefix='pm_gate_test_')
    print(f"Temp root: {_ROOT}")
    try:
        test_logic_layer()
        test_cli_layer()
    finally:
        shutil.rmtree(_ROOT, ignore_errors=True)
    print(f"\n==== Result: passed {PASS} / failed {FAIL} ====")
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
