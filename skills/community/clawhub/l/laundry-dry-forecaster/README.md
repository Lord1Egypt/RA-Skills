# Laundry Dry Forecaster

**You hang a load at 22:00 and need it dry by 07:00. Will it be? And how
much of that load is about to become condensation on your windows?**
A spun laundry load holds 1.5–3 kg of water — indoor rack drying is a
zero-sum transfer of that water into your room air, at a rate set by
vapor-pressure-deficit physics (temperature, RH, airflow). Both the
hours-to-dry and the humidity hit are computable. This tool computes them.

```
python3 scripts/laundrydry.py --kg 4 --spin 1400 --tin 20 --rh 55 \
    --airflow fan --room-m3 40 --vent-ach 1.0 --hang-hour 22 --deadline 7
# DRY in ~7 h   -> hour 05:00  -> MEETS deadline
# Peak room RH during drying: 55%   WARNING: expect window fogging

python3 scripts/laundrydry.py --kg 4 --spin 800 ...   # -> 10 h (spin lever!)
python3 scripts/laundrydry.py --airflow dehumidifier --room-m3 15 --vent-ach 0.3
# DRY in ~4 h, peak RH 58% — water goes to the tank, not the glass
```

## The real-world problem
- Drying laundry indoors is near-universal in apartments and winter — and
  it's a top-3 indoor moisture source (one load ≈ 2 kg water; a drying rack
  indoors is comparable to showering 10× daily). The consequences — window
  fog, frame mold, musty loads — are treated as mysteries when they're
  arithmetic.
- The musty-load failure: "dry to the touch" isn't dry; the falling-rate
  tail holds 10–15% water in seams for hours, and a slow load sitting damp
  grows microbes. Knowing the *total*-dry time (two-phase model) prevents it.
- Money: spin 800→1400 rpm removes ~0.8 kg water for ~30 Wh — the cheapest
  drying acceleration that exists. `--compare` prices rack vs dehumidifier
  vs heated airer vs condenser vs heat-pump dryer at YOUR tariff
  (rack+dehumidifier ≈ $0.14/load and fixes the humidity; condenser dryer
  ≈ $0.55 and worsens it).

## What it does
- Residual water from spin rpm (800→1600 interpolation)
- VPD evaporation engine with airflow classes (still/fan/heated airer/
  dehumidifier/outdoor) and two-phase drying (constant-rate + 0.4× tail)
- Coupled room-RM simulation: kg water dumped, peak room RH, condensation
  warning against your glazing threshold (pair with
  humidity-window-fog-doctor)
- Dry-by deadline verdict; method cost table at your electricity price

## What's inside
- `SKILL.md` — triggers, steps, pitfalls (radiator-drape trap, cramming the
  rack, spin myths, winter outdoor fatalism), checklist
- `references/drying-physics.md` — VPD engine, calibration anchors, room
  moisture math, cost derivations, freeze-drying, musty rescue
- `scripts/laundrydry.py` — pure stdlib, `--json`; verified: still 14 h /
  fan 7 h / dehumidifier 4 h / closed-bathroom saturation 40 h / outdoor
  breezy 19 h — all matching field behavior

MIT © Denis Voronin
