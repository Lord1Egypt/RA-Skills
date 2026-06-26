---
name: nex-pricewatch
description: Competitive price monitoring and alert system for tracking competitor and supplier pricing across websites. Monitor pricing pages from competitors (concurrenten) using CSS selectors, XPath, or regex patterns to extract prices from dynamic and static websites. Automatically detect when competitors change their pricing (prijs wijzigen) and receive alerts when prices increase or decrease significantly. Configure custom alert thresholds for price movements (default: 5% increases, 10% decreases). View complete price history with timestamps, identify pricing trends (UP, DOWN, STABLE), and compare price changes over time. Track multiple pricing targets per competitor to monitor different product tiers, packages, or bundles. Optional Telegram notifications alert you immediately when prices change. Export price history data in CSV or JSON formats for competitive analysis, pricing strategy reviews, and business decision-making. Perfect for Belgian agencies, resellers, and business owners who need to monitor competitor pricing, adjust their own rates competitively, and stay informed about market changes. All price tracking data remains local and private.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      bins:
        - python3
      env:
        - NEX_PRICEWATCH_TELEGRAM_BOT_TOKEN
        - NEX_PRICEWATCH_TELEGRAM_CHAT_ID
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-pricewatch.py"
      - "lib/*"
      - "setup.sh"
---

# Nex PriceWatch

Competitive Price Monitor for SMEs and Agencies. Track competitor and supplier pricing with automatic alerts, historical data, and analytics. All pricing data stays on your machine.

## When to Use

Use this skill when the user asks about:

- Tracking competitor pricing pages
- Monitoring supplier cost changes
- Setting up price alerts for competitors
- Comparing your pricing against competitors
- Historical price analysis and trends
- Detecting when competitors change their pricing
- Exporting price history for analysis
- Price monitoring dashboard

Trigger phrases: "price", "pricing", "competitor", "concurrentie" (Dutch), "prijs", "tarief", "goedkoper", "duurder", "monitor", "track competitor", "price alert", "price change", "pricing comparison", "have competitors changed their prices"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory and initializes the SQLite database.

## Available Commands

### 1. Add a Price Target

Add a website to monitor:

```bash
nex-pricewatch add \
  --name "Competitor X Website Package" \
  --url "https://competitor.be/pricing" \
  --competitor "WebAgency X" \
  --selector ".price-premium" \
  --selector-type css \
  --type competitor \
  --currency EUR
```

**Parameters:**
- `--name` (required): Descriptive target name
- `--url` (required): Full URL to monitor
- `--competitor`: Competitor/company name
- `--selector-type` (required): `css`, `xpath`, `regex`, or `text`
- `--selector` (required): CSS class (`.price`), ID (`#price`), regex pattern, or text label
- `--type`: `competitor`, `supplier`, or `market` (default: competitor)
- `--currency`: Currency code (EUR, USD, etc.)
- `--interval`: Check interval in hours (default: 24)
- `--tags`: Comma-separated tags
- `--notes`: Additional notes

**Selector Examples:**
- CSS class: `.price-tag` → finds element with class "price-tag"
- CSS ID: `#pricing` → finds element with id "pricing"
- Regex: `\€[\d.,]+` → finds currency amounts
- Text label: `Prijs` → finds price near text label

### 2. Check Prices Now

```bash
nex-pricewatch check
nex-pricewatch check --name "Competitor X Website Package"
nex-pricewatch check --alerts
nex-pricewatch check --alerts --telegram
```

Check current prices for all or specific targets. Shows success/failure and any price changes.

### 3. List Targets

```bash
nex-pricewatch list
```

Shows all configured targets with current prices and status.

### 4. Show Target Details

```bash
nex-pricewatch show "Competitor X Website Package"
```

Display detailed information including:
- Target configuration
- Current and previous prices
- Recent price history
- Price statistics (min, max, avg, trend)

### 5. Price History

```bash
nex-pricewatch history "Competitor X Website Package"
nex-pricewatch history "Competitor X Website Package" --since 2026-01-01
nex-pricewatch history "Competitor X Website Package" --limit 20
```

View complete price history with timestamps and raw extracted text.

### 6. Recent Changes

```bash
nex-pricewatch changes
nex-pricewatch changes --since 2026-01-01
```

Show all detected price changes with percentages and dates.

### 7. Compare Pricing

```bash
nex-pricewatch compare
```

Side-by-side view of all competitor pricing organized by company.

### 8. Dashboard View

```bash
nex-pricewatch dashboard
```

Full monitoring dashboard with all tracked prices, trends, and status.

### 9. Remove Target

```bash
nex-pricewatch remove "Competitor X Website Package"
nex-pricewatch remove "Competitor X Website Package" --force
```

Remove a price target and its history.

### 10. Export History

