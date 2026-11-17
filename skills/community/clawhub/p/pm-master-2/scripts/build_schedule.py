#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · WBS -> Schedule / Gantt generator
--------------------------------------------
Turn the WBS in `project.yaml` into a trackable schedule deliverable
(schedule_gantt.md) instead of only printing the critical path to stdout
(which is schedule_health.py's job).

Views (--level / --sow):
  - full (default; program auto-degrades to program): all schedulable tasks (skip summary packages).
  - program: program-level milestones only (tier: program SOW summary packages + phase milestones),
             focusing on program-level planning without expanding leaf details.
             Output plans/schedule_program_gantt.md.
  - sow <SOW_ID>: only that SOW's subtree (SOW summary package + its leaf packages + milestones that
             depend on it), output to plans/<sow>/schedule_gantt.md as "that SOW's own plan"
             (executable independently, linked to the parent project/program via project.name + SOW id).

What it does:
  1. Forward pass: using the project start date + each task's duration + dependencies (dependsOn)
     compute each task's earliest start (ES) / earliest finish (EF), yielding start/end dates.
     Dependencies outside the view are treated as satisfied and do not affect this view's scheduling.
  2. Write the computed start/end back to project.yaml's wbs[].start/end (single source of truth).
  3. Build the `tasks` list from the selected rows and render templates/waterfall/schedule_gantt.md.
  4. Write the artifact path back to project.yaml's artifacts (schedule_gantt / schedule_program /
     schedule_sow_<slug>).

Usage:
  python3 build_schedule.py --project /workspace/<slug>/project.yaml
  python3 build_schedule.py --project <yaml> --level program            # program-level schedule
  python3 build_schedule.py --project <yaml> --sow SOW1                 # single-SOW schedule (sub-plan)
  python3 build_schedule.py --project <yaml> --start 2026-08-01 --no-write-back
