---
name: grocery-price-book
description: "Use when grocery bills keep creeping up, when you want to know which store actually has the best prices on what YOU buy, or when deciding whether a bulk-club membership pays off — builds a personal price book from receipts (manual entry or receipt-file parsing), computes unit prices across package sizes and stores, tracks price history per item to expose shrinkflation and stealth increases, ranks stores by your-basket cost instead of generic averages, and answers bulk-buy and stock-up questions with real math (cost per serving, shelf-life breakeven, membership breakeven)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [groceries, price-tracking, unit-price, shrinkflation, budgeting, household]
---

# Grocery Price Book

## Overview

Grocery prices rose sharply in recent years and never came back down — but the increases are deliberately uneven. The cereal box quietly shrinks from 500g to 440g at the same price. Your usual store raises the price of the 12 items you actually buy while advertising "everyday low prices." A bulk club looks cheap but 30% of what you buy there is more expensive per unit than the supermarket across the street.

The old-school fix is a **price book**: a small notebook where frugal households recorded what each item costs at each store, per unit, over time. It's proven (it's how our grandparents shopped) but nobody maintains it because manual tracking is tedious.

This skill modernizes it:

1. **Log purchases** — one line per item from a receipt: store, date, item, size, price. Or import a whole receipt file and confirm the parse.
2. **Unit-price engine** — normalizes everything to price-per-100g / per-liter / per-count, with a unit-guessing heuristic (metric and US customary), so a 440g box and a 1kg bag become comparable.
3. **Store ranking by YOUR basket** — ranks stores by the total cost of the items you actually buy there, not by average savings claims.
4. **Price history & shrinkflation detector** — flags items whose unit price jumped >10% since you started tracking, and items whose package size shrank while price held.
5. **Bulk-buy advisor** — answers "should I buy the 15kg bag?" with shelf-life breakeven math: how much do you consume per month, when does it expire, what's the actual savings per month of shelf life.
6. **Membership breakeven** — is the $60/year club card worth it given what you'd actually save?

All data stays in a local JSON file. Pure stdlib. No accounts, no receipts uploaded anywhere.

## When to Use

- **"Why is my grocery bill higher every month?"** — find the specific items driving it, with numbers.
- **Choosing where to shop** — rank stores by the cost of YOUR top items, not marketing.
- **At the shelf, deciding between sizes** — `unit` command: instant price-per-unit comparison of 2-3 options.
- **Suspecting shrinkflation** — "didn't this box used to be bigger?" — history proves or disproves it.
- **Bulk-club decision** — "will the membership pay for itself?"
- **Stock-up decisions** — "turkey is $0.99/lb this week; how much should I freeze?"
- Don't use for: restaurant spending, non-grocery retail (different seasonality), or as a full budgeting system — it's a price-intelligence tool, not an expense tracker (use receipt-raccoon-style skills for full spend categorization).

## How It Works

1. **Add entries** — `add --store costco --date 2026-09-18 --item "Flour AP" --qty 10 --size 10kg --price 8.99`. Size parsing understands `500g`, `2L`, `12ct`, `1lb`, `24x330ml`, and combinations.
2. **Build history** — each entry appends to `pricebook.json`; multiple entries of the same item (fuzzy name match) form a time series per store.
3. **Analyze**:
   - `report` — basket cost per store (items common to compared stores), unit-price table, top shrinkflation suspects.
   - `unit A B C` — quick shelf-side comparison of specific options.
   - `bulk` — consumption rate (from your own history or stated) vs shelf life vs size.
   - `membership` — observed savings rate on overlapping items vs annual fee.
4. **Act** — switch stores for specific items, time stock-ups around your own historical price floors, and drop the bulk membership if the math says so.

## Commands

