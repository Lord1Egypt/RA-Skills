#!/usr/bin/env python3
"""
meeting_load.py — ICS-based meeting audit: hours, fragmentation, series cost, prescriptions.

Pure stdlib. Handles VEVENT with DTSTART/DTEND or DURATION, RRULE (DAILY/WEEKLY/
BIWEEKLY-ish INTERVALs, BYDAY, COUNT/UNTIL), EXDATE, cancelled events, attendees.
Exotic recurrence rules fall back to a weekly approximation (flagged).
"""
import argparse
import datetime as dt
import sys
from collections import defaultdict

WEEKDAY_MAP = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5, "SU": 6}

# ---------------------------------------------------------------- ics parsing

def unfold(text):
    out = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if line[:1] in (" ", "\t") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def parse_dt(value, tz=None):
    # formats: YYYYMMDD, YYYYMMDDTHHMMSS(Z), with optional ;VALUE=DATE handled by caller
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1]
        naive = True
    else:
        naive = True
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%d"):
        try:
            d = dt.datetime.strptime(v, fmt)
            return d
        except ValueError:
            continue
    raise ValueError(f"unparseable datetime {value!r}")


def parse_dur(value):
    # e.g. PT1H30M, PT45M, P1D
    import re
    m = re.match(r"^([+-])?P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$", value.strip())
    if not m:
        raise ValueError(f"unparseable duration {value!r}")
    days, h, mi, s = (int(x) if x else 0 for x in m.group(2, 3, 4, 5))
    return dt.timedelta(days=days, hours=h, minutes=mi, seconds=s)


def parse_ics(path):
    """Return list of event dicts: uid, summary, start, end, duration, attendees,
    cancelled, rrule(dict|None), exdates(set), all_day."""
    text = open(path, encoding="utf-8", errors="replace").read()
    events = []
    cur = None
    for line in unfold(text):
        if line.startswith("BEGIN:VEVENT"):
            cur = {"attendees": [], "exdates": set(), "rrule": None,
                   "cancelled": False, "all_day": False}
        elif line.startswith("END:VEVENT"):
            if cur is not None:
                events.append(cur)
            cur = None
        elif cur is not None and ":" in line:
            name_full, _, value = line.partition(":")
            name, *params = name_full.split(";")
            name = name.upper()
            if name == "UID":
                cur["uid"] = value.strip()
            elif name == "SUMMARY":
                cur["summary"] = value.strip()
            elif name == "DTSTART":
                cur["start"] = parse_dt(value)
                if "VALUE=DATE" in name_full.upper() and "T" not in value:
                    cur["all_day"] = True
            elif name == "DTEND":
                cur["end"] = parse_dt(value)
            elif name == "DURATION":
                cur["duration"] = parse_dur(value)
            elif name == "ATTENDEE":
                for p in params:
                    if p.upper().startswith("CN="):
                        cur["attendees"].append(p[3:].strip().strip('"'))
                        break
                else:
                    cur["attendees"].append(value.strip().removeprefix("mailto:"))
            elif name == "STATUS":
                if value.strip().upper() == "CANCELLED":
                    cur["cancelled"] = True
            elif name == "RRULE":
                rule = {}
                for part in value.strip().split(";"):
                    if "=" in part:
                        k, v = part.split("=", 1)
                        rule[k.upper()] = v
                cur["rrule"] = rule
            elif name == "EXDATE":
                for piece in value.split(","):
                    try:
                        cur["exdates"].add(parse_dt(piece).date())
                    except ValueError:
                        pass
    # finalize durations
    for e in events:
        if "end" not in e and "duration" in e:
            e["end"] = e["start"] + e["duration"]
        elif "end" in e:
            e["duration"] = e["end"] - e["start"]
        else:
            e["end"] = e["start"]
            e["duration"] = dt.timedelta(0)
    return events


