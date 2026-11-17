---
name: heating-setback-optimizer
description: "Use when designing or questioning a thermostat schedule: computes real fuel savings from night/away temperature setbacks (degree-hour physics with thermal-mass and heat-loss-recovery effects), compares constant vs setback strategies, finds optimal setback depth, and warns when setback BACKFIRES (heat pumps with strips, radiant floors, short setbacks)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [thermostat, setback, heating, energy-saving, degree-hours, heat-pump, hvac, utility-bills]
---

# Heating Setback Optimizer

## Overview
"Turn the heat down at night" is folk wisdom with failure modes. The savings
exist — a heated house loses energy at a rate proportional to
(inside − outside), so every degree-hour you don't maintain is fuel not
burned — but the *size* of the saving depends on your building, your
climate, and critically **your heating system**. A deep setback on a heat
pump that triggers resistive backup strips on recovery can cost MORE than it
saves. This skill computes, for your house:

- **Degree-hour savings** of a candidate setback schedule vs constant
  holding, using your balance point and thermal mass
- **Recovery penalty**: the extra burner/strip capacity needed to climb back
  (and the comfort lag in the morning)
- **System-specific verdicts**: furnace/boiler (setback wins), heat pump
  with strips (setback depth capped, or use smart recovery), radiant slab
  (setbacks must be shallow and slow — slab time constants are 6–12 h)
- **Optimal depth search**: scans 0–6 °C setback × schedule shapes and
  ranks by net saving; flags comfort tradeoff (morning warm-up time)
- **Dollars**: converts saved energy to fuel cost for gas/oil/ electric-
  resistance/heat-pump COP

## When to Use
- "Is it worth setting back at night, or is that a myth?" (answer: measured,
  not folklore)
- Designing a weekly program: workday away 9–17, night 22–7, weekend shape
- Heat-pump owners told to "never touch the thermostat" — get the real cap
- Comparing smart-thermostat claims (Nest-style "10–12% savings") for YOUR
  house and climate
- **Don't use for:** cooling setbacks (different physics: latent load —
  humidity), multi-zone commercial, or exact billing prediction (model
  accuracy is ±20%, good for decisions, not invoices).

## Steps
1. Estimate your house: heat-loss coefficient (or last winter's fuel use —
   script converts), indoor setpoint, outdoor design/average temps, system
   type and efficiency/COP, thermal mass class (light = timber frame + air,
   medium = drywall+contents, heavy = slab/stone).
   ```bash
   python3 scripts/setback.py --k 220 --tin 21 --tout-avg -3 --hours-night 8 \
       --system furnace --fuel gas --price 1.30
   python3 scripts/setback.py --scan   # optimal depth search with defaults
   ```
2. Read the comparison table: constant vs your setback schedule, % and
   $ saved, recovery ramp minutes, morning comfort temp at wake time.
3. Check the verdict block for your system: allowed depth, cycle-length
   floor (setbacks shorter than ~3 h rarely pay), smart-recovery advice.
4. Iterate: try deeper/shallower, weekend shapes, away-day — pick the
   schedule on the ranked list.

## The Model (summary — full in references/setback-physics.md)
- Steady loss: `Q_loss = K·(T_in − T_out)` W; setback saves
  `K·ΔT·t_setback` minus recovery overrun.
- Recovery needs the system's excess capacity: ramp time ≈
  `C·ΔT / (Q_max − K·(T_in − T_out))` with mass C (light≈3, medium≈6,
  heavy≈12 kWh/K effective).
- Heat pump with auxiliary strips: if recovery load > compressor capacity,
  strips (COP≈1) burn the savings; effective cap ≈ 1.5–2 °C unless the
  thermostat does staged/smart recovery at compressor-only speed.
- Furnace/boiler: recovery is cheap (oversized burners); savings ≈
  0.8–1.2% per °C-setback per 8 h — the classic field-study band.

## Output
Savings table (energy, %, $ per heating season), recovery ramps, ranked
schedule candidates from the scan, system verdict. `--json` for machine use.

## Common Pitfalls
1. **Deep setback on a strip-equipped heat pump.** The morning recovery
   calls strips (resistance, COP 1) and erases the night's savings. Cap at
   1.5–2 °C or use gradual/smart recovery; the script prices this in.
2. **Setback shorter than the house's time constant.** A 1 h dip in a heavy
   slab house barely moves the temperature; savings ≈ 0, cycling wear ≈ up.
   Keep setback windows ≥3 h (light) / ≥6 h (heavy).
3. **Counting recovery as free.** Raising 3 °C costs an overshoot of mass
   heating; the model subtracts it — folk math usually doesn't.
4. **Ignoring outdoor-reset/radiant systems.** Radiant slab with outdoor
   reset: use 1 °C max setback or none; ask the model (system=radiant).
5. **Vented/uninsulated setback arithmetic** on old houses overestimates
   savings if K is taken from design-day instead of seasonal average —
   use fuel-bill-derived K when possible.
6. **Humidity swing**: deep setbacks in tight winter houses raise morning RH
   at windows → condensation; check glazing class if you see frosting.

## Verification Checklist
- [ ] System type honored: heat-pump caps / radiant floors / furnace freedom
- [ ] Recovery energy subtracted, not ignored
- [ ] Setback window ≥ system-appropriate minimum flagged if violated
- [ ] Savings quoted as % of *heating* energy, not total bill
- [ ] Scan ranked list shows the depth curve, including where it flattens
