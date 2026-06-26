# insider-trade-tracker

> Monitor SEC Form 4 insider buying and selling for any US-listed company, detect cluster buy/sell signals, and assess insider conviction — all via free-tier [Finskills API](https://finskills.net) SEC endpoints.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Free-brightgreen.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-alternative--data-yellow.svg)]()

---

## What This Skill Does

1. Fetches SEC Form 4 insider transactions for any ticker (last 90 days)
2. Filters to open-market purchases/sales (excludes option exercises and gifts)
3. Weights signals by insider role (CEO/CFO = highest conviction)
4. Detects **Cluster Buy** (3+ insiders buying in 30 days) and **Cluster Sell** signals
5. Calculates net insider sentiment score and price context (stock vs. purchase price)
6. Outputs structured verdict: Strong Buy / Mild Buy / Neutral / Caution

**All endpoints used are free tier — no Pro plan required.**

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/insider-trade-tracker):

1. Visit **[https://clawhub.ai/finskills/insider-trade-tracker](https://clawhub.ai/finskills/insider-trade-tracker)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: Is management buying AAPL stock?
Claude: [Fetches Form 4 data, filters to open-market trades, scores by role, outputs report]
```

## Example Triggers

- `"Are insiders buying NVDA?"`
- `"Show me insider trades for META in the last 3 months"`
- `"Is there any cluster insider buying in the healthcare sector?"`
- `"What does recent insider selling at Tesla mean?"`
- `"Check insider activity for my watchlist: AAPL, MSFT, AMZN"`

## Signal Framework

| Signal | Condition |
|--------|-----------|
| ⭐⭐⭐ Cluster Buy | 3+ insiders buying in 30 days, incl. C-suite |
| ⭐⭐⭐ CEO/CFO Buy | Chief executive open-market purchase > $500K |
| ⚠️ Cluster Sell | 3+ insiders selling > 20% of holdings in 30 days |
| 🚨 Exec Mass Sell | CEO/CFO selling > 50% of holdings |

## API Endpoints Used (All Free)

| Endpoint | Data |
|----------|------|
| `GET /v1/free/sec/insider-trades/{symbol}` | Form 4 transaction history |
| `GET /v1/free/sec/filings/{cik}` | 10-K/10-Q/8-K context |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **free plan is sufficient**
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
