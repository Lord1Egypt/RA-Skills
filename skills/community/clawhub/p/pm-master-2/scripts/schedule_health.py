#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Schedule Health Check
-------------------------------------------------
Two input modes:
  A. Standalone schedule file: --data schedule.yaml(.json), a tasks list, each item:
       id, name, duration(days), deps: [predecessor task ids...]   (deps optional)
     Optional: start(project start date, ISO) used to derive each task's dates.
  B. Single source of truth: --project project.yaml — derive the schedule network
     directly from its wbs:
     - duration: prefer the start/end date difference (calendar days); otherwise
       parse the duration field ("N wks" -> N*7 days; "Gate" -> 0).
     - deps: parse the dependsOn of each wbs row (accepts both list and
       comma-separated string).

Output:
  - Missing/unknown dependency warnings
  - Critical path (longest-duration path)
  - Each task's early start/finish, late start/finish, slack

Usage:
  python3 schedule_health.py --data schedule.yaml [--start 2025-08-01]
  python3 schedule_health.py --project /workspace/<slug>/project.yaml
"""
import argparse
import json
import re
import sys
import datetime
from collections import defaultdict

try:
    import yaml
except ImportError:
    yaml = None


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    if path.endswith(('.yaml', '.yml')):
        return yaml.safe_load(raw)
    return json.loads(raw)


def _parse_deps(dep):
    """dependsOn accepts both a list and a comma-separated string."""
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


def _parse_duration_days(item):
    """Prefer the start/end date difference; otherwise parse the duration field."""
    s, e = item.get('start'), item.get('end')
    if s and e:
        try:
            d0 = datetime.date.fromisoformat(str(s)[:10])
            d1 = datetime.date.fromisoformat(str(e)[:10])
            return max((d1 - d0).days, 0)
        except ValueError:
            pass
    dur = str(item.get('duration', '') or '')
    m = re.search(r'(\d+(?:\.\d+)?)\s*w', dur, re.I)
    if m:
        return int(float(m.group(1)) * 7)  # weeks -> calendar days
    m = re.search(r'(\d+(?:\.\d+)?)\s*d', dur, re.I)
    if m:
        return int(float(m.group(1)))
    if 'gate' in dur.lower():
        return 0
    m = re.search(r'(\d+(?:\.\d+)?)', dur)
    return int(float(m.group(1))) if m else 0


def tasks_from_project(data):
    """Derive the tasks list from project.yaml's wbs."""
    wbs = data.get('wbs') or []
    tasks = []
    for w in wbs:
        tasks.append({
            'id': w.get('id'),
            'name': w.get('name', w.get('id')),
            'duration': _parse_duration_days(w),
            'deps': _parse_deps(w.get('dependsOn')),
            'start': w.get('start'),
            'end': w.get('end'),
            'children': w.get('children'),
        })
    return tasks


