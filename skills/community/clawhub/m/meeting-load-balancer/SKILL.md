---
name: meeting-load-balancer
description: "Use when your calendar is eating your week and you want to know exactly where the time goes, when planning recurring meetings for a team, before proposing a new recurring meeting, when someone says 'we should sync weekly' and you want data, or when auditing which meetings to kill — imports ICS calendar files, measures meeting hours per week/person/meeting-series (including double-bookings and fragmentation), computes focus-time destruction from meeting placement, scores the true cost of each series (hours × attendees × frequency), flags specific meetings to kill/shorten/make-async using explicit rules, and simulates the recovered hours before anyone has to argue about it."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [meetings, calendar, time-management, productivity, team-analytics, ics]
---

# Meeting Load Balancer

## Overview

Knowledge workers lose 10–20+ hours a week to meetings, and almost nobody measures it.
Calendars fill by accretion: each recurring meeting was individually justifiable in
isolation and collectively catastrophic. The damage isn't only the summed hours — it's
*fragmentation*: a day with 4 hours of meetings scattered into 45-minute gaps has zero
deep-work blocks left, and a team's most expensive people are often its most
double-booked.

This skill turns an exported calendar (`.ics`) into an evidence-based meeting audit:

1. **Import** — parses standard ICS files (Google/Outlook/Apple all export it), expands
   recurring events over a date window, dedupes cancelled occurrences.
2. **Measure** — hours/week total, per weekday, per meeting series, per attendee;
   double-booked overlaps; meeting-free gaps and the longest focus block per day.
3. **Fragmentation score** — counts usable focus blocks (≥90 uninterrupted minutes)
    destroyed by meeting placement, per day and per week. 4 hours of meetings can cost
   8 hours of focus depending on placement.
4. **True-cost ranking** — each series scored by `hours × attendees × frequency` with
   placement damage, producing the "this standing meeting costs the team a
   work-week per month" list.
5. **Prescriptions** — explicit rules flag meetings to KILL (low attendance, no
   decision record), SHORTEN (25/50-min default), DE-DENSITY (weekly→biweekly),
   BATCH (scattered→clustered), or MAKE-ASYNC (status-shaped), plus a **simulate**
   mode that shows hours and focus blocks recovered if you applied the changes.

Everything runs offline on calendar files you control; nothing is uploaded.

## When to Use

- **Personal calendar audit** — "where did my week go?" → `stats`, `focus`
- **Before proposing a new recurring meeting** — check the team's existing load first
- **Team retro / effectiveness review** — aggregate several people's exports → `team`
- **Defending focus time** — find the batchable/blocked windows → `focus --advice`
- **Killing a standing meeting with evidence** — `rank` then `simulate` the removal
- Don't use for: room/equipment scheduling (different problem), or individual-event
  time zone archaeology (the parser handles standard ICS but exotic recurrence rules
  may be simplified — always sanity-check counts against your calendar app).

## Commands

```bash
# Export your calendar first (see references/ics-export.md), then:
python3 scripts/meeting_load.py stats --ics calendar.ics --weeks 4
python3 scripts/meeting_load.py stats --ics calendar.ics --weeks 4 --person "you@corp.com"

# Focus-time analysis (fragmentation, longest blocks, batchable windows)
python3 scripts/meeting_load.py focus --ics calendar.ics --weeks 4

# Rank every recurring series by true cost
python3 scripts/meeting_load.py rank --ics calendar.ics --weeks 4

# Rule-based prescriptions: kill / shorten / de-density / batch / async
python3 scripts/meeting_load.py prescribe --ics calendar.ics --weeks 4

# Simulate applying the prescriptions (before arguing about it)
python3 scripts/meeting_load.py simulate --ics calendar.ics --weeks 4

# Multi-person: combine exports (cat them or pass --ics twice)
python3 scripts/meeting_load.py team --ics alice.ics --ics bob.ics --weeks 4

# Worked example without any calendar
python3 scripts/meeting_load.py demo
```

## Metrics Definitions

| Metric | Definition |
|---|---|
| meeting hours/week | summed event durations ÷ weeks in window |
| double-booked hrs | time in 2+ overlapping events (counted once per extra event) |
| focus block | ≥ 90 contiguous meeting-free minutes inside working hours |
| fragmentation | working hours minus longest focus block, on days with any meeting |
| series cost | avg hours × attendee count × occurrences in window |
| density | recurring-series occurrences per week (1.0 = weekly) |

Working hours default 09:00–17:00 local, Mon–Fri (`--day-start 9 --day-end 17` to
change). Multi-day and all-day events are excluded from meeting metrics by default.

## What Prescriptions Look Like

```
PRESCRIPTIONS (12 meetings analyzed, 4 series):

KILL      'Weekly Status Sync'        60min × 8 ppl × 1.0/wk — status-shaped,
          avg 53% accepted, no decisions logged → replace with written update
SHORTEN   'Design Review'             60→45min — 62% of occurrences end early
          (median actual use 40min)
DE-DENSITY '1:1 Manager'              weekly→biweekly — 4/4 weeks had
          cancellation/reschedule
BATCH     'sprint-planning' Mon 14:00 + 'retro' Thu 11:00 + 'estimation' Tue 10:00
          → same day cluster frees 2 full days/week of ≥3h blocks
ASYNC     'Incident Readout'          12 occurrences, avg 6 min used of 30,
          1 speaker — record/video instead

simulated effect: −5.6 meeting hrs/week, +2.1 focus blocks/week for the team
```

## Common Pitfalls

1. **Exporting too narrow a window.** Recurring meetings reveal their sins over 4+ weeks
   (cancellations, attendance decay). Use `--weeks 4` minimum; 8 is better.
2. **Counting declined events.** The tool excludes events you declined where the ICS
   records it; re-check surprises with `list --day` before believing a number.
3. **Treating hours as the metric.** Two calendars with identical meeting hours can
   differ 2× in usable focus time. Always read `focus` alongside `stats` — placement,
   not just volume, is the enemy.
4. **Forgetting attendee cost.** A 30-min meeting for 10 people is 5 person-hours; the
   `rank` output exists so the "quick sync" gets priced honestly.
5. **Shortening everything reflexively.** Some 60s earn their hour (decisions with real
   debate). The rules flag *evidence* of waste (early endings, decay, status-shape),
   not length per se.
6. **All-day/multi-day events polluting stats.** They're excluded by default; if your
   org encodes real meetings as all-days (some do), `--include-allday`.

## Verification Checklist

- [ ] ICS export covers ≥4 weeks and includes recurring expansions
- [ ] `stats --person <you>` matches what your calendar app reports for a sample week
- [ ] `focus` reviewed — fragmentation is usually the hidden finding
- [ ] `simulate` run before proposing changes; numbers shown to attendees
- [ ] Changes applied incrementally (kill one, measure again next month)

## One-Shot Recipes

**Personal "where did March go" audit**
```bash
python3 scripts/meeting_load.py stats --ics march.ics --weeks 4
python3 scripts/meeting_load.py focus --ics march.ics --weeks 4
```

**The 'we should add a weekly sync' moment**
```bash
python3 scripts/meeting_load.py team --ics a.ics --ics b.ics --ics c.ics --weeks 4
# if anyone is >12 hrs/wk or <1 focus block/day → propose async instead
```

**Annual meeting purge**
```bash
python3 scripts/meeting_load.py rank --ics q3.ics --weeks 8
python3 scripts/meeting_load.py simulate --ics q3.ics --weeks 8
```
