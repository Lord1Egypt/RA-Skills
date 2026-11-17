# The Price Book Method — Reference

## Why a Price Book Works

Grocery pricing is deliberately noisy. The same item swings 30-40% between
stores, and "sales" are scheduled against known demand cycles. Shoppers who
know the *normal* price of their 20-30 core items make better decisions than
anyone relying on shelf labels, because:

1. **Unit prices expose package-size tricks.** A "value" 6-pack can cost more
   per liter than the single. Only price-per-unit comparisons catch this.
2. **Price history exposes shrinkflation.** When the box shrinks 500g→440g at
   the same price, the shelf price looks stable and the unit price jumps 13.6%.
   Two observations months apart prove it.
3. **Basket-level store comparison beats averages.** "Store X is 18% cheaper"
   marketing is computed on a basket THEY choose. Your basket is what matters:
   if you buy mostly store-brand staples, the ranking inverts.

## Size Parsing Rules

The parser normalizes to grams / milliliters / count:

| Input | Parsed as | Normalized |
|---|---|---|
| `500g`, `0.5kg`, `2.5kg` | metric weight | grams |
| `1lb`, `16oz` | US weight | grams (453.6g = 1lb) |
| `750ml`, `1L`, `1.5L` | metric volume | milliliters |
| `1gal`, `1qt`, `1pt`, `12floz` | US volume | milliliters |
| `12ct`, `12-count`, `6 pack` | countable | count |
| `6x1L`, `24x330ml` | multipacks | total (6L, 7.92L) |

Bare numbers (`--size 12`) are treated as count. Unknown tokens return
`(None, None)` — the item is still logged, just without unit-price math. When
in doubt, print the interpreted unit and correct on the next entry.

## Item Naming Discipline

The fuzzy matcher strips case, punctuation, and size suffixes: `Butter 250g`,
`BUTTER`, and `butter` are one item. But `Butter` and `Butter salted` are two.
Keep names **short + brand + variant**: "Oat milk Barista", not "the blue oat
milk carton from the fridge section".

## Reading the Report

- **Store ranking** counts only items present at 2+ stores (latest price per
  store). Small overlap (<5 items) = weak conclusion; log more receipts.
- **Price increases** are per (item, store) — switching stores doesn't create
  fake hikes. Threshold is 10% unit-price change.
- **Shrinkflation** requires: same unit, size −3% or more, price within −2%.
  This combination is almost never accidental.
- **Buy floors** are your historical lows per item+store; entries only appear
  when current price is ≥5% above the floor.

## Bulk-Buy Math

```
months_to_consume = package_size / monthly_usage
waste             = max(0, months_to_consume − shelf_life_months)
effective_unit    = price / (size × (1 − wasted_fraction))
```

A 15kg flour bag at $19.90 for a 2kg/month household = 7.5 months to consume.
Within a 12-month shelf life → fine. The same bag for a 0.5kg/month household
= 30 months → half expires; effective price doubles and the "deal" evaporates.

## Membership Breakeven

```
savings_per_trip = Σ (best_other_store_price − club_price) over overlapping items
trips_to_breakeven = ⌈ fee / savings_per_trip ⌉
```

If your overlapping basket shows the club cheaper by $12/trip, a $60 card
repays in 5 trips (~5 weeks at weekly cadence). If the club isn't actually
cheaper on YOUR items, no number of trips repays it.

## Seasonal Buying Notes

Historical US price cycles worth exploiting (verify with your own data):
- **Butter & baking staples**: floor in late Nov–Dec (holiday competition).
- **Turkey/ham**: rock-bottom in Nov (loss leaders), pre-Easter for ham.
- **Grill meats**: Memorial Day / July 4th week.
- **School snacks/lunch items**: August back-to-school promos.
- **Eggs**: post-Easter oversupply dip.

Your own `buy floors` data beats these generalizations — that's the point of
keeping the book.

## Privacy

All data lives in one local `pricebook.json` next to the script. No network
calls, no accounts, no receipts uploaded anywhere. Delete the file to reset.
