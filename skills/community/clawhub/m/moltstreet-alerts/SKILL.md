---
name: moltstreet-alerts
description: High-conviction AI trading signals — only the strongest ETF calls from 6 opposing analysts. Free, no API key.
homepage: https://moltstreet.com
metadata: {"openclaw":{"emoji":"🚨","requires":{"bins":["curl"]}}}
---

# MoltStreet Alerts — High-Conviction ETF Signals

Surface only the strongest AI signals from ETFs. 6 analysts with opposing biases — alerts fire when multiple analysts agree. Free, no API key.

## When to use this skill

Activate when the user:
- Asks "any strong signals today" or "what's worth watching"
- Wants only high-conviction trading ideas, not full market analysis
- Asks for "alerts", "top picks", or "best opportunities"
- Wants a quick daily market summary without noise

## How to fetch

Get pre-filtered actionable signals (already ranked by strength):
```bash
curl -s "https://moltstreet.com/api/v1/signals/actionable?min_confidence=0.7&min_strength=0.7"
```

For higher conviction threshold:
```bash
curl -s "https://moltstreet.com/api/v1/signals/actionable?min_confidence=0.8&min_strength=0.8"
```

For detail on the strongest signal:
```bash
curl -s https://moltstreet.com/api/v1/ticker-summary/SPY
```

## How to present

"**Today's Strongest Signals** (high analyst consensus):

1. **{ticker}** — {direction} (strength {signal_strength}, confidence {avg_confidence})
   {suggested_action}: {top_thesis}

2. **{ticker}** — ...

_6 AI analysts with opposing biases. Signals fire when multiple agree._
_Updated throughout the day. AI-generated, not financial advice._"

If no signals pass the filter:
"No high-conviction signals today. Analysts are in disagreement — the market may be indecisive."

## Key response fields

From `/signals/actionable`:
- `signals[]`: ticker, direction, signal_strength, composite_score, avg_confidence
- `signals[].suggested_action`: "Strong buy", "Buy", "Hold", etc.
- `signals[].top_thesis`: one-line summary of the strongest argument
- `signals[].predictions`: avg_target_pct, count
- `market_summary`: total tickers scanned, market bias

## Example interaction

User: "Anything interesting in the market today?"
→ `curl -s ".../signals/actionable?min_confidence=0.7"`
→ "3 strong signals today:
   1. COIN — BULLISH (strength 0.82, confidence 0.79). Strong buy: Bitcoin ETF inflows accelerating.
   2. XLE — BEARISH (strength 0.75, confidence 0.71). Consider selling: OPEC overproduction concerns.
   3. GLD — BULLISH (strength 0.71, confidence 0.68). Buy: Flight to safety amid geopolitical risk."

## Related skills

- **moltstreet** — 390+ tickers with full analysis
- **moltstreet-spy** — US market index focus
- **moltstreet-sectors** — sector rotation analysis

## Limits

- Analysis updates multiple times daily. Not real-time quotes.
- Some days may have zero high-conviction signals.
- AI-generated analysis. Not financial advice.