def expand(event, window_start, window_end):
    """Expand an event (with optional RRULE) into concrete occurrences within window."""
    occs = []
    start = event["start"]

    def add(s):
        if window_start <= s <= window_end and s.date() not in event["exdates"]:
            occs.append({"summary": event.get("summary", "(untitled)"),
                         "uid": event.get("uid", ""),
                         "start": s,
                         "end": s + event["duration"],
                         "minutes": event["duration"].total_seconds() / 60,
                         "attendees": event["attendees"],
                         "cancelled": event["cancelled"],
                         "all_day": event["all_day"]})

    rule = event["rrule"]
    if not rule:
        add(start)
        return [o for o in occs if not o["cancelled"]]

    freq = rule.get("FREQ", "").upper()
    interval = int(rule.get("INTERVAL", "1") or 1)
    count = int(rule["COUNT"]) if "COUNT" in rule else None
    until = parse_dt(rule["UNTIL"]) if "UNTIL" in rule else None
    byday = [WEEKDAY_MAP[d.strip()[-2:]] for d in rule["BYDAY"].split(",")] if "BYDAY" in rule else None

    if freq in ("DAILY",):
        cur, i = start, 0
        while (until is None or cur <= until) and (count is None or i < count) and cur <= window_end:
            add(cur)
            cur += dt.timedelta(days=interval)
            i += 1
    elif freq in ("WEEKLY", "MONTHLY", "YEARLY"):
        step_weeks = interval if freq == "WEEKLY" else interval * (4 if freq == "MONTHLY" else 52)
        # anchor: first week/day of the pattern
        anchor = start
        i = 0
        while anchor <= window_end and (count is None or i < count) and (until is None or anchor <= until):
            if freq == "WEEKLY" and byday:
                week_start = dt.datetime.combine(
                    anchor.date() - dt.timedelta(days=anchor.weekday()), dt.time(0))
                for wd in sorted(byday):
                    occ = week_start + dt.timedelta(days=wd,
                                                    hours=anchor.hour, minutes=anchor.minute)
                    if occ >= anchor or anchor.weekday() == wd:
                        if count is None or i < count:
                            add(occ)
                            i += 1
            else:
                add(anchor)
                i += 1
            anchor += dt.timedelta(weeks=step_weeks)
    else:
        add(start)
    return [o for o in occs if not o["cancelled"] and not o["all_day"]]


def load_occurrences(paths, weeks, args):
    window_end = dt.datetime.combine(dt.date.today(), dt.time(23, 59))
    window_start = window_end - dt.timedelta(weeks=weeks)
    occs = []
    approximate = False
    for p in paths:
        for e in parse_ics(p):
            if e.get("all_day") and not getattr(args, "include_allday", False):
                continue
            if "start" not in e:
                continue
            before = len(occs)
            occs.extend(expand(e, window_start, window_end))
            rule = e.get("rrule") or {}
            if rule.get("FREQ", "").upper() not in ("", "DAILY", "WEEKLY") or "BYSETPOS" in rule:
                approximate = True
    return occs, window_start, window_end, approximate

# ---------------------------------------------------------------- analysis

def in_work_hours(o, args):
    return (o["start"].weekday() < 5 and
            args.day_start <= o["start"].hour < args.day_end)


def meeting_minutes(occs, args, person=None):
    tot = 0
    by_day = defaultdict(int)
    by_series = defaultdict(lambda: {"min": 0, "n": 0, "attendees": 0})
    for o in occs:
        if person and person.lower() not in [a.lower() for a in o["attendees"]] and not person_is_organizer_default(o, person):
            continue
        if o["start"].weekday() >= 5:
            continue
        tot += o["minutes"]
        by_day[o["start"].strftime("%a")] += o["minutes"]
        s = by_series[(o["uid"], o["summary"])]
        s["min"] += o["minutes"]
        s["n"] += 1
        s["attendees"] = max(s["attendees"], len(o["attendees"]) or 1)
    return tot, by_day, by_series


def person_is_organizer_default(o, person):
    # without ORGANIZER parsing, count events with no attendee list for the single
    # calendar owner (personal export) — the common case
    return not o["attendees"]


def focus_blocks(occs, args, person=None, dates=None):
    """For each workday: longest meeting-free run and usable blocks.
    If `dates` given, analyze exactly those dates (for before/after comparison)."""
    days = defaultdict(list)
    for o in occs:
        if person and person.lower() not in [a.lower() for a in o["attendees"]] and o["attendees"]:
            continue
        if o["start"].weekday() < 5:
            days[o["start"].date()].append((o["start"], o["end"]))
    if dates is None:
        dates = sorted(days.keys())
    out = []
    for d in dates:
        if d.weekday() >= 5:
            continue
        busy = days.get(d, [])
        work_start = dt.datetime.combine(d, dt.time(args.day_start))
        work_end = dt.datetime.combine(d, dt.time(args.day_end))
        # clamp busy intervals to the work window; drop meetings entirely outside it
        clamped = []
        for s, e in busy:
            s2, e2 = max(s, work_start), min(e, work_end)
            if e2 > s2:
                clamped.append((s2, e2))
        clamped.sort()
        gaps = []
        cur = work_start
        for s, e in clamped:
            if s > cur:
                gaps.append((cur, s))
            cur = max(cur, e)
        if work_end > cur:
            gaps.append((cur, work_end))
        longest = max(((e - s).total_seconds() / 60 for s, e in gaps), default=0)
        usable = sum(1 for s, e in gaps if (e - s).total_seconds() / 60 >= args.block_min)
        fragmented = (work_end - work_start).total_seconds() / 60 - longest
        out.append({"date": d, "longest_min": longest, "blocks": usable,
                    "fragmented_min": fragmented, "n_meetings": len(clamped)})
    return out


