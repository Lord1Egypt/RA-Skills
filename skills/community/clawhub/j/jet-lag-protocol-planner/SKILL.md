---
name: jet-lag-protocol-planner
description: "Use when crossing 2+ time zones: computes your day-by-day circadian shift protocol — pre-trip sleep shifting, light SEEK/AVOID windows timed to your core-body-temperature minimum, low-dose melatonin timing, caffeine cutoffs, and in-flight/first-days rules for east and west travel."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [jet-lag, circadian, travel, melatonin, light-therapy, sleep, time-zones]
---

# Jet Lag Protocol Planner

## Overview
Jet lag is not "being tired" — it is your circadian clock being out of phase
with local time. The clock shifts about **1 h/day eastward** and **1.5 h/day
westward** on its own; light and melatonin, correctly timed, do the steering.
Incorrectly timed they make it *worse*: bright light in the wrong window pushes
your phase the wrong direction. This skill turns a trip into a dated protocol:

- Finds your **CBTmin** (core body temperature minimum, ≈2 h before habitual
  wake) — the anchor for every timing decision
- Computes required phase shift and direction (handling the >12 h wrap case)
- Generates a **day-by-day table**: Day −3 … landing … aligned, with wake
  target, **SEEK-light window**, **AVOID-light window**, melatonin time,
  caffeine cutoff — all in the clock you are actually living on that day
- In-flight rules (sleep window on plane, alcohol/hydration) and the
  critical first-48-hours light discipline at destination

## When to Use
- Any trip crossing ≥2 time zones (shorter: arrive-mode advice only)
- "Which side of the plane / when do I get sunlight in Tokyo?"
- Pre-trip: "should I start shifting my sleep before I fly, and how?"
- Athletes/execs who must perform on landing day
- **Don't use for:** shift work (different skill: sleep-shift-survivor),
  melatonin dosing for children (ask a pediatrician), or as medical advice —
  this is timing arithmetic on well-established circadian science.

## Steps
1. Collect: home timezone offset, destination offset, habitual home wake time
   (e.g., 07:00), desired wake at destination, days available before flight
   (0–3).
   ```bash
   python3 scripts/jetlag.py --home-tz 3 --dest-tz -5 --wake-home 07:00 \
       --wake-dest 07:00 --pre-days 3
   ```
2. Read the day table. Note the direction (ADVANCE east / DELAY west), the
   daily shift rate, and which clock each day's times are in.
3. Follow the AVOID windows as strictly as the SEEK windows — sunglasses,
   dim indoor light, eye mask. Morning light before your shifted CBTmin on an
   eastward trip is the classic self-inflicted setback.
4. Long-hauls (>8 h shift): accept you will not fully align in a typical
  trip; the planner marks the realistic partial target and prioritizes
  first-3-days performance.

## The Model (summary — full detail in references/circadian-science.md)
- CBTmin ≈ habitual wake − 2 h. Phase marker for everything.
- Light PRC: light in the ~4 h **before** CBTmin → phase **delay** (west);
  in the ~4 h **after** → phase **advance** (east). Magnitude grows with
  brightness and proximity to CBTmin.
- Melatonin PRC is roughly the light curve inverted: low dose (0.3–1 mg)
  ~5 h before CBTmin → advance; after CBTmin → delay (avoid daytime dosing).
- Alignment speed: east ≈ 1.0 h/day, west ≈ 1.5 h/day; pre-trip shifting can
  pre-pay up to ~2–3 h east / ~2 h west.
- Direction picks the short way around: a +14 h east difference is treated as
  10 h west (delay) because that is what your clock will actually do.

## Output
Per-day protocol table (date-less: Day −N relative to flight), then
flight-day rules, then destination first-days discipline, then the
principles recap and safety notes. `--json` for machine use.

## Common Pitfalls
1. **Seeking light on landing morning after an eastward flight** — before
   your CBTmin has shifted, that light delays you further. Check the table.
2. **Melatonin as a sleeping pill at midnight local** — if it lands after
   CBTmin it delays you (wrong direction eastward) and grogginess results.
   The planner gives the clock time; take it then, keep dose low.
3. **Napping into the local afternoon** — caps at 25–30 min before ~15:00;
   a 3 h crash at 16:00 local locks the old phase in.
4. **Ignoring the wrap**: LA→Tokyo is +17 h on paper = **−7 h (delay)** for
   your clock. The planner picks delay automatically; don't override east.
5. **Caffeine after the cutoff** — half-life ~5–6 h pushes sleep onset later
   exactly when you need it earlier.

## Verification Checklist
- [ ] Direction (advance/delay) matches the shorter arc, not the sign of raw offset difference
- [ ] Every day's times labeled with which clock they are in (home vs destination)
- [ ] SEEK and AVOID windows move with the shifted CBTmin, not fixed clock times
- [ ] Melatonin time sits 4–6 h before that day's CBTmin (eastward) — verify in output
- [ ] Caffeine cutoff printed for flight day and each destination day
