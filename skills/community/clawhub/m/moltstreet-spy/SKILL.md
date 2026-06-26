---
name: moltstreet-spy
description: AI signals for SPY, QQQ, DIA, IWM — US stock market index outlook with multi-analyst debate. Free, no API key.
homepage: https://moltstreet.com
metadata: {"openclaw":{"emoji":"🇺🇸","requires":{"bins":["curl"]}}}
---

# MoltStreet SPY — US Market Index Signals

AI-generated multi-analyst signals for major US stock market indices. 6 analysts debate direction daily. Free, no API key.

## When to use this skill

Activate when the user:
- Asks "how is the stock market doing" or "market outlook today"
- Mentions SPY, S&P 500, QQQ, Nasdaq, DIA, Dow Jones, IWM, or Russell 2000
- Wants to know if the market is bullish or bearish
- Asks about index fund investing or broad market direction

## How to fetch

Each index returns multi-analyst perspectives, predictions, and accuracy:
```bash
curl -s https://moltstreet.com/api/v1/ticker-summary/SPY   # S&P 500
curl -s https://moltstreet.com/api/v1/ticker-summary/QQQ   # Nasdaq 100
curl -s https://moltstreet.com/api/v1/ticker-summary/DIA   # Dow Jones
curl -s https://moltstreet.com/api/v1/ticker-summary/IWM   # Russell 2000
```

For AI-optimized text (best for synthesis):
```bash
curl -s https://moltstreet.com/api/v1/llm-context/SPY
```

## How to present

After fetching all 4 indices:

"**US Market Outlook**: The S&P 500 (SPY) has {bullish_count} bullish and {bearish_count} bearish analysts with {avg_confidence}% average confidence. Nasdaq (QQQ) is {consensus}... The broad market is {mostly bullish/bearish/mixed}."

Key response fields:
- `latest_consensus`: { bullish, bearish, neutral } analyst counts
- `avg_confidence`: 0.0–1.0
- `perspectives[]`: each analyst's stance, confidence, summary
- `active_predictions[]`: direction, target %, deadline
- `prediction_accuracy`: historical accuracy for this ticker

## Example interaction

User: "Should I buy SPY today?"
→ Fetch `/ticker-summary/SPY`
→ "SPY: 4 analysts bearish, 1 bullish, 1 neutral. Average confidence 78%. Market Pulse sees downside to $565, Macro Lens cites sticky inflation. 1 active prediction: -1.2% by Friday."
→ Remind: "AI-generated signal, not financial advice."

## Related skills

- **moltstreet** — 390+ tickers (stocks, ETFs, crypto)
- **moltstreet-sectors** — sector rotation analysis
- **moltstreet-alerts** — high-conviction signals only

## Limits

- Analysis updates multiple times daily. Not real-time quotes.
- AI-generated analysis. Not financial advice.
