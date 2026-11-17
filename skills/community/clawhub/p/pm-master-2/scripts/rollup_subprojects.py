#!/usr/bin/env python3
"""rollup_subprojects.py — Cross-subproject rollup (milestones/subprojects split architecture).

Reads each subproject's project.yaml (located at <program>/subprojects/<sowN>/project.yaml),
rolls up milestone status, health metrics, and EAC/cost, and produces a program-level view.

Usage:
  python3 rollup_subprojects.py --program <program_dir> [--json]
"""
import argparse
import os
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _status_from_control(ctrl):
    """Infer overall status (GREEN/AMBER/RED) from control_engine output or metrics."""
    if not isinstance(ctrl, dict):
        return 'UNKNOWN'
    for k in ('overall', 'status'):
        v = ctrl.get(k)
        if v in ('GREEN', 'AMBER', 'RED'):
            return v
    return 'UNKNOWN'


def rollup(program_dir):
    subs = []
    sub_root = os.path.join(program_dir, 'subprojects')
    if not os.path.isdir(sub_root):
        sub_root = program_dir  # may also be passed a directory containing multiple project.yaml files
    for name in sorted(os.listdir(sub_root)):
        py = os.path.join(sub_root, name, 'project.yaml')
        if not os.path.isfile(py):
            continue
        try:
            d = _load(py)
        except Exception:
            subs.append({'id': name, 'error': 'parse failed'})
            continue
        proj = d.get('project') or {}
        metrics = d.get('metrics') or {}
        evm = metrics.get('evm') or {}
        actuals = d.get('actuals') or {}
        wbs = d.get('wbs') or []
        # Milestone statistics (derived from wbs)
        ms_done = ms_total = 0
        for w in wbs:
            if w.get('milestone'):
                ms_total += 1
                wp = actuals.get('wbs_progress', {}).get(w.get('id'))
                try:
                    if float(wp or 0) >= 100:
                        ms_done += 1
                except (TypeError, ValueError):
                    pass
        subs.append({
            'id': proj.get('id') or name,
            'name': proj.get('name') or name,
            'lifecycle': proj.get('lifecycle_state'),
            'type': proj.get('type'),
            'start': proj.get('start_date'),
            'target_end': proj.get('target_end'),
            'milestones': {'done': ms_done, 'total': ms_total},
            'bac': evm.get('bac') or 0,
            'ev': evm.get('ev') or actuals.get('ev') or 0,
            'ac': actuals.get('ac') or 0,
            'eac': evm.get('eac') or 0,
            'cpi': evm.get('cpi'),
            'spi': evm.get('spi'),
            'status': _status_from_control(metrics.get('control')),
        })
    # Rollup
    tot_bac = sum(s.get('bac', 0) or 0 for s in subs)
    tot_ev = sum(s.get('ev', 0) or 0 for s in subs)
    tot_ac = sum(s.get('ac', 0) or 0 for s in subs)
    tot_eac = sum(s.get('eac', 0) or 0 for s in subs)
    roll = {
        'subprojects': subs,
        'summary': {
            'count': len(subs),
            'bac': tot_bac,
            'ev': tot_ev,
            'ac': tot_ac,
            'eac': tot_eac,
            'cpi': (tot_ev / tot_ac) if tot_ac else None,
            'eac_vs_bac_var': (tot_bac - tot_eac) if tot_eac else None,
        },
    }
    return roll


def main():
    ap = argparse.ArgumentParser(description="Cross-subproject rollup")
    ap.add_argument('--program', required=True, help="Program directory (containing subprojects/)")
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    roll = rollup(a.program)
    if a.json:
        print(yaml.safe_dump(roll, allow_unicode=True, sort_keys=False))
        return
    print(f"=== Subproject rollup ({roll['summary']['count']} total) ===")
    print(f"{'ID':<10}{'Milestone':>10}{'BAC':>14}{'EV':>14}{'AC':>14}{'EAC':>14}{'Status':>8}")
    for s in roll['subprojects']:
        m = s.get('milestones', {})
        print(f"{str(s['id']):<10}{str(m.get('done',0))+'/'+str(m.get('total',0)):>10}"
              f"{s.get('bac',0) or 0:>14.0f}{s.get('ev',0) or 0:>14.0f}"
              f"{s.get('ac',0) or 0:>14.0f}{s.get('eac',0) or 0:>14.0f}{'':>3}{s.get('status','')}")
    sm = roll['summary']
    print(f"{'Total':<10}{'':>10}{sm['bac']:>14.0f}{sm['ev']:>14.0f}{sm['ac']:>14.0f}{sm['eac']:>14.0f}")
    if sm.get('cpi') is not None:
        var = sm.get('eac_vs_bac_var')
        var_txt = f"{var:.0f}" if isinstance(var, (int, float)) else 'n/a'
        print(f"Program CPI (estimate)={sm['cpi']:.3f}  EAC vs BAC variance={var_txt}")


if __name__ == '__main__':
    main()
