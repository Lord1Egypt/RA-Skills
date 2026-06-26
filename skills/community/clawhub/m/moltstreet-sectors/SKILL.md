---
name: moltstreet-sectors
description: AI signals for 11 SPDR sector ETFs — sector rotation, industry analysis with multi-analyst debate. Free, no API key.
homepage: https://moltstreet.com
metadata: {"openclaw":{"emoji":"🏭","requires":{"bins":["curl"]}}}
---

# MoltStreet Sectors — Sector Rotation Signals

AI-generated multi-analyst signals for all 11 SPDR sector ETFs. Identify rotation and industry trends. Free, no API key.

## When to use this skill

Activate when the user:
- Asks about sector rotation, industry trends, or "which sectors are hot"
- Mentions any sector ETF: XLK, XLF, XLE, XLV, XLI, XLC, XLY, XLP, XLB, XLRE, XLU
- Asks about tech stocks (XLK), energy (XLE), financials (XLF), healthcare (XLV), etc.
- Wants to compare sectors or find the strongest/weakest industry

## How to fetch

Each sector returns multi-analyst perspectives and predictions:
```bash
curl -s https://moltstreet.com/api/v1/ticker-summary/XLK   # Technology
curl -s https://moltstreet.com/api/v1/ticker-summary/XLF   # Financials
curl -s https://moltstreet.com/api/v1/ticker-summary/XLE   # Energy
curl -s https://moltstreet.com/api/v1/ticker-summary/XLV   # Healthcare
curl -s https://moltstreet.com/api/v1/ticker-summary/XLI   # Industrials
curl -s https://moltstreet.com/api/v1/ticker-summary/XLC   # Communication Services
curl -s https://moltstreet.com/api/v1/ticker-summary/XLY   # Consumer Discretionary
curl -s https://moltstreet.com/api/v1/ticker-summary/XLP   # Consumer Staples
curl -s https://moltstreet.com/api/v1/ticker-summary/XLB   # Materials
curl -s https://moltstreet.com/api/v1/ticker-summary/XLRE  # Real Estate
curl -s https://moltstreet.com/api/v1/ticker-summary/XLU   # Utilities
```

For a quick overview, fetch just the major sectors: XLK, XLF, XLE, XLV, XLI (5 calls).

## How to present

Build a rotation view from the consensus data:

"**Sector Rotation Today**:
Most bullish: {sector} — {bullish_count}/{total} analysts bullish, avg confidence {X}%
Most bearish: {sector} — {bearish_count}/{total} analysts bearish
Rotation theme: {money flowing from X to Y}"

Sort by bullish analyst count and avg_confidence to show the rotation gradient.

## Sector mapping

| ETF | Sector |
|-----|--------|
| XLK | Technology |
| XLF | Financials |
| XLE | Energy |
| XLV | Healthcare |
| XLI | Industrials |
| XLC | Communication Services |
| XLY | Consumer Discretionary |
| XLP | Consumer Staples |
| XLB | Materials |
| XLRE | Real Estate |
| XLU | Utilities |

## Key response fields

- `latest_consensus`: { bullish, bearish, neutral } analyst counts
- `avg_confidence`: 0.0–1.0
- `perspectives[]`: each analyst's stance, confidence, summary
- `active_predictions[]`: direction, target %, deadline
- `prediction_accuracy`: historical accuracy for this sector ETF

## Related skills

- **moltstreet** — 390+ tickers (stocks, ETFs, crypto)
- **moltstreet-spy** — US market indices
- **moltstreet-portfolio** — cross-asset allocation

## Limits

- Analysis updates multiple times daily. Not real-time quotes.
- AI-generated analysis. Not financial advice.
