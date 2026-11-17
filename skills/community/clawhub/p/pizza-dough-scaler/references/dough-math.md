# Pizza Dough Scaling — Reference

## Why baker's percentages

Flour is always 100; every other ingredient is a percentage of
flour weight. Scaling a recipe from 2 doughs to 7 is then one
multiplication, and salt never silently doubles. Formula:

```
flour = total_dough_weight / (1 + hyd% + salt% + oil% + yeast% + sugar%)
water = flour × hyd%
salt  = flour × salt%   ... etc
```

## Ball weight targets (grams)

### Round pizzas (thickness factor in g/in² of pan area)
- 10" neo: 200-215g | 12" neo: 260-280g | 14" NY: 430-460g |
  16" NY: 530-560g | 18" NY: 650-700g
- Factors: neo 2.4-2.6, NY 2.8-3.0 (higher for a foldable
  street slice), bar/tavern 2.5-2.7 with oil

### Rectangular pans
- Detroit 8×10×2": 520-560g (two balls is fine — it's pan pizza)
- Detroit 10×14×2": 900-980g
- Sicilian full sheet 16×21×1": 1.5-1.7kg; half sheet 12×17:
  880-980g
- Grandma 12×17 (thin): 700-780g

Detroit depth rule: ~0.55-0.60 g per in² per inch of depth
covers the classic pans; dough should fill the pan ~1/3 before
proof, ~2/3 after.

## Flour classes and hydration feel

| Flour | Protein | Same-% feel vs bread flour | Advice |
|---|---|---|---|
| Caputo 00 pizzeria | ~12.5% | drier/harder to hydrate | 62-65% standard |
| Caputo 00 Americana / rinforzato | ~14% | closer to bread flour | use for NY/Detroit blends |
| Bread flour (KA Sir Lancelot tier) | 14%+ | baseline | 60-63% NY |
| All-purpose | 11-12% | wetter-reading, weaker | −5% hydration, best for grandma style |
| Whole wheat (partial) | — | thirstier | +3-5% hydration per 10% WW |

## Salt, oil, sugar by style

- Neo: 2.8-3.0% salt (Neapolitan tradition runs salty), 0 oil
- NY: 1.8-2.2% salt, 2-3% olive oil, 1-2% sugar optional (browns
  in a home oven)
- Detroit: 2.0-2.5% salt, 8-10% oil — half in dough, half in pan
- Sicilian: 2.0% salt, 3-5% oil

## Yeast deep-dive (instant dry yeast %; fresh = ×3; active dry = ×1.25)

Room temperature 21°C referents:
- 0.05% ≈ 8-10h RT
- 0.1% ≈ 5-6h RT
- 0.3% ≈ 3h RT
- 1.0% ≈ 1.5-2h RT

Cold ferment (4°C) slows activity ~4-5×, and the first hours at
RT before boxing matter — the script's schedule accounts for a
2h RT bulk before the fridge.

Temperature compensation (Q10 ≈ 2 per 10°C):
- Kitchen 16-18°C: ×1.3-1.5 yeast or ×1.3 time
- Kitchen 24-26°C: ×0.7 yeast or ×0.75 time

## Timeline worked example (bake Sat 19:00, 41h ferment, kitchen 18°C)

- Fri 01:30 — mix, knead 8-10 min (windowpane not required at
  this hydration; smooth is enough)
- Fri 01:45-03:45 — RT bulk ~2h (till +30-50%)
- Fri 03:45 — ball, into oiled deli boxes, fridge
- Sat 16:00-16:30 — out of fridge (Detroit: dough into oiled
  pan now, stretch gently during the hour)
- Sat 18:30 — RT dough balls press out easily; Detroit pan
  proofs to ~2/3 depth, sauced
- Sat 19:00 — bake (Detroit: 250°C bottom rack 12-14 min;
  neo stone 400°C+ 60-90s; NY 290°C stone 6-8 min)

## Gluten-free adaptation (short version)

Use a GF blend with xanthan; hydration reads 5-8% higher than
the recipe because there's no gluten to hydrate; skip the
windowpane concept entirely; ball weights +10-15% (no stretch,
press only). Detroit-style GF is the most forgiving shape.

## Freezing dough

Ball, oil lightly, freeze at peak cold-ferment (day 1-2). Thaw
overnight in fridge + 2h RT before use. Yeast survives; schedule
as "bake within 2 weeks." Don't refreeze.
