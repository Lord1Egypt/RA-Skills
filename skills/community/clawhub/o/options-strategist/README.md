# options-strategist

> Analyze live options chains, select strategies by outlook and IV environment, and calculate Greeks + P&L metrics — powered by [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Pro-orange.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-options-red.svg)]()

---

## What This Skill Does

Given a ticker and market outlook, this skill:

1. Fetches the live options chain (all strikes and expirations)
2. Measures the IV environment (ATM IV, IV Rank, skew, HV vs IV)
3. Recommends the optimal strategy from 10+ common options structures
4. Calculates max profit, max loss, break-even, and probability of profit
5. Outputs position Greeks (Delta, Gamma, Theta, Vega)
6. States clear risk management rules (50% profit target, 2× stop)

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/options-strategist):

1. Visit **[https://clawhub.ai/finskills/options-strategist](https://clawhub.ai/finskills/options-strategist)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: I'm bullish on AAPL for the next 45 days. What options strategy should I use?
Claude: [Analyzes options chain, IV environment, recommends bull call spread or cash-secured put, calculates metrics]
```

## Example Triggers

- `"What's the best options strategy for SPY right now?"`
- `"I want to sell premium on NVDA — what's the IV Rank?"`
- `"Design an iron condor on QQQ for this month"`
- `"Calculate the Greeks for a TSLA straddle"`
- `"I think MSFT will stay flat — what options play makes sense?"`

## API Endpoints Used

| Endpoint | Data |
|----------|------|
| `GET /v1/stocks/quote/{symbol}` | Real-time underlying price |
| `GET /v1/stocks/options/{symbol}` | Full options chain with Greeks |
| `GET /v1/stocks/history/{symbol}` | Historical prices for HV calculation |

## Strategy Library

| Strategy | Outlook | IV Preference |
|----------|---------|--------------|
| Long Call | Bullish | Low IV |
| Bull Call Spread | Bullish | Any |
| Cash-Secured Put | Bullish | High IV |
| Long Put | Bearish | Low IV |
| Bear Put Spread | Bearish | Any |
| Bear Call Spread | Bearish | High IV |
| Iron Condor | Neutral | High IV |
| Short Strangle | Neutral | High IV |
| Long Straddle | Volatile | Low IV |
| Covered Call | Mild Bullish | High IV |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — Pro plan required for options chain
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
