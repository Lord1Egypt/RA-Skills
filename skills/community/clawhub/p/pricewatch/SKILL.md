# PriceWatch - Cross-Platform Competitive Price Monitor

**Version:** 1.0.0
**Author:** SMTM Skill Smith
**Category:** E-commerce / Data & API
**Tags:** price-monitoring, ecommerce, competitor-analysis, scraping, alerts

## Overview

PriceWatch is an AI-powered cross-platform price monitoring skill for OpenClaw agents. It automatically tracks competitor pricing across Amazon, Walmart, Shopify stores, and Etsy, detects price changes, normalizes prices across currencies and regions, and sends intelligent alerts via Slack, Telegram, Email, or webhook.

**Why PriceWatch?**
- Existing price tools focus on single platforms (mostly Amazon or Chinese marketplaces)
- No cross-platform price normalization exists in the OpenClaw ecosystem
- Businesses waste $300-500/month on fragmented SaaS tools — PriceWatch replaces them with pay-per-use at ~$50/month

## Features

### Core Capabilities
- **Multi-Platform Monitoring** — Track products across Amazon, Walmart, Shopify, Etsy simultaneously
- **Smart Price Normalization** — Handles different currencies, tax regimes, shipping costs automatically
- **Historical Price Tracking** — Built-in SQLite database stores price history for trend analysis
- **Intelligent Alerts** — Configurable thresholds, cooldown deduplication, and AI-contextualized notifications
- **Scheduled Scanning** — Set scan intervals from 10 minutes to daily
- **Batch Import** — Upload product URLs via CSV or direct input (up to 500 products per watchlist)

### AI-Powered Analysis
- Price drop detection with "So What?" contextual impact analysis
- Competitor behavior pattern recognition (frequency, magnitude, seasonality)
- Automatic price trend summaries with buy/hold/wait recommendations
- Market position reports — how your pricing compares to top 10 competitors

### Notification Channels
| Channel | Setup Required | Format |
|---------|---------------|--------|
| Slack Webhook | Incoming Webhook URL | Rich card with price chart |
| Telegram Bot | Bot Token + Chat ID | Formatted message + chart |
| Email (SMTP) | SMTP credentials | HTML email with table |
| Custom Webhook | Any HTTP endpoint | JSON payload |

## Installation

```bash
# Via ClawHub CLI
npx clawhub@latest install smtm-pricewatch

# Or manual install
git clone https://github.com/smtm-skills/pricewatch.git
cd pricewatch
cp scripts/config.example.yaml scripts/config.yaml
# Edit config.yaml with your settings
```

## Quick Start

```yaml
# config.yaml
watchlist:
  - name: "Competitor Running Shoes"
    platform: amazon
    url: "https://www.amazon.com/dp/B08EXAMPLE"
    target_price: 89.99
    currency: USD
  - name: "Competitor Yoga Mat"
    platform: walmart
    url: "https://www.walmart.com/ip/EXAMPLE123"
    target_price: 29.99
    currency: USD

alerts:
  slack_webhook: "https://hooks.slack.com/services/xxx"
  cooldown_minutes: 30
  threshold_percent: 5.0

schedule:
  interval_minutes: 60
```

```bash
# Run a scan
npx clawhub run smtm-pricewatch --scan

# Add a product to watchlist
npx clawhub run smtm-pricewatch --add --url "https://shopify.com/product/xyz" --target 49.99

# View price history
npx clawhub run smtm-pricewatch --history --product "Competitor Running Shoes"

# Generate market report
npx clawhub run smtm-pricewatch --report
```

## Skill Interface

### Input Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | Yes | `scan`, `add`, `history`, `report`, `export` |
| `url` | string | For `add` | Product URL to monitor |
| `target_price` | number | For `add` | Alert threshold price |
| `platform` | string | For `add` | `amazon`, `walmart`, `shopify`, `etsy` |
| `product_name` | string | For `history` | Name of product to look up |

### Output / Return Data
```json
{
  "status": "success",
  "scan_id": "scan_20260616_001",
  "products_scanned": 15,
  "alerts_triggered": 2,
  "alerts": [
    {
      "product": "Competitor Running Shoes",
      "platform": "amazon",
      "old_price": 95.00,
      "new_price": 85.00,
      "change_percent": -10.53,
      "currency": "USD",
      "detected_at": "2026-06-16T10:30:00Z",
      "recommendation": "Strong buy signal — price at lowest point in 30 days"
    }
  ],
  "next_scheduled_scan": "2026-06-16T11:30:00Z"
}
```

## Dependencies

- Python 3.9+ (for the scraping engine)
- SQLite3 (included in Python stdlib)
- `requests` library (for webhooks and API calls)
- `beautifulsoup4` (for HTML parsing when needed)
- OpenClaw Agent (any version with skill support)

## Files Structure

```
smtm-pricewatch/
├── SKILL.md              # This file — skill definition
├── skill-card.md         # ClawHub marketplace listing
├── scripts/
│   ├── price_watch.py    # Core monitoring engine
│   ├── config.yaml       # User configuration (generated from example)
│   ├── config.example.yaml  # Configuration template
│   └── platforms/
│       ├── amazon.py     # Amazon scraper adapter
│       ├── walmart.py    # Walmart scraper adapter
│       ├── shopify.py    # Shopify scraper adapter
│       └── etsy.py       # Etsy scraper adapter
└── data/
    └── price_history.db  # SQLite database (auto-created)
```

## Security & Privacy

- All data stored locally in SQLite — no external database required
- No API keys sent to third parties (except user-configured webhooks)
- Configurable user-agent rotation and rate limiting
- Open source — fully auditable

## Roadmap

| Version | Feature | Status |
|---------|---------|--------|
| 1.0 | Core multi-platform monitoring, price normalization, Slack/Telegram alerts | MVP |
| 1.1 | Historical trends chart, batch CSV import | Planned |
| 1.5 | eBay, AliExpress support; dynamic repricing suggestions | Planned |
| 2.0 | AI-powered competitive intelligence reports, market share analysis | Future |

## Support

- GitHub Issues: https://github.com/smtm-skills/pricewatch/issues
- Documentation: https://smtm-skills.github.io/pricewatch/docs
- Discord: SMTM Skill Smith community (link in skill-card.md)
