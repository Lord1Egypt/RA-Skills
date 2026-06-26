# Nex PriceWatch

**Competitive Price Monitor for SMEs and Agencies**

Track competitor and supplier pricing with automatic alerts, historical trends, and analytics. Monitor price changes across websites and get notified when competitors change their pricing strategy.

All pricing data stays locally on your machine.

## Features

- **Price Tracking**: Monitor any website price using CSS selectors, XPath, regex, or text patterns
- **Automatic Alerts**: Get notified when prices increase >5% or decrease >10%
- **Price History**: Complete historical data with timestamps and trend analysis
- **Competitor Comparison**: Side-by-side pricing comparison across competitors
- **Flexible Selectors**: CSS, XPath, Regex, and text label extraction methods
- **Export Options**: Export price history as JSON or CSV
- **Local Storage**: All data stored in SQLite database (~/.nex-pricewatch/)
- **Telegram Integration**: Optional real-time alerts via Telegram
- **No External Dependencies**: Uses Python stdlib only (urllib, sqlite3, json)

## Installation

### Quick Setup

```bash
# Navigate to skill directory
cd nex-pricewatch

# Run setup script
bash setup.sh
```

This will:
1. Check Python 3 installation
2. Create data directory (~/.nex-pricewatch/)
3. Initialize SQLite database
4. Make `nex-pricewatch` command available

### Manual Setup

```bash
# Create data directory
mkdir -p ~/.nex-pricewatch

# Initialize database
python3 -c "from lib.storage import init_db; init_db()"

# Run commands directly
python3 nex-pricewatch.py list
```

## Quick Start

### 1. Add a Price Target

Track a competitor's pricing page:

```bash
nex-pricewatch add \
  --name "WebAgency X Website Package" \
  --url "https://webagency-x.be/pricing" \
  --competitor "WebAgency X" \
  --selector ".pricing-tier:nth-child(2) .price" \
  --selector-type css \
  --currency EUR
```

### 2. Check Current Prices

```bash
# Check all targets
nex-pricewatch check --alerts

# Check specific target
nex-pricewatch check --name "WebAgency X Website Package"
```

### 3. View Dashboard

```bash
nex-pricewatch dashboard
```

### 4. Compare Competitor Pricing

```bash
nex-pricewatch compare
```

### 5. Price History Analysis

```bash
nex-pricewatch history "WebAgency X Website Package" --since 2026-01-01
nex-pricewatch stats
```

## Selector Types

### CSS Selectors

Most common method for modern websites:

```bash
# Class selector
nex-pricewatch add --selector ".price" --selector-type css

# ID selector
nex-pricewatch add --selector "#product-price" --selector-type css

# Complex selector
nex-pricewatch add --selector ".pricing-card:nth-child(2) .amount" --selector-type css
```

### XPath

For complex HTML structures:

```bash
nex-pricewatch add --selector "//div[@class='price']/span" --selector-type xpath
```

### Regex

Pattern matching for unstructured content:

```bash
# Euro amounts: €1.499,00
nex-pricewatch add --selector "€[\d.,]+" --selector-type regex

# Dollar amounts: $99.99
nex-pricewatch add --selector "\$[\d.,]+" --selector-type regex
```

### Text Labels

Find price near text labels:

```bash
# Find "Prijs: €1.499,00"
nex-pricewatch add --selector "Prijs" --selector-type text

# Find "Price: $99.99"
nex-pricewatch add --selector "Price" --selector-type text
```

## Commands Reference

### Adding & Managing Targets

```bash
# Add target
nex-pricewatch add --name "Name" --url "URL" --selector "selector" --selector-type css

# List all targets
nex-pricewatch list

# Show target details
nex-pricewatch show "Name"

# Remove target
nex-pricewatch remove "Name" --force
```

### Checking Prices

```bash
# Check all enabled targets
nex-pricewatch check

# Check with alerts
nex-pricewatch check --alerts

# Send alerts to Telegram
nex-pricewatch check --alerts --telegram

# Check specific target
nex-pricewatch check --name "Target Name"
```

### Analysis

```bash
# View price history
nex-pricewatch history "Name" --since 2026-01-01 --limit 50

# Recent price changes
nex-pricewatch changes --since 2026-01-01

# Compare competitor pricing
nex-pricewatch compare

# Full dashboard
nex-pricewatch dashboard

# Statistics
nex-pricewatch stats

# Configuration
nex-pricewatch config
```

### Export

```bash
# Export as JSON
nex-pricewatch export "Name"

# Export as CSV
nex-pricewatch export "Name" --format csv

# Save to file
nex-pricewatch export "Name" --output prices.json
```

## Price Extraction Examples

### Example 1: WebAgency Website Package

**Page HTML:**
```html
<div class="pricing-tier">
  <h3>Standard</h3>
  <span class="price-tag">€1.499,00</span>
</div>
```

**Command:**
```bash
nex-pricewatch add \
  --name "WebAgency X Standard" \
  --url "https://webagency-x.be/pricing" \
  --competitor "WebAgency X" \
  --selector ".price-tag" \
  --selector-type css
```

### Example 2: E-commerce Product

**Page HTML:**
```html
<div id="product-price">
  <span class="amount">$99.99</span>
</div>
```

**Command:**
```bash
nex-pricewatch add \
  --name "Product X Price" \
  --url "https://ecommerce.com/product/x" \
  --selector "#product-price .amount" \
  --selector-type css
```

### Example 3: Supplier Catalog

**Page HTML:**
```html
<tr>
  <td>Item Code: ABC123</td>
  <td>Unit Price: €12,50</td>
</tr>
```

