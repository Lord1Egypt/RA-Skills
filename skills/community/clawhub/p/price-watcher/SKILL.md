---
name: price-watcher
description: Monitor product URLs for price changes. Tracks a watchlist of products with baseline prices, fetches pages to extract current prices, and alerts on significant changes. Use when asked to: watch a price, track a price, set a price alert, check for a price drop, find a deal alert, or monitor a product price. Triggers on phrases like "price watch", "track price", "price alert", "price drop", "deal alert", "monitor price", "watch this product", or "let me know when it goes on sale".
---

# Price Watcher

Monitor product URLs for price changes via a local watchlist. No API keys required.

## Skill Location

```
~/.openclaw/workspace/skills/price-watcher/
```

All scripts use `SKILL_DIR` (parent of `scripts/`) to resolve `watchlist.json`.

## Core Workflow

### Add a product to watch

```bash
# Auto-fetch current price from page
python3 scripts/add_product.py "https://www.amazon.com/dp/BXXX"

# Explicit price + name (use when auto-fetch fails)
python3 scripts/add_product.py "https://..." 49.99 "Product Name"
```

### Check all prices

```bash
python3 scripts/check_prices.py
```

Outputs JSON to stdout. Updates `watchlist.json` with new prices and timestamps.

### Filter significant changes

```bash
python3 scripts/check_prices.py | python3 scripts/compare.py
python3 scripts/check_prices.py | python3 scripts/compare.py --threshold 10
```

Default threshold: 5%. Always surfaces fetch errors and no-price results.

### Format as markdown alert

```bash
python3 scripts/check_prices.py | python3 scripts/compare.py | python3 scripts/format_alert.py
```

Produces a markdown report with 📉 drops, 📈 increases, and ⚠️ errors.

## Watchlist Format

`watchlist.json` (in skill root) stores an array of objects:

```json
{
  "url": "https://...",
  "name": "Product Name",
  "baseline_price": 49.99,
  "last_price": 44.99,
  "last_checked": "2024-03-15T14:00:00+00:00",
  "price_history": [{"price": 49.99, "date": "..."}]
}
```

See `assets/watchlist.example.json` for a full example.

## Scheduling

For cron setup, threshold tuning, and anti-bot notes, see `references/setup-guide.md`.

## Error Handling

- `fetch_error`: Page couldn't be retrieved (503, timeout, network issue)
- `no_price`: Page loaded but no price found — check if site layout changed
- Both statuses surface in `compare.py` output and `format_alert.py` regardless of threshold
- `add_product.py` exits with an error if price can't be extracted and none was provided manually