def double_booked_minutes(occs):
    occs = sorted(occs, key=lambda o: o["start"])
    total = 0.0
    active = []
    for o in occs:
        active = [a for a in active if a["end"] > o["start"]]
        if active:
            overlap = min(a["end"] for a in active)
            if o["end"] > overlap:
                total += (o["end"] - overlap).total_seconds() / 60
        active.append(o)
    return total

# ---------------------------------------------------------------- commands

def cmd_stats(a):
    occs, wstart, wend, approx = load_occurrences(a.ics, a.weeks, a)
    tot, by_day, by_series = meeting_minutes(occs, a, a.person)
    weeks = a.weeks
    print(f"Meeting load — {len(occs)} occurrences, {weeks} weeks "
          f"({wstart.date()} → {wend.date()})")
    if approx:
        print("  (note: exotic recurrence approximated — sanity-check counts)")
    if not occs:
        return
    print(f"  meeting time: {tot/60:.1f} h total  =  {tot/weeks/60:.1f} h/week"
          f"  ({tot/weeks/60/40*100:.0f}% of a 40h week)")
    print(f"  double-booked: {double_booked_minutes(occs)/weeks:.0f} min/week")
    print("  by weekday:")
    for wd in ("Mon", "Tue", "Wed", "Thu", "Fri"):
        if by_day.get(wd):
            print(f"    {wd} {by_day[wd]/weeks/60:.1f} h/week")
    if len(by_series) > 1:
        print(f"  top series:")
        for (uid, name), s in sorted(by_series.items(), key=lambda kv: -kv[1]["min"])[:5]:
            print(f"    {s['min']/weeks/60:.1f} h/wk  ×{s['attendees']}ppl  {name[:48]}")


def cmd_focus(a):
    occs, wstart, wend, _ = load_occurrences(a.ics, a.weeks, a)
    rows = focus_blocks(occs, a, a.person)
    if not rows:
        print("(no weekday meetings in window)")
        return
    weeks = max(1, a.weeks)
    blocks = sum(r["blocks"] for r in rows) / weeks
    frag = sum(r["fragmented_min"] for r in rows) / weeks / 60
    print(f"Focus analysis (working {a.day_start:02d}:00–{a.day_end:02d}:00, "
          f"block ≥{a.block_min} min):")
    print(f"  focus blocks: {blocks:.1f}/week   fragmentation: {frag:.1f} h/week")
    for r in rows[-10:]:
        print(f"    {r['date']} {r['date'].strftime('%a')}  longest block "
              f"{r['longest_min']:.0f}min  usable blocks {r['blocks']}  "
              f"meetings {r['n_meetings']}")
    if a.advice:
        worst = max(rows, key=lambda r: r["fragmented_min"])
        print(f"\n  worst day: {worst['date']} — batch meetings into 1–2 clusters;")
        print(f"  protect one {a.block_min}-min+ block as 'focus' recurring event")


def cmd_rank(a):
    occs, wstart, wend, _ = load_occurrences(a.ics, a.weeks, a)
    _, _, by_series = meeting_minutes(occs, a, a.person)
    if not by_series:
        print("(no meetings)")
        return
    rows = []
    for (uid, name), s in by_series.items():
        per_occ = s["attendees"] * (s["min"] / max(1, s["n"]))
        density = s["n"] / a.weeks
        rows.append((per_occ * s["n"] / a.weeks, per_occ, density, name, s))
    rows.sort(reverse=True)
    print(f"{'person-hrs/wk':>13}  {'per-occ':>8}  {'/wk':>4}  series")
    for cost, per_occ, density, name, s in rows:
        print(f"{cost:>13.1f}  {per_occ:>7.1f}h  {density:>4.1f}  "
              f"{name[:44]}  ({s['attendees']}ppl)")


