---
name: home-care-calendar
description: "Use when you own a home (or apartment) and things keep breaking because nobody remembered the last service date — builds a whole-home maintenance registry from a guided 10-minute inventory (roof, HVAC, water heater, gutters, detectors, filters, seals, drains), generates a personalized seasonal task calendar with intervals from real maintenance science (filters 1-3 months, HVAC service yearly, water-heater flush yearly, detector batteries yearly, chimney every 2 years...), schedules via ICS export, tracks completion, and estimates the deferred-maintenance debt you're accumulating in dollars — because a $12 filter neglected for a year becomes a $1500 compressor."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [home-maintenance, homeowners, calendar, hvac, prevention, household]
---

# Home Care Calendar

## Overview

Homes decay on schedules nobody memorizes. The HVAC filter chokes silently for 18 months until the compressor dies. Gutters fill until the fascia rots. The water heater sediment layer grows until efficiency tanks. Smoke detector batteries die at 2 AM. Every one of these is a $12–$50 task whose neglect becomes a $500–$15,000 repair.

The problem isn't knowledge — maintenance intervals are well established — it's **remembering**. Paper checklists get lost, and generic online calendars don't know what equipment you actually have.

This skill builds a **personal home-care system** in three steps:

1. **Guided inventory** (10 min, one time) — record your home's maintainable systems: type, install year, notes. The CLI walks you through the standard checklist room by room.
2. **Auto-generated calendar** — every item maps to interval tasks (from maintenance science: filter changes, flushes, inspections, tests). You get this month's list, the next-90-days view, and a full seasonal calendar.
3. **Completion tracking + ICS export** — mark tasks done; intervals reset from completion, not from schedule (real life slips). Export an .ics for any calendar app; tasks appear as all-day events with instructions.

Plus **deferred-maintenance debt**: each overdue task carries an estimated neglect cost (e.g., "filter overdue 4 months → compressor strain risk ~$180 of expected lifespan"), summed into a single number you can watch go down.

## When to Use

- **New homeowners** — the first-year maintenance schedule nobody hands you at closing.
- **"When did we last service the furnace?"** — the registry answers instantly.
- **Seasonal transitions** — spring/fall task lists (gutters, AC coils, winterization, detector batteries at DST changes).
- **After any repair** — log the new equipment; the calendar absorbs it.
- **Renters too** — smaller scope: filters, detectors, drains, caulk; plus documentation for deposit disputes.
- **Landlords** — per-property registries; proof of diligence.
- Don't use for: emergency repairs (call a pro now), HOA-managed systems (their schedule wins), or structural issues — those need an inspector, not a calendar.

## How It Works

1. **Inventory** — `add` each system: `--kind furnace --installed 2019 --note "Carrier, basement"`. Kind library has ~30 types with default intervals and instructions.
2. **Calendar** — `calendar` renders this month / next 90 days / full year grouped by season. Each task: what, why, how long, DIY vs pro.
3. **Complete** — `done <task-id>` resets the interval clock and records history.
4. **ICS export** — `ics home-care.ics` writes all-day events for every scheduled occurrence over the next 12 months, with instructions in the description.
5. **Debt report** — `debt` lists overdue tasks with neglect-cost estimates and a total.

## Commands

```bash
# Guided inventory: walks through the standard home systems
python3 scripts/home_care.py inventory

# Add items directly
python3 scripts/home_care.py add --kind furnace --installed 2019 --note "Carrier 59SC5, basement"
python3 scripts/home_care.py add --kind hvac-filter --note "16x25x1, hallway"
python3 scripts/home_care.py add --kind smoke-detector --note "3 units: hallway, 2 bedrooms"

# What's due now / soon
python3 scripts/home_care.py calendar           # this month
python3 scripts/home_care.py calendar --days 90 # next 90 days
python3 scripts/home_care.py calendar --year    # full seasonal view

# Mark done (interval restarts from today)
python3 scripts/home_care.py done hvac-filter:1

# Export to calendar app
python3 scripts/home_care.py ics home-care.ics

# Deferred-maintenance debt in dollars
python3 scripts/home_care.py debt

# Everything as JSON
python3 scripts/home_care.py calendar --json
```

## Example Session

