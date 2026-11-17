# Humidity & Window Fog Doctor

**Every cold morning: windows weeping on the inside, puddles on the sills,
black speckles on the frame corners.** "The windows are bad" and "the house
is too humid" are both half right — condensation is a computable dew-point
collision: warm moist air against glass chilled below that air's dew point.
Change either side of the collision and it stops. Which side is cheaper to
change is arithmetic, and this tool does it.

```
python3 scripts/windowfog.py --tin 21 --rh 50 --tout -10 --glazing single
# Inner pane surface: -0.8°C   threshold RH: 23%
# VERDICT: CONDENSATION
# Fix: GLASS-SIDE FIX required — target RH 18% is below the comfort floor

python3 scripts/windowfog.py --tin 21 --rh 55 --tout -8 --glazing double --curtains
# Tonight's culprit may be the curtains: pane is 5.5°C colder with them closed.
```

## The real-world problem
- Condensation is the #1 winter indoor-air complaint in temperate climates,
  and the standard responses fail: wiping (water returns nightly), closing
  curtains "to keep the glass warm" (actually chills the pane further),
  humidifiers chasing "healthy 50%" folklore (single glazing at −15 °C
  can't carry it).
- Persistent frame wetting becomes **mold in 24–48 h** on organic
  substrates — a health issue, not cosmetics.
- The correct target RH depends on your *coldest* glazing class and tonight's
  outdoor temperature — a number nobody knows without this physics. Single
  pane at −10 °C tops out at 23%; triple at 80%.
- Renters and landlords argue about fault; this separates "house carries
  X% RH fine, your drying rack adds 2 kg/day" from "glazing genuinely can't
  hold healthy humidity."

## What it does
- Inner-pane surface temperature from U-value + film resistances, incl. the
  closed-curtain cavity effect (5–6 °C colder pane)
- Condensation verdict + threshold-RH table across 0…−20 °C for your glazing
- Target RH with safety margin; if the target drops below the ~35% comfort
  floor, it prescribes glass-side fixes instead of "dry out more"
- Moisture-source audit (laundry 2 kg/day, unflued gas 1.6 kg/kg-fuel,
  sleepers, showers) and the ventilation pump math
- Fix ladder ordered by cost: behavior → air washing → storm film/panel →
  low-e glazing / HRV

## What's inside
- `SKILL.md` — triggers, steps, pitfalls (curtains!, wiping-vs-ventilating,
  humidifier folklore), checklist
- `references/condensation-physics.md` — resistance chain, threshold table,
  moisture handbook, ventilation math, mold timing, fix ladder
- `scripts/windowfog.py` — pure stdlib; Magnus dew point, `--curtains`,
  `--json`; verified on single/double/low-e/triple + curtain cases

MIT © Denis Voronin
