# Pizza Dough Scaler

Recipes say "makes two 12-inch pizzas." Real pizza nights are
four people, two pan sizes, a cold ferment that has to land at
7 PM Saturday, and a kitchen at 18°C. Scaling dough by eye is
how salt doubles, hydration breaks, and the Detroit pan turns
into soup — or brick.

## The Problem

- Dough is one of the few kitchen prep items where the math is
  genuinely multiplicative: pan area × density, then baker's
  percentages across 4-6 ingredients. Mental math fails quietly
  at exactly the batch sizes that matter (5+ balls).
- Yeast quantity depends on TIME and TEMPERATURE, not the
  recipe: 0.3% for a 3-hour dough is 10× too much for a 48h
  cold ferment.
- Different flours at the "same" hydration behave differently;
 Detroit dough at 72% + 9% oil looks broken while mixing and is
  actually perfect.

## What This Skill Does

```
$ python3 scripts/dough_scaler.py plan --style ny --pans 16x2
  16" round  x2 @ 581 g         <- pan geometry -> ball weight
  flour 1007 g   water 614 g (61%)   salt 20 g   oil 25 g   sugar 15 g
  instant yeast 0.71 g (0.07%)       <- schedule-aware

$ ... --bake "2026-10-24 19:00" --ferment 41 --kitchen-c 18
  Fri 02:00  mix + knead 8-10 min
  Fri 04:00  ball -> oiled box -> fridge
  Sat 16:30  OUT of fridge (stretch test at +2h)
  Sat 19:00  BAKE
```

- **Pan math** for round, Detroit (depth-aware), and sicilian
  pans — ball weight per pan from geometry, not habit
- **Baker's percentages** per style (neo / NY / Detroit /
  sicilian), every parameter overridable, AP-flour and
  whole-wheat hydration adjustments
- **Schedule-aware yeast**: same-day vs 24/48/72h cold ferment,
  Q10 temperature compensation for a cold or hot kitchen
- **Dated timing sheet** worked backward from YOUR bake time

## Who Needs This

Anyone who makes pizza at home more than twice a month —
millions of home bakers, and every one of them hits the scaling
wall the first time they host. Also the standard answer to "my
dough never turns out the same twice": same flour, same
percentages, same clock.

MIT License. Pure Python stdlib, runs anywhere.