def main():
    ap = argparse.ArgumentParser(description="PM Master schedule health check")
    ap.add_argument('--data', default=None, help="Standalone schedule file schedule.yaml(.json)")
    ap.add_argument('--project', default=None, help="Single source of truth project.yaml (reads wbs directly)")
    ap.add_argument('--start', default=None, help="Project start date ISO, e.g. 2025-08-01")
    a = ap.parse_args()
    if not a.data and not a.project:
        ap.error("You must provide one of --data or --project")

    if a.project:
        d = load(a.project)
        task_list = tasks_from_project(d)
        if not task_list:
            print("⚠ No wbs schedule data found in project.yaml; cannot compute critical path.")
            sys.exit(1)
    else:
        d = load(a.data)
        task_list = d.get('tasks', [])

    tasks = {t['id']: t for t in task_list}
    deps = {tid: t.get('deps', []) for tid, t in tasks.items()}

    issues = []
    for tid, ds in deps.items():
        for dep in ds:
            if dep not in tasks:
                issues.append(f"Task {tid} depends on unknown task {dep}")

    # ---- Cycle detection (Kahn topological sort; unprocessed nodes = cyclic dependency) ----
    indeg = {tid: 0 for tid in tasks}
    for tid, ds in deps.items():
        for p in ds:
            if p in tasks:
                indeg[tid] += 1
    topo = []
    queue = [t for t in tasks if indeg[t] == 0]
    while queue:
        n = queue.pop(0)
        topo.append(n)
        for t in tasks:
            if n in deps.get(t, []):
                indeg[t] -= 1
                if indeg[t] == 0:
                    queue.append(t)
    cyclic = [t for t in tasks if t not in topo]
    if cyclic:
        # Locate the edges forming the cycle (dependency points into a cycle node) to help the user fix it
        cycle_edges = []
        for t in cyclic:
            for d in deps[t]:
                if d in cyclic:
                    cycle_edges.append(f"{t} -> {d}")
        issues.append("⚠ Cyclic dependency detected (cannot be scheduled); please break one of the following edges: "
                      + "; ".join(cycle_edges[:12]) + ("..." if len(cycle_edges) > 12 else ""))

    # ---- Prefer calendar start/end already present in project.yaml for slack ----
    # When a row has both deps and real start/end, the calendar dates take precedence
    # (respecting build_schedule's wave parallelism); otherwise fall back to the
    # sequential model (duration accumulation). The two models must not be mixed,
    # to avoid distorting the "total project duration" basis.
    # Only leaf tasks (no children) with calendar dates are counted; a summary row
    # with children counts as "having" dates even if it has none.
    leaf_tasks = [t for t in tasks if t not in cyclic and not tasks[t].get('children')]
    have_calendar = all((tasks[t].get('start') and tasks[t].get('end')) for t in leaf_tasks)
    cal_start = {}
    cal_end = {}
    for t in tasks:
        s = tasks[t].get('start'); e = tasks[t].get('end')
        if s and e:
            try:
                cal_start[t] = datetime.date.fromisoformat(str(s)[:10])
                cal_end[t] = datetime.date.fromisoformat(str(e)[:10])
            except (ValueError, TypeError):
                pass
    use_calendar = have_calendar and len(cal_start) > 0

    if use_calendar:
        # Slack = allowed latest finish - planned finish (in calendar days, not sequential days)
        # LF back-propagation: a node with no successor has LF = project latest end; otherwise LF = min(successor LS)
        # First compute the project baseline (earliest start and latest end), used for LF of successor-less nodes
        proj_min = min(cal_start.values())
        proj_max = max(cal_end.values())
        # Forward: planned day offset (relative to proj_min)
        def dayoff(d):
            return (d - proj_min).days
        es = {t: dayoff(cal_start[t]) for t in cal_start}
        ef = {t: dayoff(cal_end[t]) for t in cal_end}
        # Backward LF/LS (only on the acyclic subgraph; skip cyclic nodes to avoid crashing)
        lf, ls = {}, {}
        succ_of = {t: [] for t in tasks}
        for t in topo:
            for d in deps[t]:
                if d in topo:
                    succ_of[d].append(t)
        for tid in reversed(topo):
            succ = succ_of.get(tid, [])
            if not succ:
                # No successor: LF = offset of project latest end
                lf[tid] = dayoff(proj_max)
            else:
                lf[tid] = min(ls[s] for s in succ)
            ls[tid] = lf[tid] - (ef[tid] - es[tid])
        model_label = "Calendar model (respects wave parallelism; start/end from project.yaml)"
        project_end = dayoff(proj_max)
    else:
        # Sequential model (when no calendar dates)
        es, ef = {}, {}
        for tid in topo:
            dur = tasks[tid].get('duration', 0)
            start = 0
            for p in deps[tid]:
                if p in ef:
                    start = max(start, ef[p])
            es[tid], ef[tid] = start, start + dur
        project_end = max(ef.values()) if ef else 0
        lf, ls = {}, {}
        for tid in reversed(topo):
            succ = [t for t in topo if tid in deps.get(t, [])]
            if not succ:
                lf[tid] = project_end
            else:
                lf[tid] = min(ls[s] for s in succ)
            ls[tid] = lf[tid] - tasks[tid].get('duration', 0)
        model_label = "Sequential model (duration accumulation; upper-bound estimate when no start/end)"

    print("=== Schedule Health ===")
    if issues:
        print("⚠ Dependency issues:")
        for i in issues:
            print("  -", i)
    else:
        print("✓ Dependencies complete")
    print(f"Schedule model: {model_label}")
    print(f"Total project duration (calendar days): {project_end} days")
    print(f"{'ID':<8}{'Name':<14}{'ES':>4}{'EF':>4}{'LS':>4}{'LF':>4}{'Slack':>6}  Critical?")
    crit_path = []
    for tid in topo:
        if tid not in es:
            print(f"{tid:<8}{tasks[tid].get('name',''):<14}  (cannot schedule: missing predecessor or in cycle)")
            continue
        slack = ls[tid] - es[tid]
        crit = '*' if slack == 0 else ''
        if crit:
            crit_path.append(tid)
        print(f"{tid:<8}{str(tasks[tid].get('name',''))[:12]:<14}"
              f"{es[tid]:>4}{ef[tid]:>4}{ls[tid]:>4}{lf[tid]:>4}{slack:>6}   {crit}")
    for tid in cyclic:
        print(f"{tid:<8}{tasks[tid].get('name',''):<14}  (cyclic dependency, excluded from critical path)")
    print("Critical path:", " -> ".join(crit_path) if crit_path else "none")
    if cyclic:
        print("⚠ Note: nodes with cyclic dependencies were not included in the critical path calculation; re-run after fixing to get full results.")


if __name__ == '__main__':
    main()
