---
name: price-monitor
description: Monitor website prices, inventory, and content changes using browser automation. Use when tracking e-commerce prices, competitor monitoring, stock alerts, or any web content change detection. Supports scheduled checks, price history logging, and alert notifications.
---

# Price Monitor

## Overview

Automated price and content monitoring skill using agent-browser. Tracks price changes, stock availability, and content updates on any website with configurable alerts and history logging.

## Quick Start

```bash
# Monitor a product price
agent-browser open "https://example.com/product/123"
agent-browser snapshot -i
agent-browser get text @e1  # Get price element
```

## Core Workflows

### 1. Single Product Price Check

**Use case:** Check current price of a specific product

```bash
# Navigate to product page
agent-browser open "<product-url>"

# Get page snapshot to find price element
agent-browser snapshot -i

# Extract price (use appropriate ref from snapshot)
agent-browser get text @e1

# Optional: Save to history log
echo "$(date), $(price)" >> price-history.csv
```

### 2. Multi-Product Monitoring

**Use case:** Track prices across multiple products/competitors

Create a `products.csv` with URLs and price selectors:

```csv
url,selector,name
https://site-a.com/product1,.price-tag,Product A
https://site-b.com/item2,#price,Product B
```

Run monitoring script:

```bash
python scripts/monitor_prices.py products.csv
```

### 3. Stock/Inventory Alerts

**Use case:** Get notified when out-of-stock items become available

```bash
agent-browser open "<product-url>"
agent-browser snapshot -i
agent-browser get text @e1  # Check for "In Stock" or "Out of Stock"
```

### 4. Price History Tracking

**Use case:** Build historical price data for analysis

Script automatically logs:
- Timestamp
- Product name/URL
- Current price
- Stock status

Output: `price-history.csv` or JSON format

## Scripts

### monitor_prices.py

Main monitoring script that:
- Reads product list from CSV
- Navigates to each URL
- Extracts price using CSS selector
- Logs results with timestamp
- Detects price changes
- Optional: Send alerts on significant changes

**Usage:**
```bash
python scripts/monitor_prices.py products.csv [--alert-threshold 10]
```

**Arguments:**
- `products.csv` - Product list with URLs and selectors
- `--alert-threshold` - Percentage change to trigger alert (default: 10%)

## Configuration

### Product List Format (CSV)

```csv
url,selector,name,min_price,max_price
https://amazon.com/dp/B08N5WRWNW,.a-price-whole,Sony Headphones,50,150
https://bestbuy.com/site/12345,.priceView-hero-price,TV,200,500
```

### Alert Options

- **Email alerts** - Configure SMTP settings
- **Discord webhook** - Post to Discord channel
- **File logging** - Append to CSV/JSON
- **Console output** - Print changes to terminal

## Best Practices

1. **Rate limiting** - Add delays between requests (30s+ recommended)
2. **Error handling** - Handle page load failures gracefully
3. **Selector stability** - Use stable CSS selectors, avoid dynamic classes
4. **Headless mode** - Run browser in headless mode for automation
5. **Schedule wisely** - Check prices during business hours for accuracy

## Example: Daily Price Check Cron

```bash
# Run every day at 9 AM
0 9 * * * cd /path/to/skill && python scripts/monitor_prices.py products.csv
```

## Troubleshooting

- **Element not found**: Re-run snapshot to get updated refs
- **Price format issues**: Adjust selector or parse with regex
- **Page load timeout**: Increase timeout or add wait condition
- **Blocked by site**: Add delays, rotate user agents, or use residential proxy
