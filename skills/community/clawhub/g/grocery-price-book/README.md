# Grocery Price Book

**Know the real price of everything you buy — and which store actually deserves your money.**

Grocery inflation didn't hit everything equally — it hit *your* 30 items, unevenly,
quietly. The cereal box shrank from 500g to 440g at the same price. Your store
raised olive oil 26% while advertising "everyday low prices." The bulk club
charges more per liter on the oat milk you actually buy.

The old-school fix is a **price book** — the notebook frugal households kept for
generations, recording what each item costs where, per unit, over time. It works.
It's also why nobody does it: manual tracking is tedious.

This skill is the price book, automated:

- **Receipt import** — paste a receipt text file, get parsed item lines with
  sizes pulled from item names (`FLOUR AP 2.5KG` → 2.5kg)
- **Unit-price engine** — `500g`, `1lb`, `6x1L`, `24x330ml`, `12ct` all
  normalize to comparable price-per-100g/ml/count (11/11 parse tests pass)
- **Store ranking by YOUR basket** — not marketing averages; only items you've
  priced at 2+ stores count
- **Price-increase detector** — per item, per store, with both observations
  quoted (`$0.62 → $0.78/100ml, +26%`)
- **Shrinkflation detector** — package down ≥3%, price same/up → flagged with
  the silent unit-price jump
- **Bulk-buy math** — consumption rate vs shelf life vs package size, with
  waste-adjusted effective price
- **Membership breakeven** — is the $60/yr club card repaid by what YOU save?

100% offline, pure Python stdlib, data in one local JSON file.

## Quick Start

```bash
# Log a purchase
python3 scripts/price_book.py add --store lidl --item "Oat milk" --size 1L --price 1.29

# Import a whole receipt
python3 scripts/price_book.py import --store kroger references/receipt-example.txt

# At the shelf right now: which size is actually cheaper?
python3 scripts/price_book.py unit --opts "2L@3.49" "6x1L@7.49" "1L@1.29"

# Full report after 2-3 weeks of entries
python3 scripts/price_book.py report

# Should I buy the 15kg bag?
python3 scripts/price_book.py bulk --size 15kg --price 19.90 --use 2kg/month --shelf 12months

# Does the club membership pay off?
python3 scripts/price_book.py membership --store costco --fee 60
```

## Example Report

```
STORE RANKING by overlapping-basket cost:
  1. lidl      $7.27   (3 common items)
  2. kroger    $7.77   (3 common items)
  3. costco   $16.48   (2 common items; membership not counted)

PRICE INCREASES (>10% unit-price jump):
  Butter @ lidl: $1.00 → $1.28 /100g  +28.1%  (Jun → Sep)

SHRINKFLATION SUSPECTS:
  CEREAL O'S @ kroger: 500g → 440g at $4.99 → unit price +13.6% silently
```

That shrinkflation line is the "aha" every user gets within a month of logging.

## Who Needs This

Anyone who buys groceries — which is everyone — but especially: households
trying to cut spending without cutting quality, bulk-store members unsure the
fee pays off, and anyone who's stood in an aisle wondering if the bigger box
is actually cheaper (it often isn't).

## License

MIT — see [LICENSE](LICENSE).