```bash
nex-pricewatch export "Competitor X Website Package"
nex-pricewatch export "Competitor X Website Package" --format csv
nex-pricewatch export "Competitor X Website Package" --output prices.json
```

Export price history as JSON or CSV for external analysis.

### 11. Statistics

```bash
nex-pricewatch stats
```

Overall statistics including:
- Total targets configured
- Number of price changes (30 days)
- Biggest price increase
- Biggest price decrease

### 12. Configuration

```bash
nex-pricewatch config
```

Display current configuration settings.

## Alert Configuration

Alerts are automatically generated when:
- Price increases by more than **5%**
- Price decreases by more than **10%**

Adjust these thresholds in `lib/config.py`:
```python
ALERT_INCREASE_PCT = 5
ALERT_DECREASE_PCT = 10
```

## Telegram Notifications (Optional)

To enable Telegram alerts:

1. Create a Telegram bot via @BotFather
2. Set environment variables:
   ```bash
   export NEX_PRICEWATCH_TELEGRAM_BOT_TOKEN="your_bot_token"
   export NEX_PRICEWATCH_TELEGRAM_CHAT_ID="your_chat_id"
   ```
3. Enable in config: `TELEGRAM_ENABLED = True`

## Data Storage

All price data is stored locally at `~/.nex-pricewatch/`:
- `pricewatch.db` - SQLite database with all targets, prices, and alerts
- `snapshots/` - HTML snapshots for comparison

## Supported Selectors

### CSS Selectors
Simple CSS selector matching:
- `.price` - class selector
- `#price` - ID selector
- `span.amount` - tag with class
- Works with common price page structures

### XPath
Basic XPath support:
- `//div[@class='price']/span`
- `//span[@id='price']`

### Regex
Full regex pattern matching:
- `\€[\d.,]+` - Euro amounts
- `\$\d{2,4}(\.\d{2})?` - Dollar amounts
- `\d+\s*(?:euro|EUR)` - Numbers followed by currency

### Text Labels
Find price near text labels:
- `Prijs` - finds "Prijs: €1.499,00"
- `Price` - finds "Price: $99.99"
- `Tarif` - finds "Tarif: 1999 EUR"

## Interpreting Results

Price changes show:
- **⬆️ +X%**: Price increased
- **⬇️ -X%**: Price decreased
- **🔔**: New price tracking started

Trends indicate direction:
- **UP**: Recent prices higher than historical average
- **DOWN**: Recent prices lower than historical average
- **STABLE**: Consistent pricing

## Examples

### Track WebAgency Competitor Pricing

```bash
nex-pricewatch add \
  --name "WebAgency X Standard Package" \
  --url "https://webagency-x.be/pricing" \
  --competitor "WebAgency X" \
  --selector ".pricing-card:nth-child(2) .price" \
  --selector-type css

nex-pricewatch check --alerts
```

### Monitor Supplier Material Costs

```bash
nex-pricewatch add \
  --name "Steel supplier A - 10mm plate" \
  --url "https://supplier-a.com/catalog/steel" \
  --type supplier \
  --selector "table.prices tr:contains('10mm') .price" \
  --selector-type css

nex-pricewatch history "Steel supplier A - 10mm plate" --since 2025-12-01
```

### Market Rate Tracking

```bash
nex-pricewatch add \
  --name "EURIBOR 12M Rate" \
  --url "https://www.euribor-rates.eu/" \
  --type market \
  --selector ".euribor-12m-rate" \
  --selector-type css

nex-pricewatch dashboard
```

### Export for Analysis

```bash
nex-pricewatch export "WebAgency X Standard Package" --format csv --output ~/analysis.csv
```

## Troubleshooting

### Price Not Extracting

1. **Check URL**: Ensure the URL is correct and accessible
2. **Inspect page**: Right-click → Inspect to find correct selector
3. **Test selector**: Try different selector types (css, xpath, regex)
4. **Use regex**: If static selectors fail, use regex: `\€[\d.,]+`

### JavaScript-Heavy Sites

If the site loads prices with JavaScript:
1. Try regex selector: `\€[\d.,]+`
2. Or provide the actual HTML view source selector
3. Advanced: Use playwright (optional dependency) for dynamic sites

### Currency Parsing Issues

If currency not detected:
1. Specify explicit `--currency` code
2. Ensure price format includes currency symbol or code
3. Supported: EUR, USD, GBP, JPY, CNY, INR, etc.

## Privacy & Security

- All data stored locally in `~/.nex-pricewatch/`
- No data sent to external services (except optional Telegram)
- Uses standard HTTP with proper user-agent
- Snapshots stored for comparison purposes only

## Technical Details

- **Database**: SQLite (lib/storage.py)
- **Scraper**: Python urllib + regex (lib/scraper.py)
- **Alerts**: Threshold-based detection (lib/alerter.py)
- **No external dependencies**: Uses Python stdlib only
- **Optional**: Playwright for JavaScript-heavy sites

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
