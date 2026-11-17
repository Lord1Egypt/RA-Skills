---
name: laundry-dry-forecaster
description: "Use when drying laundry on a rack indoors (or outdoors): computes hours-to-dry from vapor-pressure-deficit evaporation physics and spin-speed residual moisture, the kg of water the load dumps into your air, the room RH rise (condensation risk), and the cheapest drying method comparison (rack vs dehumidifier vs heated airer vs tumble dryer kWh)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [laundry, drying, evaporation, humidity, indoor-air, energy-cost, vpd, clothesline]
---

# Laundry Dry Forecaster

## Overview
A wet laundry load is 1.5–3 kg of water waiting to become your indoor air's
humidity. Whether the load dries in 4 hours or 18 — and whether your windows
start weeping because of it — is computable evaporation physics: the drying
rate is driven by **vapor pressure deficit** (how much more moisture the air
can still hold at its temperature), air movement, and the load's residual
water after spinning.

This skill computes:

- **Residual water** in the load from wash weight and spin speed
  (1400 rpm ≈ 50% of dry weight; 800 rpm ≈ 70%)
- **Drying time** from VPD-based evaporation rate (temp, RH, airflow class),
  with the two-phase reality (constant-rate wet phase ≈ 70% of water, then
  the slow falling-rate phase for seams/pockets)
- **Moisture dumped into the room**: total kg water, room RH rise with your
  room volume and air-change rate, and the condensation warning when it
  pushes past your glazing's threshold
- **Drying-finish verdict**: "dry by 07:00 if hung at 22:00?" — direct answer
- **Method cost comparison**: rack (free but +humidity), dehumidifier
  (~0.3 kWh/kg water, heats room), heated airer, condenser vs heat-pump
  tumble dryer — kWh and $ per load for your tariffs

## When to Use
- "If I hang this load at 22:00, will it be dry by morning?"
- Winter indoor drying: how much humidity is this adding to my flat?
  (Condensation chain: see humidity-window-fog-doctor skill)
- Choosing a drying method on cost: rack+dehumidifier often beats a
  condenser dryer AND fixes the humidity problem
- Outdoor line: temperature, RH, wind and freeze-drying verdicts
- **Don't use for:** delicate-fabric care rules (labels win), commercial
  laundry sizing, or tumble dryer sensor troubleshooting.

## Steps
1. Know: dry weight of load (typical: 3–4 kg), spin rpm used, indoor temp
   and RH, airflow (still room / fan on / heated airer / dehumidifier),
   room volume and rough air changes (closed bathroom ≈ 0.5 ACH, living
   room with door open ≈ 1–2).
   ```bash
   python3 scripts/laundrydry.py --kg 4 --spin 1400 --tin 20 --rh 60 --airflow still \
       --room-m3 40 --vent-ach 1.0 --hang-hour 22 --deadline 7
   python3 scripts/laundrydry.py --kg 4 --spin 1400 --tin 20 --rh 45 --airflow dehumidifier
   ```
2. Read: hours to dry, dry-by verdict, kg water into the air, peak RH rise.
3. If RH rise pushes the room past your window threshold (rule of thumb:
   +8–15 RH points from one load in a small flat), apply the fix: dehumidifier
   mode (drying AND draining) or ventilate in bursts.
4. Compare `--compare` costs per load for your tariff.

## The Model (summary — full in references/drying-physics.md)
- Residual moisture: `m_water = m_dry × RM(spin)`, RM: 800→0.70, 1000→0.62,
  1200→0.55, 1400→0.50, 1600→0.45 (interpolated).
- Evaporation: `E = k_airflow × VPD(T,RH)`; VPD from saturation vapor
  pressure (Magnus/Tetens) minus actual; k: still 0.018, fan 0.035,
  heated airer 0.06, dehumidifier 0.09 kg/h per kPa deficit (per ~4 kg load,
  spread on a rack).
- Two phases: constant-rate until ~30% of water remains, then rate ×0.4
  (falling-rate period — the socks-seam tail).
- Room RH rise: added water minus ventilation removal
  (ACH × volume × moisture capacity difference), integrated over the drying.
- Outdoor: same VPD engine with wind classes; below 0 °C the freeze-dry
  path (ice sublimation) is slow but real; rain/dew re-wetting resets.

## Output
Verdict block (hours, dry-by time), water budget, RH trajectory warning,
method comparison table. `--json` for machine use.

## Common Pitfalls
1. **Drying on the radiator next to a closed window**: fastest local
   evaporation but 100% of the water goes into the room, then onto the
   coldest glass. The RH-rise number tells you if that's this load's fate.
2. **Assuming "dry to the touch" = dry**: the falling-rate tail holds
   10–15% water in seams/elastics for hours more — musty smell is microbial
   growth on that residual in slow loads; the verdict uses total-dry time.
3. **Cramming the rack**: overlapping items halve the effective area; the
   airflow classes assume a spread load — hang a 6 kg load like a 6 kg load
   (two racks or re-hang), not like a 10 kg pile.
4. **Dehumidifier in the same room with door open**: it dries the whole
   flat, not just the laundry — fine, but drying time lengthens toward the
   house-volume number; close the room for the fast version.
5. **Spin-speed myth**: "high spin damages clothes" is mostly false for
   cottons; going 800→1400 rpm removes ~0.6 kg water per 4 kg load — often
   the single cheapest drying acceleration available (free, done by the
   machine you already own).
6. **Outdoor winter "won't dry" fatalism**: at −5 °C and 70% RH, freeze-
  drying still completes in a day of sun/wind — check the verdict before
  defaulting to the indoor rack + humidity penalty.

## Verification Checklist
- [ ] Residual water computed from actual spin rpm, not "wet = heavy"
- [ ] Two-phase drying modeled (the tail dominates the finish time)
- [ ] RH rise checked against a stated condensation threshold, not vague "humidity"
- [ ] Cost comparison uses the user's tariff, not generic kWh prices
- [ ] Dry-by verdict answers the actual hang-time question asked