```bash
# Log an item (size optional but needed for unit prices)
python3 scripts/price_book.py add --store lidl --item "Oat milk" --size 1L --price 1.29
python3 scripts/price_book.py add --store costco --item "Oat milk" --size 6x1L --price 7.49 --date 2026-09-10

# Import a whole receipt (see references/receipt-example.txt for format)
python3 scripts/price_book.py import --store kroger references/receipt-example.txt

# Compare options at the shelf right now
python3 scripts/price_book.py unit --opts "2L@3.49" "6x1L@7.49" "1L@1.29"

# Full report: store ranking by your basket, unit-price table, inflation flags
python3 scripts/price_book.py report

# Shrinkflation suspects only
python3 scripts/price_book.py report | grep -A3 SHRINK   # or read the JSON via --json

# Bulk-buy math: consume 2kg/month, shelf life 12 months, 15kg bag at $19.90?
python3 scripts/price_book.py bulk --size 15kg --price 19.90 --use 2kg/month --shelf 12months

# Is the $60/yr membership worth it? (compares overlapping items in your book)
python3 scripts/price_book.py membership --store costco --fee 60
```

## Example Session

```
$ python3 scripts/price_book.py report

=== PRICE BOOK: 23 items, 3 stores, 61 entries ===

STORE RANKING by overlapping-basket cost (lower = better):
  1. lidl      $42.10   (11 common items)
  2. costco    $44.85   (9 common items; membership not counted)
  3. kroger    $49.30   (11 common items)
  → Buying the common basket at lidl instead of kroger saves ~$7.20/trip
    (~$374/yr at weekly trips)

UNIT-PRICE TABLE (best deal per item flagged):
  Item            Size      Store   Price   Unit
  Flour AP        10kg      costco  $8.99   $0.090/100g ★
  Flour AP        2.5kg     lidl    $3.29   $0.132/100g
  Oat milk        6x1L      costco  $7.49   $1.25/L     ★
  Oat milk        1L        lidl    $1.29   $1.29/L

PRICE INCREASES (>10% unit-price jump, tracked items):
  Olive oil EVOO @ kroger: $0.62/100ml (Aug) → $0.78/100ml (Sep)  +26%
  → Consider: switch store, stock up if shelf-stable, or substitute.

SHRINKFLATION SUSPECTS (size down, price same/up):
  Cereal O's @ kroger: 500g → 440g at $4.99  → unit price +13.6% silently

BULK/STOCK-UP FLOORS (your historical lows — buy when at/below):
  Butter: $2.49 (lidl, Jun) — current best $3.19 → wait
  Turkey (seasonal): $1.10/lb (Nov) vs $2.89/lb now → Nov stock-up
```

## Workflow for an Agent

1. Ask for the latest receipt (photo → OCR, or text paste). Confirm item lines before importing.
2. `add` or `import` entries; flag any line where size or price parsing looks wrong — never silently guess wrong units.
3. After ~2-3 weeks of entries, run `report`; present store ranking and top 5 opportunities with dollar impact per month.
4. Watch price-increase and shrinkflation sections — these are the "aha" outputs users care about most.
5. For bulk/membership questions use `bulk` and `membership` with the user's real consumption numbers, not defaults.

## Common Pitfalls

1. **Comparing items with wrong units.** `500g` vs `1lb` vs `12ct` only compare if the unit guess is right. Always show the interpreted unit (`g`, `ml`, `ct`) in output; correct it with `--size` on the next entry if wrong.
2. **Name drift.** "Milk 2%" and "milk 2% carton" become two items. Keep names short and consistent (store brand + type + variant); the fuzzy matcher helps but isn't clairvoyant.
3. **Judging stores on one trip.** Sales distort single trips; require ≥2 dates per store before quoting savings.
4. **Forgetting membership fees.** Costco's basket price means nothing until the fee is amortized — always run `membership` too.
5. **Bulk-buying perishables.** The bulk math must include shelf life; a 15kg bag of flour for a 1kg/month household is mouse food, not savings.
6. **Treating the price book as a budget.** It tracks PRICES, not spending totals. Different tool.

## Verification Checklist

- [ ] Entries have store + date + item + price (+ size for unit math)
- [ ] Unit interpretation shown for every compared item (and corrected where wrong)
- [ ] Store ranking only quotes items present at both stores
- [ ] Shrinkflation/increase claims cite both observations (old and new)
- [ ] Bulk advice includes consumption rate, shelf life, and monthly savings
- [ ] Membership verdict states observed savings vs fee, with item count basis