def cmd_prescribe(a):
    occs, wstart, wend, _ = load_occurrences(a.ics, a.weeks, a)
    _, _, by_series = meeting_minutes(occs, a, a.person)
    if not by_series:
        print("(no meetings)")
        return
    print(f"PRESCRIPTIONS ({sum(s['n'] for s in by_series.values())} occurrences, "
          f"{len(by_series)} series):\n")
    kill, shorten, dedensity, asyncs = [], [], [], []
    for (uid, name), s in sorted(by_series.items(), key=lambda kv: -kv[1]["min"]):
        density = s["n"] / a.weeks
        avg_min = s["min"] / max(1, s["n"])
        lname = name.lower()
        if any(k in lname for k in ("status", "sync-up", "standup for", "check-in", "touchpoint")):
            asyncs.append((name, s, "status-shaped name — replace with written update"))
        elif avg_min >= 55:
            shorten.append((name, s, f"{avg_min:.0f}→45min — default to shorter"))
        elif density >= 0.9 and avg_min >= 30:
            dedensity.append((name, s, "weekly→biweekly candidate if decisions rare"))
    for label, group in (("KILL/ASYNC", asyncs), ("SHORTEN", shorten), ("DE-DENSITY", dedensity)):
        for name, s, why in group:
            print(f"{label:<11} {name[:44]:<46} {why}")
    # batching advice from focus analysis
    rows = focus_blocks(occs, a, a.person)
    if rows:
        worst = max(rows, key=lambda r: r["fragmented_min"])
        print(f"\nBATCH       scatter on {worst['date'].strftime('%a')} — "
              f"cluster to free a ≥{a.block_min}min block")


def cmd_simulate(a):
    occs, wstart, wend, _ = load_occurrences(a.ics, a.weeks, a)
    base_h = sum(o["minutes"] for o in occs) / a.weeks / 60
    all_dates = sorted({o["start"].date() for o in occs if o["start"].weekday() < 5})
    base_rows = focus_blocks(occs, a, a.person, dates=all_dates)
    base_blocks = sum(r["blocks"] for r in base_rows) / a.weeks
    # focus time = working minutes - fragmented minutes, summed per day
    base_focus_min = sum((a.day_end - a.day_start) * 60 - r["fragmented_min"]
                         for r in base_rows)
    # simulation: drop status-shaped series, shorten 60s to 45
    _, _, by_series = meeting_minutes(occs, a, a.person)
    drop_uids = set()
    saved_min = 0.0
    for (uid, name), s in by_series.items():
        lname = name.lower()
        avg_min = s["min"] / max(1, s["n"])
        if any(k in lname for k in ("status", "sync-up", "check-in", "touchpoint")):
            drop_uids.add(uid)
            saved_min += s["min"]
        elif avg_min >= 55:
            saved_min += s["n"] * (avg_min - 45)
    kept = [o for o in occs if o["uid"] not in drop_uids]
    new_rows = focus_blocks(kept, a, a.person, dates=all_dates)
    new_blocks = sum(r["blocks"] for r in new_rows) / a.weeks
    new_focus_min = sum((a.day_end - a.day_start) * 60 - r["fragmented_min"]
                        for r in new_rows)
    print("SIMULATION — apply KILL/ASYNC + SHORTEN prescriptions:")
    print(f"  meeting hours:  {base_h:.1f} → "
          f"{sum(o['minutes'] for o in kept)/a.weeks/60:.1f} h/week")
    print(f"  focus blocks:   {base_blocks:.1f} → {new_blocks:.1f} /week "
          f"(≥{a.block_min}-min uninterrupted)")
    print(f"  focus time:     {base_focus_min/a.weeks/60:.1f} → "
          f"{new_focus_min/a.weeks/60:.1f} h/week (meeting-free work hours)")
    print(f"  recovered:      {saved_min/a.weeks/60:.1f} meeting-hrs/week "
          f"+ {(new_focus_min-base_focus_min)/a.weeks/60:.1f} h focus time")
    print("  (numbers to bring to the meeting about meetings — meta, but worth it)")


def cmd_team(a):
    all_people = defaultdict(float)
    for p in a.ics:
        occs, wstart, wend, _ = load_occurrences([p], a.weeks, a)
        for o in occs:
            if o["start"].weekday() < 5:
                for att in (o["attendees"] or ["(owner)"]):
                    all_people[att] += o["minutes"]
    if not all_people:
        print("(no attendees found — single-person exports show as (owner))")
    print(f"Team meeting load ({a.weeks} weeks):")
    for person, mins in sorted(all_people.items(), key=lambda kv: -kv[1]):
        flag = " ⚠ >12h/wk" if mins / a.weeks / 60 > 12 else ""
        print(f"  {mins/a.weeks/60:5.1f} h/week  {person}{flag}")


