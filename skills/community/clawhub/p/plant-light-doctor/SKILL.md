---
name: plant-light-doctor
description: "Use when choosing plants for a specific window or diagnosing why a houseplant is leggy, pale, or not blooming. Computes real monthly light (DLI) for any window orientation, floor, and latitude, matches plants against light needs, and specs a grow light if nature is not enough."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [plants, gardening, houseplants, light, dli, grow-lights, indoor-gardening]
---

# Plant Light Doctor

## Overview

"Low light / medium light / bright indirect" is the least useful classification ever
applied to plants. Two windows in the same apartment can differ by a factor of 8 in
actual light delivered — and the same north window in Oslo vs. Athens is a different
planet. Meanwhile people buy fiddle-leaf figs for dark corners, watch them slowly
etiolate, and conclude they have a "black thumb".

This skill replaces vibes with physics. It computes **DLI (Daily Light Integral,
mol·m⁻²·day⁻¹)** — the horticulture industry's gold-standard light metric — for a
specific window: orientation, floor height, outdoor obstructions, latitude, sky
climate. It then matches that DLI against a library of common houseplants' actual
requirements, month by month, and delivers one of four verdicts: **THRIVES /
SURVIVES / STRUGGLES / IMPOSSIBLE**. If nature falls short, it sizes a grow light:
required PPFD, photoperiod, and realistic wattage.

## When to Use

- "What plants will survive in my north-facing window?" (or any orientation)
- "Why is my monstera leggy / why won't my orchid rebloom / why is everything pale?"
- "I live on the 1st floor across from a building — what can I actually grow?"
- "Do I need a grow light? Which one, how strong, how many hours?"
- "Can I grow herbs / lettuce / tomatoes / succulents on my windowsill?"
- Choosing a plant BEFORE buying it, for a specific spot in a specific home.
- Winter light audits ("everything dies in November") — seasonal DLI decline charts.

**Don't use for:** outdoor garden planning (use seed-calendar-planner style
frost-date logic), plant disease diagnosis, or watering/fertilizer questions.

## How It Works — the physics in 60 seconds

1. **Extraterrestrial irradiance.** Solar constant 1361 W/m², adjusted for day
   angle → clear-sky PPFD at ground level for each month (Bouguer-style model).
2. **Day length** per month from latitude (solar declination formula).
3. **Window capture model.** Direct sun hours on vertical glass by orientation
   (S gets max, E/W half, N ≈ diffuse only), scaled by:
   - floor penalty (ground floor + opposite building = big loss)
   - obstruction factor (user-reported 0-100% blockage during sun hours)
   - glass transmission (~85% typical double-glazed, tinted glass worse)
   - overhang/eave shading (reduces high summer sun more than low winter sun)
4. **Sky climate multiplier.** Cloudy oceanic (UK, PNW) vs. continental clear
   (interior US, Mediterranean) — up to 2× swing in delivered DLI.
5. **DLI = sum of (PPFD × seconds)** over the day → mol·m⁻²·day⁻¹ per month.
6. **Plant matching.** Each plant in the library has a DLI need range
   (e.g., herbs 8-14, lettuce 12-17, tomato 20-30+). Verdict rules:
   - window DLI ≥ need → **THRIVES**
   - within 15% below need → **SURVIVES** (slow growth, may not bloom)
   - 15-45% below → **STRUGGLES** (etiolation within months)
   - >45% below or <2 mol floor → **IMPOSSIBLE**
7. **Grow-light sizing.** Gap = (need − worst-month DLI). Required PPFD =
   gap × 10⁶ / (3600 × photoperiod). Then fixture wattage from efficacy
   (120 lm/W ≈ 2.3 µmol/J typical consumer LED boards).

## Files

| File | Purpose |
|---|---|
| `scripts/plant_light_analyzer.py` | Full CLI analyzer: DLI by month, plant verdicts, grow-light spec |
| `references/plant-dli-table.md` | DLI requirements for 40+ plants + symptom-to-light troubleshooting |
| `references/light-physics.md` | The full model, formulas, worked examples, measurement methods |
| `README.md` | Real-world problem statement |

## Usage

```bash
# Audit a north window in Berlin, 3rd floor, clear view
python3 scripts/plant_light_analyzer.py --orientation N --latitude 52.5 --floor 3

# South window, ground floor, opposite building blocks 70% of sun hours, cloudy city
python3 scripts/plant_light_analyzer.py --orientation S --latitude 41.0 --floor 1 \
    --obstruction 0.7 --climate cloudy

# Can I grow cherry tomatoes? Check a specific plant
python3 scripts/plant_light_analyzer.py --orientation E --latitude 50.1 --floor 2 \
    --check "cherry tomato"

# Include a grow-light recommendation
python3 scripts/plant_light_analyzer.py --orientation NW --latitude 55.7 --floor 5 \
    --grow-light --target-dli 14
```

## Workflow

1. Collect the facts (ask the user, or infer): **window orientation** (compass
   direction the window FACES — the direction you look when standing inside),
   **city or latitude**, **floor number**, **what's outside the window**
   (open street / trees / opposite wall at X meters), **glass type**.
2. Run the analyzer with those parameters. Read the monthly DLI table — note the
   worst month (usually December in the northern hemisphere).
3. Match plants: either `--check "plant name"` for a purchase decision, or read
   the ranked table of what thrives in THIS window.
4. If the user wants a plant the window can't support, size the grow light
   (`--grow-light --target-dli <need>`) — give PPFD, hours/day, and a realistic
   wattage + fixture-distance recommendation.
5. For "why is my plant sad" calls: cross-reference the symptom
   (references/plant-dli-table.md § Symptoms) with the window's verdict.

## Common Pitfalls

1. **Orientation confusion.** Users say "my window gets the morning sun" —
   that's an EAST window. The analyzer wants where the glass FACES. A window
   facing south in the northern hemisphere = sun-drenched; in Sydney/Buenos
   Aires (southern hemisphere) flip everything — the script handles this via
   latitude sign.
2. **"Bright indirect" folk wisdom.** Monstera "tolerates low light" means it
   survives at DLI 4, not that it thrives. Always quote the verdict tier, and
   set expectations for SURVIVES (slow, smaller leaves, no fenestration).
3. **Forgetting winter.** A south window in Hamburg is a jungle in July and a
   cave in December. Always check the monthly table — recommend plants by the
   WORST month, not the average.
4. **Over-trusting the model.** ±30% is honest. Nearby buildings, awnings,
   balconies, screens, and net curtains can dominate. When the user reports a
   big obstruction, trust `--obstruction` over theory.
5. **Grow-light distance.** PPFD falls with the inverse square of distance.
   The script's wattage figure assumes 30-45 cm above canopy for small fixtures.

## Example Session

> **User:** "What can I grow on a north-facing windowsill, 4th floor, Helsinki?"
>
> Run: `--orientation N --latitude 60.2 --floor 4 --climate cloudy`
> Output: worst-month DLI ≈ 1.2 (December), summer peak ≈ 4.
> Verdicts: pothos/ZZ/snake plant SURVIVE, herbs STRUGGLE, lettuce IMPOSSIBLE.
> Recommendation: accept foliage plants, or add a 20 W full-spectrum bar
> (≈ 250 µmol/m²/s at 30 cm) for 12 h/day to unlock herbs and lettuce.

## Verification Checklist

- [ ] Worst month identified and quoted in the answer
- [ ] Every plant recommendation tied to a verdict tier, not vibes
- [ ] Hemisphere handled (southern latitude flips S/N exposure)
- [ ] Grow-light spec includes PPFD + hours + wattage, not just "buy a lamp"