```
$ python3 scripts/home_care.py calendar

HOME CARE — SEPTEMBER 2026 (3 tasks due, 1 overdue)

OVERDUE:
  ⚠ WATER HEATER FLUSH — 3 months overdue
    Why: sediment layer kills efficiency and tank life.
    How: drain 5-10L from the drain valve until water runs clear. 30 min, DIY.
    Neglect cost: ~$85 so far (efficiency loss + tank life)

DUE THIS MONTH:
  • HVAC FILTER CHANGE — every 2 months (last done 2026-07-20)
    16x25x1. 5 min, DIY. $8-15.
  • RANGE HOOD FILTER DEGREASE — every 6 months
    Soak in degreaser 20 min. 25 min, DIY.

NEXT 90 DAYS (preview):
  Oct: gutter clean before leaf fall (last: never logged)
  Oct: smoke detector batteries at DST end (test monthly anyway)
  Nov: furnace professional service before heating season
  Nov: reverse ceiling fans, check weatherstripping
```

## Task Library (abridged)

| System | Task | Interval | DIY? | Neglect cost |
|---|---|---|---|---|
| HVAC filter | replace | 1–3 mo (per type) | DIY | compressor strain, energy +15% |
| Furnace/heat pump | pro service | 12 mo | PRO | efficiency loss, winter failure |
| AC condenser | coil clean + service | 12 mo | PRO/DIY | capacity loss, compressor death |
| Water heater | sediment flush | 12 mo | DIY | tank life −years, efficiency |
| Gutters | clean | 6 mo (spring/fall) | DIY | fascia rot, foundation, ice dams |
| Smoke detector | battery + test | 12 mo | DIY | lives |
| CO detector | battery + expiry check | 12 mo | DIY | lives |
| Dryer vent | lint deep-clean | 12 mo | DIY | fire risk |
| Refrigerator | coil vacuum | 6 mo | DIY | energy, compressor |
| Dishwasher | filter clean + citric run | 3 mo | DIY | pump death, smells |
| Faucet aerators | descale | 12 mo | DIY | flow, fixture scale |
| Caulk/grout | inspect + patch | 6 mo | DIY | hidden water damage |
| Sump pump | bucket test | 3 mo | DIY | flood |
| Chimney | pro inspection | 24 mo | PRO | creosote fire |
| Roof | visual inspection | 12 mo | DIY (from ground) | leaks found late |
| Trees | prune near house | 24 mo | PRO | storm damage |
| Water shutoffs | exercise valves | 12 mo | DIY | seized when needed most |

Full library in `references/task-library.md` (~30 systems).

## Workflow for an Agent

1. First run: walk the user through `inventory` — the standard system list is the checklist; skip what they don't have.
2. Generate `calendar --year` and show the seasonal rhythm; export `ics` right away (adoption = the tasks reaching a calendar they already use).
3. Monthly: `calendar` → present due tasks; after the user does them, `done`.
4. Quarterly: `debt` — present the total and the top 3 contributors.
5. After any repair/replacement: `add` the new equipment with its install date.
6. Recommend the two DST weekends as anchor dates for detector batteries — habit stacking on existing clock-change memory.

## Common Pitfalls

1. **Scheduling from install date forever.** Intervals reset on `done`; if the user never marks completion, everything drifts into "overdue" noise. Mark done as you go.
2. **One filter interval for all filters.** 1-inch fiberglass = 1–2 mo; pleated = 2–3 mo; HEPA/4-5 inch = 6–12 mo. The `add` prompt asks for type.
3. **Ignoring PRO tasks because they're pricier.** Pro HVAC service is the difference between a $150 tune-up and a $5,000 off-season replacement. DIY list ≠ complete list.
4. **Gutter timing by calendar, not trees.`` Add a month of leaf-drop delay for oak-heavy yards; clean AFTER leaf fall, not on equinox.
5. **Detector expiry, not just batteries.** Smoke detector UNITS expire (10 yr, date on back); CO units 5–10 yr. The annual task includes the expiry check.
6. **Treating neglect-cost estimates as invoices.** They're expected-value rough figures for prioritization, not quotes.

## Verification Checklist

- [ ] Inventory covers the standard systems (or explicit skips recorded)
- [ ] Filter types recorded with correct intervals
- [ ] ICS exported and imported into the user's real calendar
- [ ] Overdue tasks surfaced with neglect costs, not hidden
- [ ] `done` used after each completion (keeps intervals honest)
- [ ] Seasonal anchors (DST detector batteries, pre-heating-season furnace) placed
