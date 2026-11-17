---
name: party-provisioner
description: "Calculate exact quantities of drinks, ice, food, glassware, and supplies for parties and events from headcount, duration, guest mix, and weather. Uses bartender-standard consumption math (drinks per guest-hour), splits beer/wine/spirits by drinker preferences, applies food-per-hour catering rules, and sizes ice in pounds. Use when planning any party, BBQ, wedding, holiday dinner, or gathering and asking how much alcohol, soda, ice, or food to buy."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [party, event-planning, catering, drinks, alcohol, ice, hospitality, hosting]
---

# Party Provisioner 🎉

"How much should I buy?" — the question every host asks, usually answered by
panic-buying 30% too much or running dry at hour two. This skill computes
provisioning from the four variables that actually matter: **how many
guests, how long, what mix of drinkers/eaters, how hot is it** — using the
same per-guest-hour arithmetic bartenders and caterers use.

## Overview

The core unit is the **guest-hour**: a guest consumes X units per hour, so a
4-hour party for 20 is 80 guest-hours regardless of how you slice it.
`scripts/party_planner.py` implements:

**Drinks** (a "drink" = 1 beer / 1 glass of wine / 1 cocktail-served shot)
- Baseline: 2 drinks in the first hour, 1 per hour after (industry standard)
- Adjustments: heat (+20%), dancing/active event (+10%), light drinkers
  (−20%), wine-only crowd (1.5 glasses/hr)
- Mix split: from drinker preferences (e.g. 40/40/20 beer/wine/spirits)
- Units out: **beer bottles, wine bottles (5 glasses each), 750ml spirit
  bottles (17 shots)**, mixers, plus water/soda for non-drinkers & hydrating
  drinkers
- Round-up rules so you don't buy 0.8 bottles

**Ice**: 1.5 lb per drinking guest-hour + 1 lb per bag cooler + bar ice for
chilling bottles (formula from catering guides: ~1 lb/person for the
evening + chilling needs)

**Food** (per guest-hour, catering norms):
- Meal party: 1.2 lb total food/person for a 2-3h dinner
- Appetizer party: 12 bites/hour/person
- BBQ: ½ lb protein/person/meal (⅓ lb sides)
- Kids count ½, big eaters 1.5×

**Extras**: glassware (2 per guest, or 1 + rotates), plates ×1.5 servings,
napkins ×3, cups, trash bags, tables/chairs per seating standards

## When to Use

- "I'm hosting 25 people Saturday night — how much wine and beer?"
- "Backyard BBQ for 40, kids included, how many burgers and how much ice?"
- "Wedding reception, 80 guests, 5 hours, beer/wine only"
- "How many bottles of prosecco for a 3-hour brunch for 15?"
- "Cocktail party, no dinner — how many appetizers?"

**Don't use for:** commercial/cash-bar operations (licensing, stock
management), huge catered events with pro event planners (they have vendor
math), or dietary-restriction menu design (different problem).

## How It Works — Steps

1. **Headline numbers**:
   ```bash
   python3 scripts/party_planner.py --guests 25 --hours 4 --style cocktail
   ```
2. **Refine the crowd**:
   ```bash
   python3 scripts/party_planner.py --guests 40 --hours 5 --style bbq \
     --drinkers 30 --kids 10 --heat --mix 40/40/20
   ```
3. **Read the shopping list** — bottles, lbs, bites, and units to actually
   buy (with round-up), grouped by store section.
4. **Budget check** — enter unit prices (`--price-beer 1.2`) for a cost
   estimate per category and total.
5. **Print the host card** — ratios to remember, timing notes (what to
   chill when), and the "running low?" tripwires.

## Consumption Model (per drinking guest)

```
drinks(guest) = 2 × adj_first_hour + adj_1_per_subsequent_hour
adj = base × heat(1.2 if >27°C) × active(1.1) × light(0.8)
non-drinkers: 2 non-alc drinks/hr (soda/water/coffee-tea)
```
Wine-only event: 1.5 glasses/hr flat. Champagne toast: +1 glass/guest.

## Worked Example

```
40 guests (30 drinkers, 10 kids), 5h BBQ, hot day, mix 40/40/20:
  guest-hours: 150 drinker-hours → base drinks = 2+4 = 6/drinker
  heat adj ×1.2 → 7.2 drinks × 30 drinkers = 216 drinks
  split: 86 beer + 87 wine glasses + 43 cocktails
  BUY: 90 beer bottles · 18 wine bottles · 3×750ml spirits · 43 mixer-servings
  non-alc: 300 servings (200 sodas + 100 water/coffee)
  ICE: 3 × 20lb bags minimum (plus chilling)
  FOOD: 12.5 lb protein + sides + kid adjustments
  extras: 80 cups, 60 plates, 180 napkins, 4-5 trash bags
```

## Common Pitfalls

1. **Sizing by "drinks per person" without duration.** A 2-hour dinner and a
   6-hour party are different planets — always guest-×-hours.
2. **Forgetting non-drinkers** get thirsty too. Budget 2 non-alc
   drinks/hour/guest — running out of water is the #1 real-party failure,
   and on a hot day it's a safety issue.
3. **Wine bottle math** — a 750ml bottle is 5 glasses, not 4 (poured at
   150ml catering standard). Underestimating here runs dry in hour one.
4. **Ice melts.** Bagged ice for coolers needs ~1 lb/person extra; crushed
   bar ice for cocktails melts ~30% faster. Buy more than the formula if
   it's >27°C.
5. **Kids eat half but drink like adults** (of non-alc). Count them in
   drinks, halve them in food.
6. **No round-up = buying 0.8 bottles.** The tool rounds beer to 6-packs,
   wine to bottles, spirits to 750ml — keep that.
7. **Champagne "toast inflation"**: a toast pour is 100ml, not a full glass
   — 8 glasses/bottle for toast purposes.

## Verification Checklist

- [ ] Drinks ÷ drinkers falls in 0.8–2.5/hour band (sanity)
- [ ] Non-alc servings ≥ 1.5 × guest-hours
- [ ] Ice ≥ 1 lb × drinking guests for the evening (plus cooler ice)
- [ ] Every buy-line is a whole purchasable unit
- [ ] Water available matches heat adjustment (hot day → +20% everything)

## One-Shot Recipes

**Dinner party, 8 friends, 3 hours, wine-forward:**
```bash
python3 scripts/party_planner.py -g 8 -t 3 --style dinner --mix 20/60/20
```

**Wedding, 80 guests, 5h, beer & wine only, champagne toast:**
```bash
python3 scripts/party_planner.py -g 80 -t 5 --style reception --drinkers 60 \
  --mix 50/50/0 --toast
```

**Kid birthday, zero alcohol focus:**
```bash
python3 scripts/party_planner.py -g 20 -t 3 --style birthday --kids 12 --drinkers 0
```
