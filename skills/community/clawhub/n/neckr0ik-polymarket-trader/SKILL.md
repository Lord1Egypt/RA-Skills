---
name: neckr0ik-polymarket-trader
version: 1.0.0
description: Detect arbitrage opportunities on Polymarket. Monitor spread arbitrage, cross-market correlations, news-driven opportunities. Use for prediction market trading and risk-free profit detection.
---

# Polymarket Arbitrage Detector

Detect risk-free arbitrage opportunities on Polymarket.

## Quick Start

```bash
# Scan all markets for arbitrage opportunities
neckr0ik-polymarket-trader scan

# Monitor specific market for spreads
neckr0ik-polymarket-trader monitor --market "will-trump-declare-war"

# Find cross-platform arbitrage
neckr0ik-polymarket-trader cross-platform --markets bitcoin-100k

# Correlate news with markets
neckr0ik-polymarket-trader news --keywords "Israel,Iran,war"
```

## What This Detects

### 1. Direct Spread Arbitrage
When YES + NO prices don't equal $1.00.

```
Example:
YES: $0.48
NO: $0.50
Combined: $0.98
Profit: $0.02 (2.04% risk-free)
```

### 2. Cross-Market Correlation
Related markets with inconsistent pricing.

```
Example:
"Trump wins 2026?" @ 55%
"Republican wins?" @ 48%
→ Logically impossible. Trump > Republican shouldn't happen.
```

### 3. News-Driven Opportunities
Breaking news vs. market pricing.

```
Example:
News: "Israel strikes Tehran. Trump demands surrender."
Market: "Will Trump declare war on Iran?" @ 40%
Signal: Military action ≠ war declaration. May be overpriced.
```

### 4. Cross-Platform Arbitrage
Same event on Polymarket vs Kalshi.

```
Example:
Polymarket: "BTC > $100k by EOY" YES @ 0.55
Kalshi: Same market YES @ 0.62
→ Buy Polymarket, sell Kalshi. 7% locked profit.
```

### 5. Endgame Arbitrage
Near-certain outcomes close to resolution.

```
Example:
Market resolves in 48 hours
Current price: $0.97
Buy and hold to $1.00
→ 3% profit in 2 days (548% annualized)
```

## Commands

### scan

Scan all markets for arbitrage.

```bash
neckr0ik-polymarket-trader scan [options]

Options:
  --min-spread <pct>    Minimum spread percentage (default: 2)
  --max-results <n>     Max results to return (default: 20)
  --output <format>     Output format (table, json, csv)
```

### monitor

Continuously monitor specific markets.

```bash
neckr0ik-polymarket-trader monitor --market <id> [options]

Options:
  --interval <sec>      Check interval (default: 5)
  --alert-spread <pct>  Alert when spread exceeds threshold
  --webhook <url>       Send alerts to webhook
```

### cross-platform

Compare prices across platforms.

```bash
neckr0ik-polymarket-trader cross-platform [options]

Options:
  --platforms <list>    Platforms to compare (polymarket,kalshi)
  --min-spread <pct>    Minimum spread (default: 3)
```

### news

Correlate breaking news with markets.

```bash
neckr0ik-polymarket-trader news --keywords <terms> [options]

Options:
  --sources <list>      News sources (reuters,ap,cnbc,bbc)
  --market-keywords <list>  Polymarket search terms
  --alert               Send alerts on correlation
```

### endgame

Find near-resolution opportunities.

```bash
neckr0ik-polymarket-trader endgame [options]

Options:
  --min-prob <pct>      Minimum probability (default: 95)
  --max-days <n>        Max days to resolution (default: 7)
  --min-roi <pct>       Minimum annualized ROI (default: 100)
```

## Output Examples

### Spread Arbitrage Detection

```
ARBITRAGE FOUND
Market: Will Bitcoin reach $100k by EOY 2026?
YES Price: $0.48
NO Price: $0.50
Spread: 2.0% ($0.02)
Volume: $1.2M
Profit/Trade: $20 per $1,000
Annualized: 548% (if held 2 days)
```

### Cross-Market Correlation

```
CORRELATION VIOLATION
Market 1: "Will Trump win 2026?" @ 55%
Market 2: "Will a Republican win?" @ 48%
Issue: Trump winning implies Republican wins
Logic: Market 1 should be <= Market 2
Action: Sell Market 1 YES, Buy Market 2 NO
```

### News Correlation

```
NEWS-MARKET CORRELATION
Breaking News: "Israel strikes Tehran. Trump demands surrender."
Related Markets:
  1. "Will Trump declare war on Iran?" @ 40% → May be OVERPRICED
  2. "Will Israel strike Lebanon?" @ 85% → Already occurred
  3. "Will oil hit $100?" @ 25% → May be UNDERPRICED
Signal: Military action ≠ formal war declaration
```

## Risk Management

- **Spread threshold:** Only trade spreads > 2% (after fees)
- **Position limit:** Max 10% of portfolio per market
- **Resolution clarity:** Avoid subjective markets
- **Execution speed:** Use WebSocket, not polling

## Technical Details

### Detection Speed Requirements

| Method | Detection Time | Execution |
|--------|---------------|-----------|
| Manual | Minutes | Seconds |
| Semi-auto | Seconds | Manual |
| Full bot | Milliseconds | Sub-100ms |

### Fee Structure

| Platform | Fee |
|----------|-----|
| Polymarket US | 0.01% |
| Polymarket Int'l | 2% on winnings |
| Polygon gas | ~$0.007 |

## See Also

- `references/polymarket-strategies.md` — Full strategy guide
- `scripts/arbitrage_detector.py` — Detection engine
- `scripts/news_correlator.py` — News-market correlation