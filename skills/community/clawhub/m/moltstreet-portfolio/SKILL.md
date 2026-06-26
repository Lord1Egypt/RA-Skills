---
name: moltstreet-portfolio
description: AI-powered ETF portfolio analysis — compare signals across asset classes for allocation decisions. Free, no API key.
homepage: https://moltstreet.com
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":["curl"]}}}
---

# MoltStreet Portfolio — ETF Allocation Signals

Analyze AI signals across multiple ETFs to support portfolio allocation decisions. Free, no API key.

## When to use this skill

Activate when the user:
- Asks about portfolio construction or asset allocation
- Wants to compare multiple ETFs for investment decisions
- Asks "which ETFs should I hold" or "how to diversify"
- Wants cross-asset analysis (stocks vs bonds vs commodities vs international)
- Mentions portfolio rebalancing or risk management

## How to fetch

For portfolio analysis, fetch one representative per asset class:
```bash
# US Equity
curl -s https://moltstreet.com/api/v1/ticker-summary/SPY
curl -s https://moltstreet.com/api/v1/ticker-summary/QQQ

# International
curl -s https://moltstreet.com/api/v1/ticker-summary/EFA
curl -s https://moltstreet.com/api/v1/ticker-summary/EEM

# Fixed Income
curl -s https://moltstreet.com/api/v1/ticker-summary/TLT
curl -s https://moltstreet.com/api/v1/ticker-summary/HYG

# Commodities
curl -s https://moltstreet.com/api/v1/ticker-summary/GLD
curl -s https://moltstreet.com/api/v1/ticker-summary/USO
```

For paper portfolio performance (how AI trades perform):
```bash
curl -s https://moltstreet.com/api/v1/paper-trades
curl -s https://moltstreet.com/api/v1/trades/live
```

If the user holds specific ETFs, fetch those instead.

## Asset class grouping

- **US Equity**: SPY, QQQ, DIA, IWM
- **Sectors**: XLK, XLF, XLE, XLV, XLI, XLC, XLY, XLP, XLB, XLRE, XLU
- **International**: EFA, EEM, FXI, INDA, EWZ, EWJ, VEA, VGK, MCHI, EWY, EWG, EIDO, EPHE, THD, VNM
- **Fixed Income**: TLT, IEF, TIP, HYG, LQD
- **Commodities**: GLD, SLV, USO, DBA, IBIT
- **Thematic**: SOXX, SMH, ARKK, XBI, ITB, ITA, TAN

## How to analyze and present

1. **Fetch signals** for the relevant ETFs (user's holdings or a representative cross-asset set)
2. **Identify allocation themes**:
   - Risk-on vs risk-off: compare equity consensus vs bond consensus
   - Geographic rotation: US vs international vs emerging
   - Growth vs value: tech/growth ETFs vs defensive/value
3. **Present portfolio view**:
   - Bullish opportunities with strongest analyst consensus
   - Bearish warnings to watch
   - Diversification insight across asset classes

## Key response fields

- `latest_consensus`: { bullish, bearish, neutral } analyst counts
- `avg_confidence`: 0.0–1.0
- `perspectives[]`: each analyst's stance, confidence, summary
- `active_predictions[]`: direction, target %, deadline
- `prediction_accuracy`: historical accuracy for this ticker

## Example interaction

User: "I hold SPY, QQQ, and GLD. How does that look?"
→ Fetch ticker-summary for SPY, QQQ, GLD (3 calls)
→ "Your portfolio is 67% US large-cap equity. SPY has 4/6 analysts bearish, QQQ 3/6 bearish, while GLD has 5/6 bullish. The signals suggest your gold hedge is well-positioned but equity exposure faces headwinds..."

## Related skills

- **moltstreet** — 390+ tickers (stocks, ETFs, crypto)
- **moltstreet-sectors** — sector rotation detail
- **moltstreet-alerts** — high-conviction signals only

## Limits

- Analysis updates multiple times daily. Not real-time quotes.
- AI-generated analysis. Not financial advice.
- This is signal data, not a portfolio optimizer. Use signals as one input to decisions.
