---
name: polymarket-news-events
description: >
  Monitors 20+ premium RSS feeds for breaking news and matches stories to Polymarket
  markets via keyword analysis. Trades when breaking news creates an estimated price
  impact exceeding 12%. Uses fast accept/reject pre-filtering before deeper analysis.
metadata:
  author: "Mibayy"
  version: "2.0.3"
  displayName: "Breaking News Event Trader"
  type: "automaton"
  difficulty: "intermediate"
---

# Breaking News Event Trader

Comprehensive breaking news monitor that trades Polymarket markets on high-impact events.

## What It Does

Continuously polls 20+ premium news RSS feeds, pre-filters stories with fast keyword
matching, then matches relevant stories to active Polymarket markets. When a breaking
story has estimated price impact >12%, generates a trade signal.

## News Sources

| Category | Sources |
|----------|---------|
| **Wire Services** | Reuters, AP |
| **Broadcast** | BBC, CNBC |
| **Financial** | Bloomberg, FT, MarketWatch, WSJ |
| **Politics** | Politico, Axios, The Hill |
| **Crypto** | CoinDesk, CoinTelegraph |
| **Tech** | TechCrunch |

## Pre-Filter System

Two-stage filtering for speed:

1. **Fast reject** — Skip stories with common noise keywords (opinion, podcast, review)
2. **Fast accept** — Prioritize stories with high-signal keywords (breaking, passes,
   signs, ruling, indicted, default, crash, surge)

Only stories passing pre-filter get matched against Polymarket markets.

## Impact Estimation

Stories are scored on:
- Source credibility tier (wire services > financial > blogs)
- Keyword signal strength
- Headline match quality to market question
- Recency (exponential decay over 30 minutes)

## Requirements

**pip dependencies:** `simmer-sdk`, `requests`, `feedparser`

**Environment variables:**
- `SIMMER_API_KEY` (required) - get from simmer.markets/dashboard

> ⚠️ **Automated trading.** Dry-run is the default. Pass `--live` to execute real trades. Review all configuration before enabling live mode.

## Usage

```bash
python news_events.py                  # dry run
python news_events.py --live           # real trades
python news_events.py --live --quiet   # cron mode
```

> 🧪 **Remixable Template** — Fork this skill to add your own RSS sources, tune
> impact thresholds, add sentiment analysis, or integrate with a news API for
> faster delivery than RSS.