**Command:**
```bash
nex-pricewatch add \
  --name "Supplier Item ABC123" \
  --url "https://supplier.com/catalog" \
  --type supplier \
  --selector "€[\d.,]+" \
  --selector-type regex
```

### Example 4: Text-based Pricing

**Page HTML:**
```html
Monthly subscription:
Prijs: €99/maand
```

**Command:**
```bash
nex-pricewatch add \
  --name "Monthly Subscription" \
  --url "https://service.com/pricing" \
  --selector "Prijs" \
  --selector-type text
```

## Alert Configuration

Alerts trigger automatically when:
- **Price increases >5%** → increase alert
- **Price decreases >10%** → decrease alert

Customize thresholds in `lib/config.py`:

```python
ALERT_INCREASE_PCT = 5      # Alert when price goes up >5%
ALERT_DECREASE_PCT = 10     # Alert when price goes down >10%
```

## Telegram Notifications

### Setup

1. Create a Telegram bot via @BotFather:
   - Message: `/newbot`
   - Follow prompts to get bot token

2. Get your chat ID:
   - Message bot: `/start`
   - Get ID from https://api.telegram.org/bot<TOKEN>/getUpdates

3. Set environment variables:

```bash
export NEX_PRICEWATCH_TELEGRAM_BOT_TOKEN="your_bot_token"
export NEX_PRICEWATCH_TELEGRAM_CHAT_ID="your_chat_id"
```

4. Add to shell profile (~/.bashrc or ~/.zshrc):

```bash
echo 'export NEX_PRICEWATCH_TELEGRAM_BOT_TOKEN="token"' >> ~/.bashrc
echo 'export NEX_PRICEWATCH_TELEGRAM_CHAT_ID="id"' >> ~/.bashrc
```

5. Enable in config (`lib/config.py`):

```python
TELEGRAM_ENABLED = True
```

6. Use in commands:

```bash
nex-pricewatch check --alerts --telegram
```

## Data Storage

All data stored locally in `~/.nex-pricewatch/`:

```
~/.nex-pricewatch/
├── pricewatch.db          # SQLite database
├── snapshots/             # HTML snapshots for comparison
│   └── target_1_abc123.html
│   └── target_2_def456.html
└── ...
```

**Database tables:**
- `targets` - Monitored price targets
- `price_history` - Historical price data with timestamps
- `alerts` - Price change alerts
- Indexes on target_id and timestamps for fast queries

## Currency Support

Supported currency codes and symbols:

| Code | Symbol | Code | Symbol |
|------|--------|------|--------|
| EUR  | €      | GBP  | £      |
| USD  | $      | JPY  | ¥      |
| CNY  | ¥      | INR  | ₹      |
| RUB  | ₽      | TRY  | ₺      |
| ILS  | ₪      | BRL  | R$     |
| AUD  | A$     | CAD  | C$     |

Specify currency with `--currency` flag or detect automatically.

## Troubleshooting

### Price Not Extracting

1. **Verify URL**: Is page accessible and correct?
2. **Inspect HTML**: Right-click → Inspect → Find selector
3. **Test selector**: Try CSS first, then regex if failing
4. **Check format**: Ensure price is visible in HTML (not JavaScript-rendered)

### "No match found for selector"

- Page structure may have changed
- Try right-clicking → Inspect to find current selector
- Use regex: `€[\d.,]+` for more flexible matching
- Check if site blocks web scraping

### Price parsing failed

- Currency symbol not recognized? Specify `--currency EUR`
- Try regex selector: `\d+[\.,]\d{2}` for generic numbers
- Check if raw price text includes unwanted characters

### JavaScript-Heavy Sites

Sites that load prices via JavaScript may fail. Options:

1. **Use regex**: If content visible in source, use regex selector
2. **Playwright**: Install optional dependency:
   ```bash
   pip install playwright
   python3 -m playwright install chromium
   ```
3. **Find API**: Some sites load prices via JSON API (use regex on JSON)

### Database Locked

If getting "database is locked" error:

```bash
# Remove database and reinitialize
rm ~/.nex-pricewatch/pricewatch.db
python3 -c "from lib.storage import init_db; init_db()"
```

## Performance Tips

1. **Set appropriate check intervals**: Use `--interval 48` for less-frequent checks
2. **Limit price history**: Database grows with each check
3. **Export & archive**: Export old data to CSV and clean up
4. **Use selective checks**: Check specific targets instead of all

```bash
# Archive old data
nex-pricewatch export "Name" --format csv --output backup.csv

# Check only important targets
nex-pricewatch check --name "Critical Competitor"
```

## Security & Privacy

- All data stored locally (no cloud sync)
- Uses standard HTTP with proper User-Agent headers
- Optional Telegram integration is encrypted HTTPS
- No personal data collected
- HTML snapshots stored for visual comparison only

## Architecture

- **lib/config.py** - Configuration and constants
- **lib/storage.py** - SQLite database operations
- **lib/scraper.py** - HTTP fetching and price extraction
- **lib/alerter.py** - Price change detection and notifications
- **nex-pricewatch.py** - CLI interface and commands

## Development

### Testing a Selector

```bash
python3 -c "
from lib.scraper import scrape_price
result = scrape_price(
    'https://example.com',
    'css',
    '.price'
)
print(f\"Price: {result['price']} {result['currency']}\")
print(f\"Raw: {result['raw_text']}\")
"
```

### Debugging

Enable verbose output:

```bash
python3 nex-pricewatch.py check -vv
```

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Free to use, modify, and distribute. No restrictions.

## Support

- Website: https://nex-ai.be
- Issues: Report bugs and suggestions
- Community: Built for SMEs and agencies

---

**Version 1.0.0** • Built by Nex AI • Updated 2026-04-05
