#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Operational Control Engine

After entering the operational phase, run the configured checks periodically against
the **baseline** per control.cadence, ensuring the project runs as expected versus the
baseline; any control item breaching a threshold escalates an alert (exit 1, can be
hooked to a scheduled job).

Comparison target: baselines/<date>.yaml (frozen by baseline.py)
Input (project.yaml): baseline pointer + actuals (latest actual progress) + control (thresholds/frequency/recipients)

Control items:
  1. Schedule    : per-WBS-package planned% vs actual% variance / overdue days
  2. Cost EVM    : SPI=EV/PV, CPI=EV/AC, EAC/ETC/VAC
  3. Risk Drift  : current score vs baseline score; new red/critical risks
  4. Milestone   : milestone overdue and unfinished
  5. Issue       : RAID issue overdue and unclosed
  6. Change      : number of open change requests
  7. Integrity   : re-run consistency_check

Usage:
  python3 control_engine.py --project /workspace/<slug>/project.yaml [--as-of 2026-08-12] [--json]
"""
import os
import sys
import json
import subprocess
import datetime
import argparse

try:
    import yaml
except ImportError:
    yaml = None

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config():
    """Read the install-time config.yaml (knobs such as operational_control / quality_gate)."""
    for cand in (os.path.join(HERE, '..', 'config.yaml'),
                 os.path.join(HERE, 'config.yaml')):
        if os.path.exists(cand):
            try:
                with open(cand, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                return {}
    return {}
RENDER = os.path.join(HERE, 'render.py')
CONSISTENCY = os.path.join(HERE, 'consistency_check.py')

# ---- Unified status constants (avoid per-pillar inline hardcode causing typos) ----
DONE_STATES = {'done', 'complete', 'completed'}
CLOSED_STATES = {'closed', 'resolved', 'retired'}
CANCELLED_STATES = {'cancelled', 'canceled', 'descoped', 'out-of-scope',
                    'terminated', 'deferred'}
NOT_OVERDUE_STATES = DONE_STATES | CLOSED_STATES | CANCELLED_STATES
NON_WORKING_STATES = CANCELLED_STATES
RISK_INACTIVE_STATES = CLOSED_STATES | CANCELLED_STATES | DONE_STATES


def _norm_status(v):
    """Normalize status: lowercase + compatible synonyms."""
    if v is None:
        return ''
    s = str(v).strip().lower()
    return s


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required; please run: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def run(cmd):
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True)


def parse_date(s):
    if not s:
        return None
    for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.datetime.strptime(str(s), fmt).date()
        except ValueError:
            continue
    return None


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def collect_risks(data):
    seen = {}
    for r in (data.get('risks') or []):
        if r.get('id'):
            seen[r['id']] = r
    for r in ((data.get('raid') or {}).get('risks') or []):
        if r.get('id') and r['id'] not in seen:
            seen[r['id']] = r
    return list(seen.values())


SEV_TO_BAND = {'green': 'low', 'yellow': 'medium', 'orange': 'high', 'red': 'critical'}


def norm_sev(s):
    return SEV_TO_BAND.get(str(s).strip().lower()) if s else None


def compute(data, bdata, as_of):
    controls = []
    escalations = []
    cfg = data.get('control') or {}
    thr = cfg.get('thresholds') or {}
    spi_warn = float(thr.get('spi_warn', 0.95))
    cpi_warn = float(thr.get('cpi_warn', 0.95))
    slip_pct = float(thr.get('schedule_slip_pct', 15))
    open_change_high = int(thr.get('open_change_high', 2))

    actuals = data.get('actuals') or {}
    have_actuals = bool(data.get('actuals'))
    wbs_progress = actuals.get('wbs_progress') or {}
    ev_reported = actuals.get('ev')
    ac = actuals.get('ac')

    bl_wbs = bdata.get('wbs') or []
    # Program level: only compute progress from milestone-level rows (tier != 'component'),
    # to avoid spreading component leaf detail into the program report; component level
    # computes across its own full wbs.
    bl_wbs_all = bl_wbs
    if str((data.get('project') or {}).get('type', '')).lower() == 'program':
        bl_wbs = [w for w in bl_wbs if w.get('tier') != 'component']
    proj_type = str((data.get('project') or {}).get('type', '')).lower()
    bl_evm = (bdata.get('metrics') or {}).get('evm') or {}
    bac = bl_evm.get('bac') or bl_evm.get('pv') or 0
    # If baseline carries pv as the total planned value and no bac is given, use pv as the
    # approximate budget-at-completion.
    if not bac and bl_evm.get('pv'):
        bac = bl_evm.get('pv')

    # ---------- 1. Schedule ----------
    # Structured progress detail: one row per work package/milestone, recording planned% /
    # actual% / variance% / status. Program level: baseline.wbs contains only each SOW
    # milestone summary package -> naturally aggregates to milestone-level detail; component
    # level: baseline.wbs contains leaf packages -> detail down to leaf level. Both share
    # the same render logic.
    sched_msgs = []
    total_est = 0.0
    planned_wsum = 0.0
    actual_wsum = 0.0
    overdue_pkgs = []
    schedule_rows = []
    for w in bl_wbs:
        # Summary package is a label row whose estimate is a rollup of child leaves;
        # including it would double-count, so skip.
        if w.get('summary'):
            continue
        # Cancelled/descoped/terminated/out-of-scope packages are excluded from schedule
        # control (not active work, not counted as overdue).
        if _norm_status(w.get('status')) in NON_WORKING_STATES:
            continue
        est = w.get('estimate') or 0
        try:
            est = float(est)
        except (TypeError, ValueError):
            est = 0
        s = parse_date(w.get('start'))
        e = parse_date(w.get('end'))
        planned_pct = 0.0
        if s and e and e >= s:
            if as_of <= s:
                planned_pct = 0.0
            elif as_of >= e:
                planned_pct = 100.0
            else:
                planned_pct = (as_of - s).days / max((e - s).days, 1) * 100.0
        if isinstance(wbs_progress, dict):
            actual_pct = float(wbs_progress.get(w.get('id'), 0) or 0)
        else:
            # Fault tolerance: if wbs_progress is passed as a scalar (overall completion%),
            # apply it uniformly to each work package
            try:
                actual_pct = float(wbs_progress or 0)
            except (TypeError, ValueError):
                actual_pct = 0.0
        total_est += est
        planned_wsum += est * planned_pct
        actual_wsum += est * actual_pct
        variance = actual_pct - planned_pct
        # Row-level status: behind by more than threshold -> alert; overdue and unfinished -> red; otherwise green
        if actual_pct < planned_pct - slip_pct:
            row_status = 'RED' if (e and as_of > e and actual_pct < 100) else 'AMBER'
        else:
            row_status = 'GREEN'
        schedule_rows.append({
            'id': w.get('id'), 'name': w.get('name'),
            'planned': round(planned_pct, 1), 'actual': round(actual_pct, 1),
            'variance': round(variance, 1), 'status': row_status,
        })
        if e and as_of > e and actual_pct < 100:
            overdue_pkgs.append({'id': w.get('id'), 'name': w.get('name'),
                                 'overdue_days': (as_of - e).days})
        if actual_pct < planned_pct - slip_pct:
            sched_msgs.append(f"{w.get('id')} actual {actual_pct:.0f}% behind plan {planned_pct:.0f}% "
                             f"(diff {planned_pct-actual_pct:.0f}%)")
    overall_planned = (planned_wsum / total_est) if total_est else 0.0
    overall_actual = (actual_wsum / total_est) if total_est else 0.0
    # Overall status aggregates from row-level statuses: any RED -> red; any AMBER -> yellow; otherwise green
    row_statuses = [r['status'] for r in schedule_rows]
    if 'RED' in row_statuses:
        sched_status = 'RED'
    elif 'AMBER' in row_statuses or sched_msgs:
        sched_status = 'AMBER'
    else:
        sched_status = 'GREEN'
    if overdue_pkgs:
        sched_status = 'RED'
    sched_detail = (f"Overall progress plan {overall_planned:.0f}% / actual {overall_actual:.0f}%."
                    + (f" {len(sched_msgs)} behind, {len(overdue_pkgs)} overdue."
                       if (sched_msgs or overdue_pkgs) else " Schedule under control."))
    controls.append({'name': 'Schedule Control', 'status': sched_status,
                     'detail': sched_detail, 'key': 'schedule'})
    if sched_status == 'RED':
        escalations.append('schedule_slip')

    # ---------- 2. Cost / EVM ----------
    # Unified EVM currency basis: PV/EV/AC must share the same basis. This engine uses
    # BAC (currency) as the sole basis, and no longer references metrics.evm.pv (historically
    # stored person-days, now deprecated). For fixed-fee work, EV should be measured by
    # 'billing milestone done' rather than physical completion%; before the first billing
    # milestone is confirmed, physical% systematically understates EV, so CPI should not be
    # flagged red.
    proj_start = parse_date((data.get('project') or {}).get('start_date'))
    pre_start = bool(proj_start and as_of < proj_start)

    # Billing milestones (fixed-fee) and their completion status (from actuals.milestone_status
    # or wbs_progress milestone rows)
    def _milestone_done(mid):
        ms = (actuals.get('milestone_status') or {}) if isinstance(actuals, dict) else {}
        st = ms.get(mid)
        if st in ('done', 'complete', 'signed-off', 'signed_off', 100):
            return True
        wp = wbs_progress.get(mid) if isinstance(wbs_progress, dict) else None
        try:
            return float(wp or 0) >= 100
        except (TypeError, ValueError):
            return False

    fixed_milestones = []
    for w in (bdata.get('wbs') or []):
        b = w.get('billing') or {}
        fee = b.get('fee_inr') or b.get('fee')
        if w.get('milestone') and b.get('fee_type') == 'fixed' and fee:
            try:
                fixed_milestones.append((w.get('id'), float(fee)))
            except (TypeError, ValueError):
                pass
    evm_method = 'physical'
    ev_fixed = 0.0
    pv_fixed = 0.0
    if fixed_milestones:
        evm_method = 'milestone'
        for mid, fee in fixed_milestones:
            if _milestone_done(mid):
                ev_fixed += fee
            # PV (fixed-fee): a milestone's planned completion (as_of past its end) counts toward planned value
            s = parse_date(({w.get('id'): w for w in (bdata.get('wbs') or [])}.get(mid) or {}).get('end'))
            if s and as_of >= s:
                pv_fixed += fee

    if pre_start:
        # Before baseline start no earned value should be produced; PV=EV=AC=0, EVM set to
        # N/A to avoid falsely reporting SPI=1.0
        pv = ev = ac_v = 0.0
        spi = cpi = 1.0
        eac = etc = vac = 0.0
        evm_status = 'N/A'
        evm_detail = (f"EVM not applicable: as_of {as_of.isoformat()} is before project start {proj_start.isoformat()}"
                      f"; no earned value before baseline start (PV=EV=AC=0).")
    else:
        if evm_method == 'milestone':
            # Fixed-fee portion measured by milestones; non-fixed (BAC - fixed total) portion
            # measured by physical%
            fixed_total = sum(f for _, f in fixed_milestones)
            tm_base = max(bac - fixed_total, 0.0)
            ev_tm = tm_base * overall_actual / 100.0 if tm_base else 0.0
            pv_tm = tm_base * overall_planned / 100.0 if tm_base else 0.0
            ev = ev_fixed + ev_tm
            pv = pv_fixed + pv_tm
            ac_v = float(ac) if isinstance(ac, (int, float)) else 0.0
            # Before the first billing milestone is confirmed, CPI uses physical% as an
            # estimate, flagged only as AMBER, not escalated to red
            if ev_fixed <= 0 and ac_v > 0:
                cpi = (ev / ac_v) if ac_v > 0 else 1.0
                spi = (ev / pv) if pv > 0 else 1.0
                eac = etc = vac = 0.0  # do not extrapolate EAC/VAC before billing milestone confirmed (avoid false variance)
                evm_status = 'AMBER'
                evm_detail = (f"SPI={spi:.2f} CPI={cpi:.2f} (estimate, physical% used before first billing milestone confirmed) | "
                              f"PV={pv:.1f} EV={ev:.1f} AC={ac_v:.1f} | Fixed-fee BAC={fixed_total:.0f} confirmed EV={ev_fixed:.0f}"
                              f"\n  ⚠ Note: for fixed-fee SOWs, before the first Wave Design Document is signed off, "
                              f"CPI does not carry a real overspend meaning; do not report EAC/VAC variance on this basis.")
                # Do not append 'cpi' escalation (avoid false RED)
                if spi < spi_warn:
                    escalations.append('spi')
            else:
                cpi = (ev / ac_v) if ac_v > 0 else 1.0
                spi = (ev / pv) if pv > 0 else 1.0
                eac = (bac / cpi) if cpi > 0 else bac
                etc = max(eac - ac_v, 0.0)
                vac = bac - eac
                evm_status = 'GREEN'
                if cpi < cpi_warn or spi < spi_warn:
                    evm_status = 'RED'
                elif cpi < 1.0 or spi < 1.0:
                    evm_status = 'AMBER'
                evm_detail = (f"SPI={spi:.2f} CPI={cpi:.2f} (milestone measured) | PV={pv:.1f} EV={ev:.1f} AC={ac_v:.1f} | "
                              f"EAC={eac:.1f} ETC={etc:.1f} VAC={vac:.1f} (BAC={bac:.1f}) | confirmed fixed-fee EV={ev_fixed:.0f}")
                if cpi < cpi_warn:
                    escalations.append('cpi')
                if spi < spi_warn:
                    escalations.append('spi')
        else:
            pv = bac * overall_planned / 100.0 if bac else 0.0
            ev = float(ev_reported) if isinstance(ev_reported, (int, float)) else (bac * overall_actual / 100.0 if bac else 0.0)
            ac_v = float(ac) if isinstance(ac, (int, float)) else 0.0
            spi = (ev / pv) if pv > 0 else 1.0
            cpi = (ev / ac_v) if ac_v > 0 else 1.0
            eac = (bac / cpi) if cpi > 0 else bac
            etc = max(eac - ac_v, 0.0)
            vac = bac - eac
            evm_status = 'GREEN'
            if cpi < cpi_warn or spi < spi_warn:
                evm_status = 'RED'
            elif cpi < 1.0 or spi < 1.0:
                evm_status = 'AMBER'
            evm_detail = (f"SPI={spi:.2f} CPI={cpi:.2f} | PV={pv:.1f} EV={ev:.1f} AC={ac_v:.1f} | "
                          f"EAC={eac:.1f} ETC={etc:.1f} VAC={vac:.1f} (BAC={bac:.1f})")
            if cpi < cpi_warn:
                escalations.append('cpi')
            if spi < spi_warn:
                escalations.append('spi')

    controls.append({'name': 'Cost / Earned Value EVM', 'status': evm_status,
                     'detail': evm_detail, 'key': 'evm'})

    # ---------- 3. Risk Drift ----------
    bl_risks = {r.get('id'): r for r in (bdata.get('risks') or [])}
    cur_risks = collect_risks(data)
    risk_msgs = []
    risk_red = False
    for r in cur_risks:
        rid = r.get('id')
        if _norm_status(r.get('status')) in RISK_INACTIVE_STATES:
            continue  # closed/resolved/cancelled risks do not count as active drift
        bl = bl_risks.get(rid)
        if bl and isinstance(r.get('score'), (int, float)) and isinstance(bl.get('score'), (int, float)):
            if r['score'] > bl['score']:
                risk_msgs.append(f"{rid} score {bl['score']}->{r['score']} escalated")
                risk_red = True
        if norm_sev(r.get('severity')) == 'critical':
            risk_msgs.append(f"{rid} is a current red/critical risk")
            risk_red = True
        if rid not in bl_risks and norm_sev(r.get('severity')) in ('high', 'critical'):
            risk_msgs.append(f"{rid} new high/critical risk added after baseline")
            risk_red = True
    risk_status = 'RED' if risk_red else ('AMBER' if risk_msgs else 'GREEN')
    controls.append({'name': 'Risk Drift', 'status': risk_status,
                     'detail': ('; '.join(risk_msgs) if risk_msgs else 'No risk escalation versus baseline'), 'key': 'risk'})
    if risk_red:
        escalations.append('new_red_risk' if any('new' in m for m in risk_msgs) else 'risk_upgrade')

    # ---------- 4. Milestone ----------
    # Milestone source: prefer top-level milestones[], otherwise derive from wbs milestone
    # packages (SKILL single source of truth).
    ms_top = data.get('milestones') or bdata.get('milestones') or []
    if not ms_top:
        wbs_all = (data.get('wbs') or []) + (bdata.get('wbs') or [])
        seen = set()
        for w in wbs_all:
            if w.get('milestone') and w.get('id') not in seen:
                seen.add(w.get('id'))
                wp = (wbs_progress.get(w.get('id')) if isinstance(wbs_progress, dict) else None)
                try:
                    done = float(wp or 0) >= 100
                except (TypeError, ValueError):
                    done = False
                ms_top.append({
                    'id': w.get('id'), 'name': w.get('name'),
                    'date': w.get('start') or w.get('end'),
                    'status': 'done' if done else (w.get('status') or 'open'),
                })
    ms = ms_top
    ms_overdue = []
    for m in ms:
        d = parse_date(m.get('date'))
        st = str(m.get('status', '')).lower()
        if d and as_of > d and st not in ('done', 'complete', 'closed'):
            ms_overdue.append(m.get('id') or m.get('name'))
    ms_status = 'RED' if ms_overdue else 'GREEN'
    controls.append({'name': 'Milestone', 'status': ms_status,
                     'detail': ('Overdue unfinished: ' + ', '.join(ms_overdue)) if ms_overdue else 'No overdue milestones',
                     'key': 'milestone'})
    if ms_overdue:
        escalations.append('overdue_milestone')

    # ---------- 5. RAID Issues ----------
    issues = (data.get('raid') or {}).get('issues') or []
    iss_overdue = []
    for i in issues:
        d = parse_date(i.get('due'))
        st = str(i.get('status', '')).lower()
        if d and as_of > d and st not in ('done', 'complete', 'closed'):
            iss_overdue.append(i.get('id'))
    iss_status = 'RED' if iss_overdue else 'GREEN'
    controls.append({'name': 'RAID Issues', 'status': iss_status,
                     'detail': ('Overdue unclosed: ' + ', '.join(iss_overdue)) if iss_overdue else 'No overdue issues',
                     'key': 'issue'})
    if iss_overdue:
        escalations.append('overdue_issue')

    # ---------- 6. Change ----------
    changes = data.get('changes') or (data.get('raid') or {}).get('changes') or []
    # Support change_log table
    clog = data.get('change_log') or []
    if isinstance(clog, list):
        changes = clog
    open_changes = [c for c in changes
                    if str(c.get('status', '')).lower() in ('open', 'pending')]
    ch_status = 'RED' if len(open_changes) >= open_change_high else ('AMBER' if open_changes else 'GREEN')
    controls.append({'name': 'Change', 'status': ch_status,
                     'detail': f"Open change requests: {len(open_changes)} (escalate at threshold >= {open_change_high})",
                     'key': 'change'})
    if len(open_changes) >= open_change_high:
        escalations.append('open_change_high')

    # ---------- 6b. Control-gate discipline (lifecycle_state technically enforced) ----------
    # Aligns with lifecycle.md section 5: waterfall/hybrid must enforce
    # planning->baselined->operational sequencing. The control engine only runs formal
    # inspections under operational; if not entered, warn (AMBER) rather than falsely
    # reporting a RED escalation.
    ls = str((data.get('project') or {}).get('lifecycle_state') or 'planning').lower()
    # Terminal closed state: program/project formally closed via the closeout gate, past the
    # operational control phase, should no longer report gate_not_operational.
    TERMINAL_LS = {'closed', 'closeout', 'terminated', 'cancelled', 'archived'}
    if ls == 'operational':
        gate_status = 'GREEN'
        gate_detail = 'Passed control gate and in operational control phase (lifecycle_state=operational); control engine inspecting normally.'
    elif ls in TERMINAL_LS:
        gate_status = 'GREEN'
        gate_detail = (f'Entered terminal state (lifecycle_state={ls}): project/program formally closed via closeout '
                       f'gate, past the operational control phase; this run is a historical comparison only and no '
                       f'longer requires operational.')
    elif ls == 'baselined':
        gate_status = 'AMBER'
        gate_detail = ('Baseline taken but lifecycle_state=operational not set; still comparing against baseline '
                       'this run, but formal operational control requires the control gate to set lifecycle_state to operational first.')
    else:
        gate_status = 'AMBER'
        gate_detail = (f'Current lifecycle_state={ls}, not yet in operational control phase; control engine should '
                       f'run under operational (baseline.py --freeze -> control gate -> operational).')
    controls.append({'name': 'Control Gate', 'status': gate_status,
                     'detail': gate_detail, 'key': 'gate'})
    if ls not in ({'operational'} | TERMINAL_LS):
        escalations.append('gate_not_operational')

    # ---------- 7. Integrity ----------
    chk = run([CONSISTENCY, '--project', project_path_global])
    int_status = 'GREEN' if chk.returncode == 0 else 'RED'
    controls.append({'name': 'Integrity', 'status': int_status,
                     'detail': ('Consistency gate passed' if chk.returncode == 0
                                else 'Consistency gate failed; see consistency_check output'), 'key': 'integrity'})
    if int_status == 'RED':
        escalations.append('integrity')

    # No actuals reported: schedule/EVM cannot be compared to baseline; mark as AMBER
    # (operational gap) rather than falsely reporting a RED escalation
    if not have_actuals:
        for c in controls:
            if c['key'] in ('schedule', 'evm'):
                c['status'] = 'AMBER'
                c['detail'] = ('No actuals reported (actuals); cannot compare to baseline to compute'
                               + ('schedule variance' if c['key'] == 'schedule' else 'EVM')
                               + '; please update actuals per control.cadence before inspecting')
        for r in schedule_rows:
            r['status'] = 'N/A'
            r['variance'] = None
        escalations = [e for e in escalations if e not in ('schedule_slip', 'cpi', 'spi')]

    order = {'GREEN': 0, 'AMBER': 1, 'RED': 2, 'N/A': 0}
    overall = 'GREEN'
    for c in controls:
        if order[c['status']] > order[overall]:
            overall = c['status']
    return {
        'as_of': as_of.isoformat(),
        'overall_status': overall,
        'controls': controls,
        'escalations': escalations,
        'schedule_table': schedule_rows,
        'schedule_slip_pct': slip_pct,
        'metrics': {'bac': round(bac, 1), 'pv': round(pv, 1), 'ev': round(ev, 1),
                    'ac': round(ac_v, 1), 'spi': round(spi, 3),
                    'cpi': round(cpi, 3), 'eac': round(eac, 1), 'etc': round(etc, 1),
                    'vac': round(vac, 1),
                    'planned_pct': round(overall_planned, 1), 'actual_pct': round(overall_actual, 1)},
    }


project_path_global = None


def main():
    global project_path_global
    ap = argparse.ArgumentParser(description="PM Master operational control engine")
    ap.add_argument('--project', required=True)
    ap.add_argument('--as-of', default=None, help="Inspection baseline date ISO, defaults to today")
    ap.add_argument('--json', action='store_true', help="Output JSON only")
    ap.add_argument('--call-evm', action='store_true',
                    help="P1-3: cross-validate EVM figures using evm.py.compute (reuse independent module)")
    a = ap.parse_args()
    project_path_global = os.path.abspath(a.project)
    data = load(project_path_global)
    proj = data.get('project', {}) or {}
    bl = data.get('baseline') or {}
    blfile = bl.get('file')
    if not blfile:
        print("✗ Control engine aborted: project not yet baselined (no baseline pointer). Please run baseline.py --freeze first.",
              file=sys.stderr)
        sys.exit(3)
    bpath = blfile if os.path.isabs(blfile) else os.path.join(os.path.dirname(project_path_global), blfile)
    if not os.path.exists(bpath):
        print(f"✗ Control engine aborted: baseline file does not exist: {bpath}", file=sys.stderr)
        sys.exit(3)
    bdata = load(bpath)
    as_of = (parse_date((data.get('actuals') or {}).get('as_of'))
             or parse_date(a.as_of) or datetime.date.today())

    # Configured thresholds (M3): inject install-time config.operational_control into
    # data.control.thresholds; compute() reads it first. Project-level control.thresholds
    # can override further (tightening takes precedence).
    cfg = load_config() if 'load_config' in globals() else {}
    oc = (cfg.get('operational_control') or {}) if isinstance(cfg, dict) else {}
    if isinstance(oc, dict) and oc:
        ctrl = data.setdefault('control', {})
        cthr = ctrl.setdefault('thresholds', {})
        for k in ('spi_warn', 'cpi_warn', 'schedule_slip_warn_pct', 'open_change_high'):
            if k in oc and k not in cthr:
                try:
                    cthr[k] = float(oc[k])
                except (ValueError, TypeError):
                    pass

    result = compute(data, bdata, as_of)

    # ---- OAG: operational-period deliverable guardrail (deliverable drift detection) ----
    oag_violation = False
    try:
        if HERE not in sys.path:
            sys.path.insert(0, HERE)
        from artifact_guard import check_artifacts as _chk_art
        _ok, _viol, _ = _chk_art(project_path_global, data)
        if _ok:
            result['controls'].append({'name': 'Artifact Drift (OAG)',
                                       'status': 'OK',
                                       'detail': 'All deliverables consistent with source of truth'})
        else:
            _msg = '; '.join(_viol[:3]) + (' ...' if len(_viol) > 3 else '')
            result['controls'].append({'name': 'Artifact Drift (OAG)',
                                       'status': 'RED',
                                       'detail': f'{len(_viol)} deliverables not refreshed with source of truth: {_msg}'})
            result.setdefault('escalations', []).append('artifact-guard-violation(OAG)')
            oag_violation = True
    except Exception as _e:
        print(f"[OAG] check skipped: {_e}")

    # ---- P1-3: cross-validate EVM figures using evm.py ----
    if a.call_evm:
        try:
            if HERE not in sys.path:
                sys.path.insert(0, HERE)
            import evm as evm_mod
            m = result.get('metrics') or {}
            cross = evm_mod.compute(m.get('pv', 0), m.get('ev', 0), m.get('ac', 0), m.get('bac', 0))
            print("[call-evm] evm.py cross-validation:", json.dumps(cross, ensure_ascii=False))
        except Exception as _e:
            print(f"[call-evm] validation skipped: {_e}")

    out_root = os.path.dirname(project_path_global)
    arts = data.get('artifacts', {}) or {}
    crep = arts.get('control_report') or 'artifacts/control_report.md'
    # Render control report
    tmp = {'project': proj, 'as_of': result['as_of'], 'overall_status': result['overall_status'],
           'controls': result['controls'], 'escalations': result['escalations'],
           'schedule_table': result['schedule_table'],
           'schedule_slip_pct': result['schedule_slip_pct'],
           'schedule_note': f"Inspection baseline date {result['as_of']}; variance alert threshold +/-{result['schedule_slip_pct']:.0f}%."
                            f"{'Program level: aggregated by each SOW milestone.' if str(proj.get('type','')).lower()=='program' else 'Component level: detail down to leaf work packages.'}",
           'metrics': result['metrics'], 'baseline_on': bl.get('on'),
           'baseline_file': bl.get('file')}
    tmp_path = os.path.join(out_root, '.control_tmp.yaml')
    with open(tmp_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(tmp, f, allow_unicode=True, sort_keys=False)
    run([RENDER, '--template',
         os.path.join(HERE, '..', 'templates', 'common', 'control_report.md'),
         '--data', tmp_path, '--out', os.path.join(out_root, crep)])
    try:
        os.remove(tmp_path)
    except OSError:
        pass

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== Operational Control Report (as_of {result['as_of']}) ===")
        print(f"Overall status: {result['overall_status']}  | Baseline: {bl.get('on')}")
        print(f"Progress {result['metrics']['planned_pct']}%->{result['metrics']['actual_pct']}%  "
              f"SPI={result['metrics']['spi']} CPI={result['metrics']['cpi']}")
        for c in result['controls']:
            print(f"  [{c['status']:>5}] {c['name']}: {c['detail']}")
        if result['escalations']:
            print(f"⚠ Escalations: {', '.join(result['escalations'])}")
        print(f"Report rendered: {crep}")
    # Inspection write timestamp (E4: avoid duplicate inspections)
    data['last_control_check'] = as_of.isoformat() if hasattr(as_of, 'isoformat') else str(as_of)
    # Sync back to control block for backward compatibility
    (data.setdefault('control', {}))['last_control_check'] = data['last_control_check']
    with open(project_path_global, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    # Exit code: any RED escalation or artifact-guard violation -> 1 (can hook to scheduled-job alert)
    sys.exit(1 if (result['overall_status'] == 'RED' or oag_violation) else 0)


if __name__ == '__main__':
    main()
