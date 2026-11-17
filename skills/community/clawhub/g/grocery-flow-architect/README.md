# Grocery Flow Architect

**The average grocery run wastes 5-15 minutes backtracking. You're in
produce, the list says milk, milk is across the store — and the bread you
forgot sends you back again.**

## The problem

Shopping lists are written in *thinking order* (whatever you remembered,
in whatever order you remembered it), not *walking order*. So every run
is a random walk through the store: backtrack for dairy, backtrack for
the household aisle, pass the frozen section twice (ice cream soup by
checkout). Multi-store trips double the waste. And the stuff you're not
sure you have — milk, coffee, trash bags — either gets skipped (2 AM
discovery) or double-bought (the three-opened-ketchup problem).

## The solution

**Map your store once (5 minutes), route every list forever:**

1. **`map-store`** — name your store's zones in the order YOU walk them,
   entrance to checkout. Your entrance, your direction, your map.
2. **`route`** — any list gets sorted into exact zone-by-zone walking
   order. A built-in matcher (~180 common items, prefix rules like
   "frozen peas"→frozen, head-noun matching) places items; unknowns are
   asked once and remembered per store.
3. **`staples`** — your recurring items with honest cadences. The radar
   flags what's probably out ("milk: 7d since bought, cadence 5d") so
   the list is complete BEFORE you leave home.
4. **`merge`** — multi-store trips: each list routed in its store's
   order, with cold-chain and heavy-items store-sequencing advice.

State lives in `~/.grocery_flow/<store>.json` — maps, learned items, and
staple timestamps improve with every run.

## Quick start

```bash
# once per store
python3 scripts/grocery_flow.py map-store --name kroger-main

# add the things you always forget
python3 scripts/grocery_flow.py staples --store kroger-main \
    --add milk coffee "trash bags" --days 5

# every run: route + radar
python3 scripts/grocery_flow.py route --store kroger-main list.txt --staples

# after shopping
python3 scripts/grocery_flow.py staples --store kroger-main --bought milk coffee
```

## What you get

```
KROGER-MAIN — route (entrance -> checkout), 12 items, 7 zones
[ 1 produce]   apples avocados(!) lemons
[ 2 bakery]    tortillas
[ 3 dairy]     milk yogurt
[ 4 meat]      chicken thighs
[ 5 pantry]    rice canned tomatoes
[ 6 household] trash bags
[ 7 frozen]    ice cream frozen peas      ← melt-friendly: last zone

STAPLES RADAR (probably out or due):
  - milk: 7d since bought (cadence 5d)
  - trash bags: never marked bought (cadence 5d)
```

One pass through the store. Frozen last. The forgotten staples surfaced
before you left the house.

## Who needs this

- Weekly household shoppers (the 5-15 min × 50 runs/year math)
- Parents shopping with kids — ordered lists cut wandering and impulse
  requests
- Anyone who "always forgets one thing"
- Multi-store shoppers (supermarket + bakery + ethnic market)
- Meal-preppers with big structured lists

## Files

- `SKILL.md` — workflow, pitfalls, examples
- `scripts/grocery_flow.py` — map-store / route / staples / merge CLI
- `references/item-zones.md` — matcher data and extension rules
- `references/store-atlas.md` — common chain layouts as starting points

## License

MIT © Denis Voronin
