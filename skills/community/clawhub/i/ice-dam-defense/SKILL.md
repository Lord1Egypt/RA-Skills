---
name: ice-dam-defense
description: "Use when winter ice strikes — planning sidewalk/driveway de-icing (which salt works at what pavement temperature, how much to spread per m², refreeze warnings, pet/concrete/plant safety) or diagnosing roof ice-dam risk and snow load (attic heat-leak scoring, roof-rake urgency, safe dam removal, leak response)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [winter, ice-dams, snow-removal, de-icing, home-maintenance, roof]
---

# Ice Dam Defense

## Overview
Two winter failures dominate homeowner help-line calls: **"I spread salt and nothing happened"**
(because pavement was colder than salt's effective range — NaCl stops melting at −9 °C pavement
temp even though the bag implies more), and **"my roof is leaking at the eave"** (an ice dam:
warm attic air melts roof snow, water refreezes at the cold eave, and the backed-up lake wicks
under the shingles).

This skill attacks both with real physics and chemistry:

- **sidewalk** — melt chemistry per material (NaCl/MgCl₂/CaCl₂/acetates/sand), application rate
  in kg for your actual area, works-at-this-temp verdict, refreeze/black-ice warnings, and
  pet/concrete/plant corrosion profiles.
- **roof** — a 10-factor ice-dam risk score (0-100) from attic heat leaks, snow-load estimate
  (depth × density × area → kg and % of typical capacity), removal urgency ladder, and the
  stop-the-leak-now playbook.

## When to Use
- "It's −15 °C — should I salt the driveway or is that pointless?"
- "How much de-icer do I actually need for a 60 m² driveway?"
- "Is rock salt bad for my dog / my new concrete / my lawn?" (yes/yes/yes — see alternatives)
- "There's an ice dam on my eave and water is coming through the ceiling."
- "Is 40 cm of snow on my roof too much?" (snow-load math)
- "I get ice dams every winter — why, and what's the permanent fix?"

**Don't use for:** arctic/alpine expedition planning, municipal road program design, or
flat-commercial-roof engineering (different codes).

## How It Works — Numbered Steps
1. **Sidewalk:** get PAVEMENT temperature (an IR thermometer on the surface; air temp is only
   a proxy — pavement radiates colder at night).
2. `python3 scripts/ice_dam_defense.py sidewalk --area-sqm 60 --temp-c -8 --material rock-salt --refreeze -12`
   → kg to apply, works-or-not verdict, warnings, material profile.
3. If the verdict says below-effective-range, switch `--material` (cacl2 to −25 °C, kac-acetate
   for corrosion-free, sand-ash for pure traction below that) and re-run.
4. **Roof:** estimate snow depth and type on the roof; answer the heat-leak flags you know.
5. `python3 scripts/ice_dam_defense.py roof --depth-cm 45 --roof-sqm 120 --insulation-poor --past-dams ...`
   → risk score, snow load vs typical 180 kg/m² capacity, urgency, playbook.
6. Follow the urgency ladder: rake from the ground; never climb an iced roof; never chip dams.

## De-Icer Quick Table

| Material | Works to (pavement) | Speed | Corrosion | Pets/Plants | Best for |
|---|---|---|---|---|---|
| Rock salt (NaCl) | −9 °C | slow (<−5 °C) | high | harsh | cheap bulk, mild temps |
| MgCl₂ | −15 °C | fast | moderate | milder | cold snaps, patios |
| CaCl₂ | −25 °C | fastest (exothermic) | mod-high | rinse paws | deep cold, blends |
| KAc acetate | −25 °C | fast | negligible | safe | airports, prized concrete |
| CMA | −9 °C | slow | negligible | safe | fresh concrete (<1 y) |
| Sand/ash | traction only | — | none (clogs drains) | safe | below −20 °C, always-slick spots |

Rates: ~12-40 lb per 1000 sq ft (light anti-ice → heavy compacted ice); the script converts to
kg for your area. More is NOT faster — just saltier runoff.

## Common Pitfalls
1. **Salting deep snow.** De-icers melt thin films, not 5 cm of snow — shovel first, chemical
   second. Salt on snowpack = wasted product + chloride soup.
2. **Trusting air temperature.** Pavement can be 5-8 °C colder than air at night; the whole
   works/doesn't-work verdict flips on this.
3. **Ignoring the refreeze.** Melted brine at 4 PM becomes black ice at 2 AM when the overnight
   low drops; either anti-ice early evening or plan a second pass.
4. **Chopping the dam.** Axes and hammers crack shingles and decks; dams are removed by melting
   channels (CaCl₂ sock) or professional steam, not force.
5. **Climbing the roof.** Ice + ladder + cold = the actual killer in this scenario. Roof rake
   from the ground reaches the critical lower 1.5 m.
6. **Treating the dam, not the attic.** Dams are a heat-leak symptom: air-seal the hatch,
   lights and flues; R-49+ insulation; working soffit/ridge vents. Heating cables are a
   band-aid for unfixable attics.
7. **Rock salt on new concrete.** Chloride + freeze-thaw pits young concrete — CMA or sand only
   in the first year.
8. **Wet-snow miscounting.** Wet snow is 4× heavier than fresh; snow-load math must use the
   right density (the script takes `--snow-type`).

## Example
```
Homeowner: "45 cm of snow, icicles at the eave, water stain on the ceiling
upstairs. It's −8 °C. Also I already salted the driveway twice, nothing."

$ python3 scripts/ice_dam_defense.py roof --depth-cm 45 --roof-sqm 120 \
    --insulation-poor --recessed-lights --past-dams --valleys-dormers --deep-snow-on-roof
Snow load: ~8,100 kg (38% of typical capacity) -> weight OK
Risk score: 95/100 -> HIGH ice-dam risk
 1. NOW: roof-rake lower 1-1.5 m + valleys from the ground.
 2. NEVER chip the dam; CaCl2 sock across it melts a drain channel.
 5. Interior: bucket + plastic, drain-hole a bulging ceiling, dry in 48 h.
Fix list (spring): air-seal attic, R-49+, check fan vents reach the exterior.

$ python3 scripts/ice_dam_defense.py sidewalk --area-sqm 60 --temp-c -8 \
    --material rock-salt --refreeze -12
APPLICATION: 3.52 kg — NaCl works at -8C but slowly; refreeze -12C tonight
means the melt WILL become black ice: anti-ice early evening instead.
```

## Safety Note
Roof work on ice kills people — ground-rake only. Structural snow loads vary by code and roof
condition; at any sign of creaking, sagging, or jammed doors, leave and call a professional.
Chemistry data reflects typical commercial de-icer products; follow the product label.

## References
- `references/deicer-chemistry.md` — eutectics, exothermics, application rates, brine making,
  concrete/pet/plant damage details, environmental notes.
- `references/ice-dam-mechanics.md` — the dam physics, the 10 risk factors with weights,
  snow-density table, load capacity context, permanent-fix spec list.
