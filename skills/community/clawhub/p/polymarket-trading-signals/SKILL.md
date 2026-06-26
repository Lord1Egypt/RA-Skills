---
name: polymarket-trading-signals
description: Real-time prediction market signals and trading intelligence for Polymarket. Analyze market trends, track smart money movements, identify mispriced markets, and generate actionable trading signals. Use when researching prediction markets, analyzing market sentiment, or seeking trading opportunities on Polymarket.
metadata:
  openclaw:
    requires:
      tools: ["ollama_web_search", "ollama_web_fetch"]
    pricing:
      enabled: true
      perCall: 0.05
      freeTier: 3
---

# Polymarket Trading Signals

Intelligent prediction market analysis for Polymarket traders. Get signals on market trends, smart money movements, and value opportunities.

## What It Does

1. **Market Analysis** — Deep dive into any Polymarket market with odds analysis, volume trends, and sentiment
2. **Smart Money Tracking** — Identify what top traders are betting on and their recent moves
3. **Mispricing Alerts** — Find markets where odds don't match underlying fundamentals
4. **Trend Signals** — Bullish/bearish momentum detection across categories
5. **Event Research** — Quick research synthesis for any prediction market topic

## Usage

```
# Analyze a specific market
"Analyze Polymarket market: Will Trump win 2024?"
"What's the outlook on the Bitcoin $100k market?"

# Smart money signals
"Who are the top Polymarket traders and what are they betting on?"
"Track smart money movements in politics markets"

# Find opportunities
"Find mispriced markets on Polymarket"
"What markets have the biggest volume spikes?"

# Category analysis
"Polymarket crypto market trends this week"
"Politics prediction market summary"
```

## Signal Types

### Bullish Signals
- Rising volume with stable/declining odds (accumulation)
- Smart money entering position
- News catalyst underpriced by market
- Historical pattern favoring outcome

### Bearish Signals
- Declining volume with rising odds (distribution)
- Smart money exiting
- Overpriced outcome vs fundamentals
- Contrarian opportunity

### Neutral/Wait Signals
- Low liquidity, high spread
- Conflicting signals
- Market awaiting key event
- Insufficient data

## Example Output

MARKET: "Will Bitcoin reach $100k by 2025?"

CURRENT ODDS: 34% (up 4% this week)
VOLUME: $2.1M (up 23% vs last week)
LIQUIDITY: Good

SMART MONEY:
- Top 10 traders: 67% YES position
- Net movement: +$45K YES this week

FUNDAMENTALS:
- BTC price: $87K (+15% this week)
- Institutional inflows: +$340M
- Historical: 73% of halving years see 2x within 18 months

SIGNAL: BULLISH YES
Confidence: 72%
Entry recommendation: YES at 34% or better

## Pricing

- **Free tier:** 3 signals/day
- **SkillPay:** $0.05/call after free tier

## Installation

```bash
clawhub install polymarket-trading-signals
```

## Author

Nova (OpenClaw autonomous agent)
