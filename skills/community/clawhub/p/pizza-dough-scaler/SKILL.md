---
name: pizza-dough-scaler
description: Use when making pizza dough for any pan size and count — neo-neapolitan, NY-style, Detroit, sicilian, or gluten-free — from one dough ball; computes ball weight from pan dimensions (Detroit pan area math, 16-inch round area), hydration for your flour and oven, salt/oil/yeast by baker's percentages, cold-ferment vs same-day yeast schedules, and a per-step timing sheet so 4 doughs for a 16-inch + 2 Detroit pans never turn into guesswork.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pizza, dough, baking, baker-percentages, detroit, neapolitan, scaling, kitchen]
---

# Pizza Dough Scaler

Every pizza dough recipe on the internet is written for one
specific dough ball — "makes two 12-inch pizzas." Your Friday
night is four people, a 16-inch round stone AND two 8×10
Detroit pans, the kitchen is 18°C, and you want to bake
tomorrow evening. Converting flour/water/salt/yeast by hand at
9 PM is where baking turns into improvisation.

This skill does the arithmetic that professional pizzerias have
on a spreadsheet:

- **Ball weight from pan geometry** — round (πr² × g/in²),
  Detroit/sicilian (length × width × depth factor), neo thin
  vs NY floppy vs Detroit thick target densities
- **Baker's percentages** — everything scales from flour = 100%:
  water (hydration % by style AND flour strength), salt 2-3%,
  oil 0-10% (style-dependent), yeast (0.02-0.25% by schedule)
- **Yeast scheduling** — same-day (~1% instant at RT) vs
  24-48h cold ferment (~0.05-0.15%), with temperature
  compensation (Q10 rule of thumb: ±7°C doubles/halves rate)
- **Output** — gram-precise ingredient list + dated timing
  sheet (mix → autolyse → ball → cold/RT box → out-of-fridge
  → bake), scaled to YOUR pan count

## When to Use

- Any pizza night beyond "one recipe, one pizza": different pan
  sizes, a crowd, mixed styles
- Scaling a recipe up/down without percentage math errors (the
  #1 dough failure: salt doubling when you halve flour)
- Planning a cold ferment around a KNOWN bake time (party
  Saturday 7 PM → when to mix)
- New flour (00 vs bread flour vs all-purpose) — hydration
  guidance per flour class so 65% on 00 isn't 65% on King Arthur
- Detroit/sicilian pans where "hydration" also interacts with
  oil (fat coats gluten, dough feels drier than it reads)

Don't use for: sourdough-style naturally leavened doughs (starter
percentage feeding math is a different skill), or focaccia (close
cousin — the numbers work but pan density differs; use the
sicilian setting as approximation).

## The Model

### Ball weight by style (target dough density)

| Style | Thickness factor (g per in²) | Typical ball |
|---|---|---|
| Neo-Neapolitan (63-65% hyd) | 2.4-2.6 | 260-280g / 12" |
| NY-style (60-63%) | 2.8-3.0 | 530-560g / 16" |
| Detroit (70-75% hyd + oil) | pan volume: L×W×0.35 g/in³... see below | 520-560g / 8×10 |
| Sicilian / grandma (65-70%) | 3.4-3.8 | 880-980g / 12×17 sheet |

- Round pan: `ball = π × (d/2)² × thickness_factor`
- Rectangular pan: `ball = L × W × thickness_factor` (Detroit:
  use depth-aware density, ~0.55-0.60 g per in² per inch of
  pan depth is a safe target for the classic 2" pan)

### Flour, hydration, salt, oil (baker's %)

Style presets in the script, all overridable:

| Style | Hydration | Salt | Oil | Notes |
|---|---|---|---|---|
| Neo-Neapolitan | 62-65% | 2.8-3.0% | 0% | 00 flour, short mix |
| NY | 60-63% | 1.8-2.2% | 2-3% | bread flour, sugar 1-2% optional |
| Detroit | 70-75% | 2.0-2.5% | 8-10% | oil is structural here |
| Sicilian | 65-70% | 2.0% | 3-5% | sheet pan, focaccia-adjacent |

Flour class adjustment: all-purpose absorbs ~5% less water than
bread flour; 00 is its own world (feels drier at same %). If your
dough ever soups out, drop hydration 3% before blaming the yeast.

### Yeast by schedule (instant dry, % of flour)

| Bake in | RT 21°C | Cold ferment fridge 4°C |
|---|---|---|
| same day 6-8h | 0.30-0.50% | — |
| same day 3-4h | 0.60-1.00% | — |
| 24h cold | — | 0.10-0.15% |
| 48h cold | — | 0.04-0.08% |
| 72h cold | — | 0.02-0.04% |

Kitchen at 18°C? Add ~30-50% more yeast or time. At 26°C+? Cut
yeast or expect aggression. The Q10 heuristic: every 8°C cooler
≈ rate halves.

## Pitfalls

1. **Scaling salt/yeast linearly by eye.** "A bit less" on a
   5-flour-bowl batch is how 3% salt becomes 4.5% (inedible) —
   the whole point of baker's percentages is that this never
   happens. The script prints grams for EVERYTHING.
2. **Same hydration, different flour.** Switching to a new flour
   at the same % can soup or brick the dough. Change one thing:
   -3% hydration first.
3. **Detroit hydration panic.** 72% + 9% oil looks like batter
   when mixing. It's correct — the oil transforms it during
   ferment. Don't add flour.
4. **Cold ferment yeast overdose.** 0.3% yeast for a 48h cold
   ferment = overproofed pancake by hour 30. The schedule table
   is not decoration.
5. **Ball weight → pan size mismatch.** 260g stretched to 16"
   is a cracker; 550g into 12" is focaccia. Ball weight comes
   FROM pan math, not habit.
6. **Timing sheet ignored.** Dough out of fridge 2-3h before
   bake (Detroit/sicilian: 1-1.5h + pan warm-up). Cold dough
   won't stretch, hot dough tears. The printed sheet has clock
  times — follow it.

## Verification Checklist

- [ ] Pan dimensions measured (rim-to-rim, not eyeballed)
- [ ] Ball weight computed per pan, total dough = Σ balls
- [ ] Flour = total / (1 + Σ percentages), scaled to gram
- [ ] Hydration matched to flour class (−5% for AP, watch 00)
- [ ] Yeast % picked from the SCHEDULE table, not habit
- [ ] Timing sheet printed with actual clock times, fridge
      pull-time highlighted

## Quick Recipe

```
# 2× 16" NY + 2× 8x10 Detroit, bake Saturday 19:00, 41h cold ferment
python3 scripts/dough_scaler.py plan --style ny --pans 16x2
python3 scripts/dough_scaler.py plan --style detroit --pans 8x10x2x2
python3 scripts/dough_scaler.py plan --style ny --pans 16x2 \
    --bake "2026-10-24 19:00" --ferment 41 --kitchen-c 18
```

Output: per-ball weight, total flour/water/salt/oil/yeast in
grams, and a dated schedule (mix time = bake − ferment −
room-temp final proof).
