---
name: grocery-flow-architect
description: "Use when grocery shopping takes too long, you always forget something, or you keep backtracking across the store. Builds a personal store map once, then sorts every list into exact aisle-by-aisle walking order, flags forgotten staples, and merges multi-store trips into one route."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [grocery, shopping, errands, list-optimization, route-planning, household]
---

# Grocery Flow Architect

## Overview

The average grocery run wastes 5-15 minutes on backtracking: you're in
produce, the list reminds you of milk, milk is at the far end, then the
bread you forgot sends you back past produce again. Multi-store trips are
worse — the same loop in two buildings plus the drive-between regret of
"why did I come here second?".

The fix is boring and effective: **know the store's zone order, walk it
once.** This skill:

1. **Store mapping (once per store, ~5 min):** you name the zones in
   walking order — the order you actually encounter them on your usual
   entrance-to-checkout path. Most stores resolve to 8-12 zones.
2. **List routing:** every item is matched to a zone (built-in matcher:
   ~180 common items; unknown items ask once, then remembered). The list
   is emitted **in exact walking order** with per-zone grouping.
3. **Staples radar:** your household's recurring items (milk, coffee,
   trash bags...) with "usual cadence" — flags the ones you've probably
   run out of by now. Catches the invisible forgetting.
4. **Multi-store merge:** when items span two stores, orders each list
   and suggests the store sequence (based on your declared trip frame:
   "grocery first, then the co-op").

Data lives in one JSON per store in `~/.grocery_flow/` — your map and
staples improve with use; unknown-item answers persist.

## When to Use

- Weekly grocery runs (the core case)
- "I always forget X" — staples radar
- Shopping with kids/partner under time pressure: ordered list = less
  wandering, fewer impulse buys
- Multi-store trips (supermarket + bakery + ethnic market + hardware)
- New-store onboarding: walk it once with the mapper, reuse forever
- Diet-specific repeats (koster/halal/vegan/gluten-free staples get the
  same radar treatment)

**Don't use for:** one-item pharmacy runs (no route to optimize), online
delivery carts (no walking), or warehouse runs where you genuinely must
traverse every aisle anyway.

## Files

| File | Purpose |
|---|---|
| `scripts/grocery_flow.py` | CLI: `map-store`, `route`, `staples`, `merge` |
| `references/item-zones.md` | The built-in item→zone matcher data + how to extend |
| `references/store-atlas.md` | Zone orders for common chain layouts (US/EU/RU) as starting points |
| `README.md` | The problem in 3 paragraphs |

## Usage

```bash
# 1. Map your store once (interactive: name zones in walking order)
python3 scripts/grocery_flow.py map-store --name kroger-main

# 2. Route a list into walking order
python3 scripts/grocery_flow.py route --store kroger-main list.txt

# 3. Same, with staples radar on
python3 scripts/grocery_flow.py route --store kroger-main list.txt --staples

# 4. Maintain your staples (add milk with ~5-day cadence)
python3 scripts/grocery_flow.py staples --store kroger-main add "milk" --days 5

# 5. Mark what you bought (updates radar timing)
python3 scripts/grocery_flow.py staples --store kroger-main bought "milk"

# 6. Two-store trip
python3 scripts/grocery_flow.py merge --stores kroger-main,coop list.txt
```

List format: one item per line; `!`-prefixed items are priority; zone
hints inline like `milk [dairy]` override the matcher.

## Workflow

1. First use: run `map-store` for your primary store. Walk it mentally
   from your usual entrance: name zones in order (produce, bakery, deli,
   dairy, frozen, meat, pantry, household, checkout...). Save.
2. Add staples with realistic cadences (the thing you ALWAYS forget goes
   in with a SHORT cadence).
3. Each run: dump the list to a text file (or let the agent do it),
   `route --staples`, screenshot/copy the output. Shop in order. Mark
   staples bought.
4. New store on vacation/after a move: 5-minute `map-store`, same lists.
5. Quarterly: review `staples list` — cadences drift (kids grow, seasons
   change).

## The matcher

Zone names are YOURS (mapper defines them), but a built-in table maps
~180 common grocery items to conventional zones (produce/dairy/frozen/
bakery/deli/meat/seafood/pantry/breakfast/beverages/snacks/household/
health/baby/pet). Unknown items prompt once (`route` asks "which zone is
X?" and stores the answer in the store's JSON for future runs). Singular/
plural and basic synonyms are normalized (tomatoes→tomato, soda→soft
drinks). See `references/item-zones.md` for the full table and extension
rules.

## Common Pitfalls

1. **Mapping the store in shelf order, not YOUR walking order.** The map
   must reflect your entrance-to-checkout direction. Two people in the
   same store can have opposite maps — both correct.
2. **Too many zones.** 8-12 is the sweet spot; more than 15 and you're
   maintaining a taxonomy, not saving time. Merge tiny zones.
3. **Staples cadence too optimistic.** "Milk every 3 days" when it's
   really 6 → radar noise → you start ignoring it. Set honest cadences;
   the radar learns from `bought` timestamps anyway.
4. **Routing at the door, not at home.** Route BEFORE leaving; the value
   is a sorted list you walk once, not a sorting exercise in aisle 1.
5. **Priority-marking everything.** `!` loses meaning past ~5 items.
   Reserve it for hard stops (pharmacy pickup, the one thing that
   justifies the trip).
6. **Frozen zone last — unless your map says otherwise.** Most routes
   should hit frozen near the end (melt time), and the mapper asks you
   where frozen sits on YOUR path; the router never reorders your zones,
   it only respects them.

## Example Session

> `route --store kroger-main tonight.txt --staples`
>
> ```
> KROGER-MAIN — route (entrance → checkout), 14 items, 9 zones
> [1 produce]   apples, avocados(!), lemons
> [2 bakery]    tortillas
> [4 dairy]     milk(!), yogurt            ← staples radar: milk likely out (6d since bought, cadence 5d)
> [6 meat]      chicken thighs
> [7 pantry]    rice, canned tomatoes, olive oil
> [10 household] trash bags                 ← radar: last bought 24d ago (cadence 21d)
> [11 frozen]   peas, ice cream
> unplaced: "that soap from the green aisle" → answered last time as household
> ```
>
> 22 minutes door-to-door, zero backtracks, and the trash bags didn't
> wait for the 2 AM discovery.

## Verification Checklist

- [ ] Store map exists and reflects YOUR walking direction
- [ ] Routed list preserves zone order exactly as mapped
- [ ] Unknown items were asked-and-remembered, not guessed silently
- [ ] Staples radar flags include days-since-bought vs cadence
- [ ] Frozen/last-zone items sit at the route tail (if your map allows)
- [ ] Multi-store merge routes each store separately and names the order
