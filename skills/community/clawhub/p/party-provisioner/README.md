# Party Provisioner 🎉

**Exactly how much beer, wine, ice, and food to buy for the party — not
"some", not "way too much".**

Every host either panic-buys 30% extra or runs dry at hour two. The fix is
the same math bartenders and caterers use: consumption scales with
**guest-hours**, adjusted for heat, activity, and crowd. This tool runs
that math and outputs a purchasable shopping list.

## What it does

- **Drinks**: 2 in the first hour + 1/hour after (industry standard), split
  by your beer/wine/spirits mix, converted to **6-packs, wine bottles
  (5 glasses each), 750ml spirits (17 shots)** — with round-up
- **Heat/active/light-crowd adjustments** (+20% / +10% / −20%)
- **Non-alcoholic budget** — the #1 real-world failure (2 servings/hr per
  non-drinker + drinker hydration)
- **Ice in 20lb bags** (1.5 lb/drinker + heat scaling)
- **Food by style**: dinner lb, cocktail bites/hr, BBQ protein+sides,
  birthday cake/kid food — kids count ½
- **Supplies**: cups, plates, napkins, trash bags, TP
- **Budget** estimate with your local unit prices
- Champagne toast mode (8 pours/bottle)

## Quick start

```bash
# Backyard BBQ: 40 guests, 30 drinkers, 10 kids, hot day
python3 scripts/party_planner.py -g 40 -t 5 --style bbq --drinkers 30 --kids 10 --heat
```

```
🥂 DRINKS
  total alcohol servings: 216 drinks
  beer      : 90 bottles (15 six-packs)
  wine      : 18 bottles (5 glasses each)
  spirits   : 3 × 750ml (17 shots each)
  non-alc   : 210 servings
🧊 ICE
  6 × 20 lb bags
🍽️ FOOD
  protein 17.5 lb · sides 35.0 lb
```

```bash
# Wedding reception, beer+wine, toast, budget check
python3 scripts/party_planner.py -g 80 -t 5 --style reception --drinkers 60 \
  --mix 50/50/0 --toast --active --price-beer 1.5 --price-wine 9
```

## Why it matters

- The average household hosts several gatherings a year; systematic
  over-buying wastes $50-150 per event, and under-buying ends parties
  early. Event size × frequency = billions in the US alone.
- The knowledge exists in catering manuals; nobody reads them at 6pm in a
  store aisle. This puts the per-guest-hour arithmetic where the decision
  happens.

## Files

- `SKILL.md` — agent-facing usage guide
- `scripts/party_planner.py` — the calculator (stdlib only)
- `scripts/test_party_planner.py` — self-tests
- `references/provisioning-math.md` — every constant, catering norms, host
  timing checklist, responsible-hosting notes

## Test

```bash
python3 scripts/test_party_planner.py
```

MIT © 2026 Denis Voronin
