# Ice Dam Defense

**"I spread salt and nothing happened" — and — "my roof is leaking at the eave."**

Two winter failures homeowners face every year, both fixable with real physics:

1. **De-icing chemistry** — rock salt stops melting at −9 °C pavement temperature (the −21 °C
   on the bag is a lab eutectic). The sidewalk planner tells you which chemical works at your
   actual pavement temp, exactly how many kg for your area, and warns when tonight's refreeze
   will turn your melt into black ice.
2. **Roof ice dams** — warm-attic heat leaks melt roof snow, it refreezes at the cold eave,
   and the backed-up water wicks under shingles into your ceiling. The roof tool scores 10
   dam risk factors (0-100), computes snow load (depth × density → kg vs typical capacity),
   and walks the safe-removal ladder: rake from the ground, never chip, CaCl₂ sock channel,
   spring air-sealing fix list.

## Quick start

```bash
python3 scripts/ice_dam_defense.py sidewalk --area-sqm 60 --temp-c -8 --material rock-salt --refreeze -12
python3 scripts/ice_dam_defense.py roof --depth-cm 45 --roof-sqm 120 --insulation-poor --past-dams
python3 scripts/ice_dam_defense.py demo
```

## What's inside

- 7 de-icers profiled: NaCl, MgCl₂, CaCl₂, blends, potassium acetate, CMA, sand — effective
  floors, rates, corrosion, pet/plant/concrete safety.
- Brine anti-icing guidance (⅓ the salt, applied the evening before).
- Ice-dam risk scoring: insulation, recessed lights, fan vents, hatch/flue leaks, ventilation,
  geometry, gutters, history, snow depth.
- Snow-load math with 5 density classes and structural danger signals.
- Leak-in-progress playbook (drain the bulge, dry in 48 h).

## Real-world problem it solves

−8 °C, refreeze to −12 °C tonight, 60 m² driveway: the tool says 3.5 kg NaCl works but slowly —
and that evening anti-icing beats salting after, because the melt WILL refreeze. Meanwhile the
water stain upstairs traces to a 95/100 ice-dam risk driven by a bathroom fan venting into the
attic; the permanent fix costs a fraction of a roof rebuild.

## Scope & limits

Residential context, follow product labels. Roof work on ice is genuinely dangerous — the
playbook is ground-rake-first for a reason. Pure Python 3 stdlib. MIT license.
