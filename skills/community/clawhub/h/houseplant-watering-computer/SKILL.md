---
name: houseplant-watering-computer
description: Use when houseplants keep dying or schedules feel like guesswork — computes real soil water balance per pot (substrate water-holding capacity, pot volume, plant size leaf area, light level, temperature/VPD, humidity), tells you HOW MUCH and HOW OFTEN to water, detects over- vs under-watering symptoms, handles self-watering pots and cache pots, and generates a per-pot care card with moisture-check dates.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [houseplants, watering, plants, soil-moisture, gardening, plant-care]
---

# Houseplant Watering Computer

"Water weekly" is why houseplants die. The right question is: **how fast
does THIS pot dry out?** — a function of substrate water-holding capacity,
pot volume, plant size, light, temperature, and humidity. This skill
computes the soil water balance per pot and turns it into an actionable
answer: how much water, how often, and when to check next.

## When to Use

- New plant, no idea how often to water it
- Repeated plant deaths (root rot = overwatering is the #1 killer)
- Changing seasons: the winter schedule isn't the summer schedule
- Repotting: substrate change changes everything
- Setting up self-watering pots / cache pots correctly
- Symptoms: yellowing, wilting despite wet soil, fungus gnats

**Don't use for:** hydroponics (different physics), outdoor gardens (rain
dominates — use ET-based scheduling), lawns.

## The Method

1. **Inventory each pot:** substrate mix, pot dimensions (top/bottom
   diameter + height), plant size class, light level, room temp/humidity.
2. **`compute`** — per-pot physics:
   - Substrate WHC (water-holding capacity) L per L of soil from the mix
   - Pot volume from truncated-cone geometry (tapered pots) or cylinder
   - Plant water use from leaf area proxy + light + VPD (vapor pressure
     deficit from temp/RH)
   - → **Dryout time**: days from saturation to the plant's wilt/watering
     point, with the usable reservoir in mL and per-watering dose in mL
3. **`check`** — interpret what you observe (finger test depths, moisture
   meter readings, weight) into wet/dry verdicts and next-check timing.
4. **`symptoms`** — route visual symptoms to over- vs under-watering and
   other causes; fungus gnat lifecycle breaks.
5. **`selfwatering`** — reservoir sizing and fill cadence for wick/cache
   pots; when NOT to use them (mines: always-wet substrate + rot-prone
   species).

## Quick Start

```bash
# Monstera in a 24cm tapered pot, peat-based mix, bright indirect, 22C/45%RH
python3 scripts/watering_computer.py compute --substrate peat-mix --pot-tapered 24,18,22 \
    --plant large-foliage --light bright-indirect --temp 22 --humidity 45

# Check what I'm feeling in the pot right now
python3 scripts/watering_computer.py check --finger-depth shallow --feels dry --pot-tapered 24,18,22

# Diagnose: yellow lower leaves + fungus gnats + soil stays wet 10+ days
python3 scripts/watering_computer.py symptoms --yellowing lower --soil wet --gnats

# Self-watering pot reservoir sizing
python3 scripts/watering_computer.py selfwatering --pot-tapered 24,18,22 --substrate peat-mix --away-days 21
```

Stdlib-only Python 3. Offline.

## Substrate Science (what drives everything)

| Mix | WHC (mL/L) | Dryout | Best for |
|---|---|---|---|
| Peat/coir-based potting mix | 450–550 | Medium | Most tropicals, foliage |
| Heavy garden soil in a pot | 600+ | Very slow | Nobody — compacts, rots |
| 50/50 peat + perlite | 380–430 | Faster | Seedlings, succulent-adjacent |
| Succulent/cactus mix | 250–320 | Fast | Sansevieria, succulents, cacti |
| Bark-heavy aroid mix | 180–250 | Very fast | Philodendron, orchid-adjacent |
| Semi-hydro (LECA) | 300–400 | Wick-driven | Cache-pot setups |

The watering INTERVAL the plant experiences is substrate × pot size ×
demand — never a calendar. A peat mix in a 12 cm pot dries in ~3 days in
summer; the same plant in a 24 cm pot takes 7–9.

## Environment Multipliers (VPD)

Demand scales with warmth and dryness of air. The script computes vapor
pressure deficit from temp + RH and multiplies plant water use:

- 18 °C / 70% RH → ×0.6 (winter, slow everything)
- 22 °C / 45% RH → ×1.0 (baseline)
- 26 °C / 30% RH → ×1.6 (heatwave, AC, radiator proximity)

Winter heating is the hidden killer: soil stays cold and wet (slow uptake)
while air is dry — check less, water less, don't fertilize.

## Common Pitfalls

1. **Calendar watering.** The #1 killer. Moisture-check before every
   watering for the first month with any new pot; the calendar emerges
   from the physics, per pot.
2. **Watering on a schedule that ignores pot size.** Same plant, doubled
   pot volume → interval nearly doubles. Small pots dry in days; big pots
   hold a hidden reservoir for a week+.
3. **"Drainage fixes overwatering."** Drainage holes move water OUT after
   saturation; they do nothing for a substrate kept continuously wet by
   too-frequent watering.
4. **Even soak vs splash.** A 200 mL splash on a 6 L pot wets the top
   2 cm, salts accumulate in the root zone, and the bottom roots stay dry.
   Water to ~20–25% of substrate volume, until slight runoff.
5. **Cold tap water on tropicals.** Let it reach room temperature; some
   species are sensitive to chlorine — overnight resting resolves both.
6. **Repotting into "bigger is better."** Too large a pot = wet soil the
   roots never reach = rot. Go up ≤ 5 cm in diameter.
7. **Self-watering pots as a cure for underwatering.** They fix interval
   management, not light/substrate problems; rot-prone species need a
   timer-free setup or a very airy mix.

## Verification Checklist

- [ ] Pot measured (top, bottom diameters, height) — tapered ≠ cylinder
- [ ] Substrate identified honestly (what's actually in the pot)
- [ ] Light level honestly assessed (what hits the plant, not the window)
- [ ] `compute` output dose is ~15–25% of substrate volume
- [ ] Finger/weight check performed before acting on any interval > 4 days
- [ ] Winter: interval stretched, fertilizer stopped

## References

- `references/water-balance.md` — the physics: WHC, pot geometry math, VPD
  tables, plant demand classes, dryout-time derivation
- `references/symptom-router.md` — full visual symptom routing table,
  fungus gnat protocol, self-watering/cache-pot engineering
