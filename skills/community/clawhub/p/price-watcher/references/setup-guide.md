# Price Watcher Setup Guide

## Quick Start

```bash
SKILL_DIR=~/.openclaw/workspace/skills/price-watcher
cd $SKILL_DIR

# Add a product (auto-fetches price)
python3 scripts/add_product.py "https://www.amazon.com/dp/BXXX"

# Add with explicit price and name
python3 scripts/add_product.py "https://www.amazon.com/dp/BXXX" 49.99 "My Widget"

# Check all prices now
python3 scripts/check_prices.py

# Full pipeline: check → filter 5%+ changes → format as markdown
python3 scripts/check_prices.py | python3 scripts/compare.py | python3 scripts/format_alert.py

# Custom threshold (10%)
python3 scripts/check_prices.py | python3 scripts/compare.py --threshold 10 | python3 scripts/format_alert.py
```

## File Locations

| File | Purpose |
|---|---|
| `watchlist.json` | Live data — all tracked products |
| `assets/watchlist.example.json` | Reference format only, not used by scripts |

The watchlist is created automatically by `add_product.py` in the skill root directory.

## Scheduling with Cron

Run price checks daily at 9am ET:

```cron
0 9 * * * cd /Users/openclaw/.openclaw/workspace/skills/price-watcher && \
  python3 scripts/check_prices.py | \
  python3 scripts/compare.py | \
  python3 scripts/format_alert.py >> /tmp/price-alerts.md 2>/tmp/price-watcher.log
```

Or to send results to Discord via curl (replace WEBHOOK_URL):

```cron
0 9 * * * cd /Users/openclaw/.openclaw/workspace/skills/price-watcher && \
  RESULT=$(python3 scripts/check_prices.py | python3 scripts/compare.py | python3 scripts/format_alert.py) && \
  [ -n "$RESULT" ] && curl -s -X POST "$DISCORD_WEBHOOK" \
    -H "Content-Type: application/json" \
    -d "{\"content\": \"\`\`\`\n$RESULT\n\`\`\`\"}"
```

## Supported Price Formats

The scripts detect these formats via regex:

- `$XX.XX` / `$X,XXX.XX` (USD dollar sign)
- `XX.XX USD` / `USD XX.XX`
- `£XX.XX` (GBP)
- `€XX.XX` / `EUR XX.XX` / `XX.XX EUR`
- Structured data: JSON-LD `"price"` fields, `<meta itemprop="price">`

## Anti-Bot Limitations

Some retailers (Amazon, Best Buy) use aggressive anti-bot measures:
- Pages may return 503/429 or a CAPTCHA HTML page
- Price will show as `null` / `no_price` status in output
- The scripts report these as errors rather than silently failing
- For heavily protected sites, consider using the manual price entry approach

## Watchlist JSON Schema

```json
{
  "url": "https://...",
  "name": "Product display name",
  "baseline_price": 49.99,
  "last_price": 44.99,
  "last_checked": "2024-03-15T14:00:00+00:00",
  "price_history": [
    {"price": 49.99, "date": "2024-03-01T10:00:00+00:00"},
    {"price": 44.99, "date": "2024-03-15T14:00:00+00:00"}
  ]
}
```

- `baseline_price`: The price when first added — used as long-term reference
- `last_price`: Most recent successfully extracted price — used for change calculations
- `price_history`: Capped at 90 entries (auto-trimmed by `check_prices.py`)

## Removing a Product

Edit `watchlist.json` directly and delete the entry for the product you want to remove.