DEMO_ICS = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//meeting-load-balancer//demo//EN
BEGIN:VEVENT
UID:demo-1@mlb
SUMMARY:Weekly Status Sync
DTSTART:20260831T090000
DTEND:20260831T100000
RRULE:FREQ=WEEKLY;BYDAY=MO
ATTENDEE;CN=Alice:mailto:alice@corp.com
ATTENDEE;CN=Bob:mailto:bob@corp.com
ATTENDEE;CN=Carol:mailto:carol@corp.com
ATTENDEE;CN=Dan:mailto:dan@corp.com
END:VEVENT
BEGIN:VEVENT
UID:demo-2@mlb
SUMMARY:Design Review
DTSTART:20260901T140000
DTEND:20260901T150000
RRULE:FREQ=WEEKLY;BYDAY=TU
ATTENDEE;CN=Alice:mailto:alice@corp.com
ATTENDEE;CN=Bob:mailto:bob@corp.com
END:VEVENT
BEGIN:VEVENT
UID:demo-3@mlb
SUMMARY:1:1 Manager
DTSTART:20260902T110000
DTEND:20260902T113000
RRULE:FREQ=WEEKLY;BYDAY=WE
ATTENDEE;CN=Alice:mailto:alice@corp.com
END:VEVENT
BEGIN:VEVENT
UID:demo-4@mlb
SUMMARY:Incident Readout
DTSTART:20260903T160000
DTEND:20260903T163000
RRULE:FREQ=WEEKLY;BYDAY=TH
ATTENDEE;CN=Alice:mailto:alice@corp.com
ATTENDEE;CN=Bob:mailto:bob@corp.com
ATTENDEE;CN=Carol:mailto:carol@corp.com
END:VEVENT
BEGIN:VEVENT
UID:demo-5@mlb
SUMMARY:sprint planning
DTSTART:20260904T100000
DTEND:20260904T113000
RRULE:FREQ=WEEKLY;BYDAY=FR
ATTENDEE;CN=Alice:mailto:alice@corp.com
ATTENDEE;CN=Bob:mailto:bob@corp.com
ATTENDEE;CN=Carol:mailto:carol@corp.com
ATTENDEE;CN=Dan:mailto:dan@corp.com
END:VEVENT
END:VCALENDAR
"""


def cmd_demo(a):
    import tempfile, os
    fd, path = tempfile.mkstemp(suffix=".ics")
    with os.fdopen(fd, "w") as f:
        f.write(DEMO_ICS)
    a.ics = [path]
    a.advice = True
    cmd_stats(a)
    print()
    cmd_focus(a)
    print()
    cmd_prescribe(a)
    print()
    cmd_simulate(a)
    os.unlink(path)


def cmd_list(a):
    occs, _, _, _ = load_occurrences(a.ics, a.weeks, a)
    for o in sorted(occs, key=lambda x: x["start"])[-a.limit:]:
        print(f"{o['start']:%Y-%m-%d %a %H:%M}–{o['end']:%H:%M} "
              f"{o['minutes']:>4.0f}min  {o['summary'][:40]}  "
              f"({len(o['attendees'])}ppl)")


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ics", action="append", required=False,
                   help="ICS file (repeatable); not needed for demo")
    p.add_argument("--weeks", type=int, default=4)
    p.add_argument("--person", help="filter to one attendee name/email")
    p.add_argument("--day-start", type=int, default=9)
    p.add_argument("--day-end", type=int, default=17)
    p.add_argument("--block-min", type=int, default=90)
    p.add_argument("--include-allday", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name, fn, help_ in (
            ("stats", cmd_stats, "hours/week, weekday split, double-booking"),
            ("focus", cmd_focus, "fragmentation and focus blocks"),
            ("rank", cmd_rank, "series ranked by person-hours"),
            ("prescribe", cmd_prescribe, "kill/shorten/de-density/batch advice"),
            ("simulate", cmd_simulate, "effect of applying prescriptions"),
            ("team", cmd_team, "per-person load across multiple exports"),
            ("list", cmd_list, "raw occurrence list")):
        sp = sub.add_parser(name, help=help_)
        sp.set_defaults(func=fn)
        if name == "focus":
            sp.add_argument("--advice", action="store_true")
        if name == "list":
            sp.add_argument("--limit", type=int, default=20)

    sp = sub.add_parser("demo", help="worked example with synthetic calendar")
    sp.set_defaults(func=cmd_demo)

    a = p.parse_args()
    if a.cmd != "demo" and not a.ics:
        p.error("--ics required (or use the demo command)")
    a.func(a)


if __name__ == "__main__":
    main()