"""
import argparse
import os
import re
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import yaml
except ImportError:
    yaml = None

from schedule_health import _parse_deps, _parse_duration_days  # Reuse duration/dependency parsing


def _load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def _select_ids(wbs, level, sow_id, ptype):
    """Return the set of wbs ids to schedule for this view; None means all (full)."""
    if sow_id:
        inc = set()
        for w in wbs:
            wid = w.get('id')
            if not wid:
                continue
            if wid == sow_id or str(wid).startswith(sow_id + '.'):
                inc.add(wid)
        # Include milestones whose dependencies all fall within this set
        # (e.g. the SOW's go-live milestone)
        for w in wbs:
            wid = w.get('id')
            if wid in inc or not wid:
                continue
            deps = _parse_deps(w.get('dependsOn'))
            if w.get('milestone') and (not deps or all(d in inc for d in deps)):
                inc.add(wid)
        return inc
    if level == 'program' or (level == 'auto' and ptype == 'program'):
        inc = set()
        for w in wbs:
            if w.get('tier') == 'program' and w.get('id'):
                inc.add(w.get('id'))
        if not inc:  # Fallback: high-level view = summary packages + milestones
            for w in wbs:
                if (w.get('summary') or w.get('milestone')) and w.get('id'):
                    inc.add(w.get('id'))
        # When scheduling we must include all descendants of each SOW subtree so the
        # summary package's real span can be computed and leaf dates written back;
        # the render stage then filters by tier/milestone (showing only program-level rows).
        descendants = set()
        for w in wbs:
            wid = w.get('id')
            if not wid:
                continue
            for p in inc:
                if str(wid).startswith(p + '.') and wid != p:
                    descendants.add(wid)
        inc |= descendants
        return inc
    return None  # full


def _normalize_date_keys(w):
    """Normalize date keys: only `start`/`end` are canonical keys.
    Tolerate the historically/templately misused `finish` key — if a row has both
    `end` and `finish` and they conflict, `end` wins; if only `finish` exists,
    normalize `finish` to `end` and drop `finish` from the row.
    Return (start, end, warned), where warned is a list of warning messages.
    """
    warned = []
    start = w.get('start')
    end = w.get('end')
    finish = w.get('finish')
    if finish is not None:
        if end is None:
            end = finish
            warned.append(f"{w.get('id')}: non-canonical key `finish` normalized to `end`")
        elif str(end) != str(finish):
            warned.append(f"{w.get('id')}: `end`({end}) conflicts with `finish`({finish}); using `end`, discarding `finish`")
        # Drop finish in any case to avoid dual-key drift
        w.pop('finish', None)
    if 'finish' in w:
        w.pop('finish', None)
    return start, end, warned


def forward_schedule(wbs, project_start, include_ids=None):
    """Forward scheduling. Return {id: (start_date, end_date, is_milestone)}.

    When include_ids is not None, only rows in that set are scheduled; dependencies
    outside the set are treated as satisfied.
    If a package's in-set dependencies are incomplete (e.g. a program view lacking
    leaf detail) and its YAML already has real start/end, then **keep the existing
    dates** (do not reset to the start date) to avoid flattening an already-baselined
    schedule. But before keeping them, validate against predecessor/successor topology:
    if overridden (user entered wrong dates), reschedule and warn instead of silently
    keeping the wrong dates.
    """
    # First normalize date keys, collecting normalization warnings
    _date_warns = []
    for w in wbs:
        s, e, wn = _normalize_date_keys(w)
        _date_warns.extend(wn)
    if _date_warns:
        for wmsg in _date_warns:
            print(f"[schedule][warn] {wmsg}")
    orig = {w.get('id'): w for w in wbs}  # source of existing dates
    info = {}
    byid = {w.get('id'): w for w in wbs}
    for w in wbs:
        wid = w.get('id')
        if not wid:
            continue
        if include_ids is not None and wid not in include_ids:
            continue
        dur = _parse_duration_days(w)
        if dur == 0 and w.get('estimate'):
            # Leaf packages may only have estimate, not duration; use estimate as duration
            dur = _parse_duration_days({'duration': str(w.get('estimate', 0)) + 'd'})
        deps = _parse_deps(w.get('dependsOn'))
        milestone = bool(w.get('milestone')) or dur == 0
        is_summary = bool(w.get('summary'))
        # Summary packages are containers and contribute no sequential duration; their
        # span comes from rollup of children (for display); scheduled dur = 0
        sched_dur = 0 if is_summary else dur
        info[wid] = {'dur': sched_dur, 'deps': deps, 'milestone': milestone, 'summary': is_summary}

    es = {}
    changed = True
    guard = 0
    while changed and guard < 10000:
        changed = False
        guard += 1
        for tid, it in info.items():
            deps = it['deps']
            # Only wait for predecessors that are in-set and not yet scheduled;
            # out-of-set dependencies are treated as satisfied
            if any(d in info and es.get(d) is None for d in deps):
                continue
            new_s = 0
            for d in deps:
                if d in info and es.get(d) is not None:
                    new_s = max(new_s, es[d] + info[d]['dur'])
            if es.get(tid) != new_s:
                es[tid] = new_s
                changed = True

    result = {}
    # First compute leaf/non-summary spans; then roll up summary packages (summary) bottom-up
    for tid, it in info.items():
        off = es.get(tid, 0)
        o = orig.get(tid) or {}
        ostart = o.get('start'); oend = o.get('end')
        has_real = bool(ostart and oend)
        # Existing-date carry validation: keep only when (a) this package has no
        # predecessor-driven offset (offset==0) AND (b) existing dates do not exceed
        # any predecessor's end AND (c) existing end is not later than the earliest
        # successor start; otherwise reschedule and warn (avoid silent wrong dates).
        carry = (off == 0) and has_real
        if carry:
            try:
                cstart = datetime.date.fromisoformat(str(ostart)[:10])
                cend = datetime.date.fromisoformat(str(oend)[:10])
                # Topology conflict check: latest predecessor end must be <= this start;
                # earliest successor start must be >= this end
                pred_max_end = None
                for d in deps:
                    if d in result:
                        pred_max_end = cend if pred_max_end is None else max(pred_max_end, result[d][1])
                succ_min_start = None
                for t in wbs:
                    if t.get('id') in info and tid in _parse_deps(t.get('dependsOn')):
                        ts = result.get(t['id'])
                        if ts:
                            succ_min_start = ts[0] if succ_min_start is None else min(succ_min_start, ts[0])
                conflict = (pred_max_end is not None and cstart < pred_max_end) or \
                           (succ_min_start is not None and cend > succ_min_start)
                if conflict:
                    print(f"[schedule][warn] {tid} existing dates {cstart}-{cend} conflict with dependency topology; rescheduled")
                    carry = False
                if carry:
                    result[tid] = (cstart, cend, it['milestone'])
                    continue
            except (ValueError, TypeError):
                carry = False
        start = project_start + datetime.timedelta(days=off)
        if it['milestone']:
            end = start
        else:
            end = start + datetime.timedelta(days=it['dur'])
        result[tid] = (start, end, it['milestone'])
    # Roll up summary: take earliest start and latest end of (direct) children
    children = {}
    for tid, it in info.items():
        pass
    # Build parent->children (by id prefix, direct children only)
    childmap = {}
    for tid in info:
        for cand in info:
            if cand != tid and cand.startswith(tid + '.') and '.' not in cand[len(tid) + 1:]:
                childmap.setdefault(tid, []).append(cand)
    # Bottom-up (by descending '.' count)
    for tid in sorted(info, key=lambda x: -x.count('.')):
        if info[tid]['summary'] and not info[tid]['milestone']:
            kids = childmap.get(tid, [])
            if kids:
                starts = [result[k][0] for k in kids if result.get(k)]
                ends = [result[k][1] for k in kids if result.get(k)]
                if starts and ends:
                    s0 = min(starts); e0 = max(ends)
                    result[tid] = (s0, e0, False)
                    info[tid]['dur'] = (e0 - s0).days
    return result


def _fortnight_groups(tasks, project_start):
    """Aggregate tasks into 2-week buckets, returning [{label,start,end,tasks}]."""
    if not tasks:
        return []
    starts = []
    for t in tasks:
        try:
            starts.append(datetime.date.fromisoformat(str(t.get('start', ''))[:10]))
        except (ValueError, TypeError):
            pass
    if not starts:
        return []
    first = min(starts)
    last = max(starts)
    # Anchor on project start; one bucket every 14 days
    anchor = project_start
    groups = []
    wk = 1
    cur = anchor
    while cur <= last:
        nxt = cur + datetime.timedelta(days=14)
        gtasks = [t for t in tasks
                  if (t.get('start') and cur <= datetime.date.fromisoformat(str(t['start'])[:10]) < nxt)]
        groups.append({
            'label': f'FN{wk:02d} {cur.isoformat()}–{(nxt - datetime.timedelta(days=1)).isoformat()}',
            'start': cur.isoformat(),
            'end': (nxt - datetime.timedelta(days=1)).isoformat(),
            'tasks': gtasks,
            'count': len(gtasks),
            'task_ids': ' '.join(t.get('id', '') for t in gtasks),
        })
        cur = nxt
        wk += 1
    return groups


def main():
    ap = argparse.ArgumentParser(description="PM Master · WBS -> Schedule generator")
    ap.add_argument('--project', required=True, help="Single source of truth: project.yaml")
    ap.add_argument('--level', default='auto', choices=['auto', 'full', 'program'],
                    help="View: auto=by type / full=all / program=program milestone level")
    ap.add_argument('--sow', default=None, help="Schedule only this SOW's subtree (e.g. SOW1); output is that SOW's own plan")
    ap.add_argument('--start', default=None, help="Project start date ISO, e.g. 2026-08-01")
    ap.add_argument('--granularity', default='task', choices=['task', 'fortnight'],
                    help="Schedule granularity: task=by task (default); fortnight=aggregate by 2-week buckets")
    ap.add_argument('--out', default=None, help="Output .md path (overrides default)")
    ap.add_argument('--no-write-back', action='store_true', help="Only render the schedule; do not write back wbs dates to project.yaml")
    ap.add_argument('--template', default=None, help="Schedule template path")
    a = ap.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML required: run `pip install pyyaml`")

    data = _load(a.project)
    wbs = data.get('wbs') or []
    if not wbs:
        raise SystemExit("⚠ No wbs found in project.yaml; cannot generate schedule (complete the WBS decomposition first).")

    ptype = (data.get('project') or {}).get('type', 'project')
    include_ids = _select_ids(wbs, a.level, a.sow, ptype)
    # Render set: program view shows only tier==program rows + milestones
    # (descendant leaves are scheduled but not rendered)
    render_ids = set(include_ids) if include_ids is not None else None
    if a.level == 'program' or (a.level == 'auto' and ptype == 'program' and a.sow is None):
        render_ids = set()
        for w in wbs:
            if w.get('id') in include_ids and (w.get('tier') == 'program' or w.get('milestone')):
                render_ids.add(w.get('id'))

    start_iso = a.start or (data.get('project') or {}).get('start_date')
    if start_iso:
        try:
            project_start = datetime.date.fromisoformat(str(start_iso)[:10])
        except ValueError:
            raise SystemExit(f"Invalid --start / project.start_date: {start_iso}")
    else:
        project_start = datetime.date.today()
        print(f"[schedule] No start date given; using today {project_start.isoformat()} (use --start or set project.start_date).")

    sched = forward_schedule(wbs, project_start, include_ids)

    if not a.no_write_back and include_ids is None and a.level in ('auto', 'full'):
        # Only the full view (with the complete leaf graph) writes back dates;
        # program/SOW views are read-only and do not alter the index
        for w in wbs:
            tid = w.get('id')
            if tid in sched:
                s, e, _ = sched[tid]
                w['start'] = s.isoformat()
                w['end'] = e.isoformat()

    # Build tasks: full skips summary; program/sow filter by render_ids
    # (program shows only tier==program + milestones)
    tasks = []
    for w in wbs:
        tid = w.get('id')
        if not tid:
            continue
        if render_ids is not None:
            if tid not in render_ids:
                continue
        else:
            if w.get('summary'):
                continue
        s, e, milestone = sched.get(tid, (None, None, False))
        # duration uses the recomputed real duration (summary = child rollup span; leaf = own duration)
        dur = (e - s).days if (s and e) else _parse_duration_days(w)
        tasks.append({
            'id': tid,
            'name': w.get('name', tid),
            'duration': dur,
            'is_summary': bool(w.get('summary')),
            'deps': _parse_deps(w.get('dependsOn')),
            'start': s.isoformat() if s else (w.get('start') or ''),
            'end': e.isoformat() if e else (w.get('end') or ''),
            'milestone': milestone,
        })

    if not tasks:
        raise SystemExit("⚠ No schedulable tasks under this view (check wbs tier / summary / milestone flags).")

    # View label + output path
    if a.sow:
        view_label = f'SOW {a.sow}'
        slug = str(a.sow).replace('.', '_')
        out_def = os.path.join('plans', slug, 'schedule_gantt.md')
        art_key = f'schedule_sow_{slug}'
    elif include_ids is not None:  # program
        view_label = 'Program'
        out_def = os.path.join('plans', 'schedule_program_gantt.md')
        art_key = 'schedule_program'
    else:
        view_label = 'Project'
        out_def = os.path.join('plans', 'schedule_gantt.md')
        art_key = 'schedule_gantt'

    # Pillar 2: milestone coverage — the set of activities directly attributed to each milestone
    milestone_coverage = []
    byid = {w.get('id'): w for w in wbs}
    ms_map = {w.get('id'): w for w in wbs if w.get('milestone')}
    for m in ms_map.values():
        mid_ = m.get('id')
        leaves = []
        for w in wbs:
            if w.get('summary') or w.get('milestone') or w.get('tier') == 'program':
                continue
            mref = w.get('milestone_ref')
            if mref == mid_:
                leaves.append(w.get('id'))
                continue
            deps = _parse_deps(w.get('dependsOn'))
            # A dependency endpoint (chain tail with no predecessor) landing on the milestone also counts
            if mid_ in deps:
                leaves.append(w.get('id'))
        b = m.get('billing') or {}
        milestone_coverage.append({
            'id': mid_,
            'name': m.get('name', mid_),
            'payment_id': b.get('payment_id'),
            'fee': b.get('fee_inr') or b.get('fee'),
            'fee_type': b.get('fee_type'),
            'date': sched.get(mid_, (None, None, False))[0].isoformat() if mid_ in sched else (m.get('start') or ''),
            'leaves': leaves,
            'leaf_count': len(leaves),
        })
    # Pillar 4: payment<->schedule linkage — each fixed-fee payment line + its milestone +
    # scheduled date vs contract due_date
    payment_linkage = []
    prog = data.get('program') or {}
    sows_src = (prog.get('sows') or []) + (data.get('sow_map') or [])
    for s in sows_src:
        fee = s.get('fee')
        if isinstance(fee, str):
            fee = re.sub(r'[^0-9.]', '', fee) or '0'
        try:
            fee_v = float(fee)
        except (TypeError, ValueError):
            fee_v = 0.0
        ft = s.get('fee_type')
        if ft != 'fixed' or fee_v <= 0:
            continue
        sid = s.get('sow')
        # All billable milestones under this SOW
        ms_for_sow = [mc for mc in milestone_coverage if mc['payment_id'] and str(mc['id']).startswith(sid + '.')]
        for mc in ms_for_sow:
            # A milestone billing (fixed) with no independent contract calendar -> payment
            # falls due when the milestone is achieved (collection rhythm = delivery rhythm);
            # if the contract explicitly gives a due_date, compare against the contract calendar
            # (can trigger drift).
            due = (s.get('due_date') or (s.get('billing') or {}).get('due_date') or mc['date'])
            payment_linkage.append({
                'sow': sid,
                'payment_id': mc['payment_id'],
                'milestone': mc['id'],
                'scheduled': mc['date'],
                'contract_due': due or '',
                'fee': mc['fee'],
                'status': ('linked' if (due and mc['date'] and mc['date'] <= due) else ('drift' if due else 'no-due')),
            })
    if not payment_linkage:
        # Single-tier project: use billing milestones directly
        for mc in milestone_coverage:
            if mc['fee_type'] == 'fixed' and mc['fee']:
                payment_linkage.append({
                    'sow': str(mc['id']).split('.')[0],
                    'payment_id': mc['payment_id'] or mc['id'],
                    'milestone': mc['id'],
                    'scheduled': mc['date'],
                    'contract_due': '',
                    'fee': mc['fee'],
                    'status': 'no-due',
                })

    tpl_path = a.template or os.path.join(SCRIPT_DIR, '..', 'templates', 'waterfall', 'schedule_gantt.md')
    tpl_path = os.path.abspath(tpl_path)
    if not os.path.exists(tpl_path):
        raise SystemExit(f"Schedule template not found: {tpl_path}")
    with open(tpl_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    from render import render
    ctx = {'project': data.get('project', {}), 'view_label': view_label,
           'tasks': tasks, 'granularity': a.granularity,
           'milestone_coverage': milestone_coverage, 'payment_linkage': payment_linkage}
    if a.granularity == 'fortnight':
        ctx['fortnight_groups'] = _fortnight_groups(tasks, project_start)
    rendered = render(tpl, ctx)

    root = os.path.dirname(os.path.abspath(a.project))
    out_path = a.out or os.path.join(root, out_def)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    rel = os.path.relpath(out_path, root)
    if 'artifacts' not in data or not isinstance(data['artifacts'], dict):
        data['artifacts'] = {}
    data['artifacts'][art_key] = rel
    _save(a.project, data)

    print(f"[schedule] Schedule generated ({view_label} view, {len(tasks)} tasks, project start {project_start.isoformat()}): {out_path}")
    print(f"[schedule] artifacts.{art_key} = {rel}")


if __name__ == '__main__':
    main()
