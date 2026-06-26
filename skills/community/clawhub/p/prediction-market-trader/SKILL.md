---
name: prediction-market-trader
description: Prediction market trading toolkit for Kalshi. Includes API authentication (RSA-PSS signatures), market scanning, Sofascore tennis de-vigging, true probability calculation, Kelly criterion sizing, and order execution. Use when trading on Kalshi, analyzing prediction market odds, calculating expected value, de-vigging bookmaker odds, sizing bets with Kelly criterion, or building prediction market bots.
---

# Prediction Market Trader — Kalshi Trading Toolkit

Trade prediction markets with edge. Scan markets, calculate true probabilities, size positions, execute orders.

## Pipeline

1. **Scan** — Pull open markets from Kalshi API by category (sports, weather, politics, economics)
2. **De-vig** — Get bookmaker odds from Sofascore, remove vig to find true probabilities
3. **Compare** — Find gaps between Kalshi price and true probability (minimum 4% edge)
4. **Size** — Quarter-Kelly criterion for position sizing (max 15% of bankroll per trade)
5. **Execute** — Place limit orders via Kalshi API with RSA-PSS authentication
6. **Monitor** — Track positions, P&L, and exit on profit targets

## Requirements

- **Kalshi API credentials** — `KALSHI_KEY_ID` and `KALSHI_PRIVATE_KEY` (RSA private key, inline or .pem)
- **Node.js 18+** — for crypto.sign with RSA-PSS

## Quick Start

```bash
# Set credentials
export KALSHI_KEY_ID=your_key_id
export KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"

# Scan for edges
node scripts/scan-edges.js --category tennis

# Place a trade (dry run)
node scripts/trade.js --ticker KXATPMATCH-26MAR12DRAMED-DRA --side yes --price 38 --count 10 --dry

# Check portfolio
node scripts/portfolio.js
```

## Kalshi API Authentication

Kalshi uses RSA-PSS signatures. The signing message is: `timestamp + method + path` (NO request body in signature).

```javascript
const crypto = require('crypto');
const timestamp = Math.floor(Date.now() / 1000).toString();
const message = timestamp + 'GET' + '/trade-api/v2/portfolio/balance';
const signature = crypto.sign('sha256', Buffer.from(message), {
  key: crypto.createPrivateKey(privateKey),
  padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
  saltLength: 32
});
```

Headers: `KALSHI-ACCESS-KEY`, `KALSHI-ACCESS-TIMESTAMP`, `KALSHI-ACCESS-SIGNATURE` (base64)

## De-Vigging Methodology

Bookmaker odds include a margin (vig). Remove it to find true probabilities:

```
implied_prob_A = 1 / decimal_odds_A
implied_prob_B = 1 / decimal_odds_B
total = implied_prob_A + implied_prob_B  (always > 1.0)
true_prob_A = implied_prob_A / total
true_prob_B = implied_prob_B / total
```

## Kelly Criterion Sizing

```
edge = true_probability - kalshi_price
odds = (1 / kalshi_price) - 1
kelly_fraction = (true_prob * odds - (1 - true_prob)) / odds
position_size = kelly_fraction * 0.25 * bankroll  (quarter-Kelly)
```

Constraints: max 15% bankroll per position, min 4% edge to trade.

## Scripts

- `scripts/kalshi-auth.js` — Kalshi API client with RSA-PSS authentication
- `scripts/scan-edges.js` — Scan markets and compare to Sofascore de-vig
- `scripts/trade.js` — Place/cancel orders with safety checks
- `scripts/portfolio.js` — Check balance, positions, P&L

## References

- `references/market-categories.md` — Kalshi series tickers and best edge sources
- `references/risk-rules.md` — Position sizing rules and risk management
- `references/lessons-learned.md` — Common mistakes and how to avoid them

## Key Insights (Battle-Tested)

- **Tennis qualifying/challengers** = best edge source (5-40% EV gaps)
- **NBA/NHL live markets** = 1¢ spreads, zero edge. Don't bother.
- **NCAAB small conference tournaments** = 4-9% EV
- **Indian Wells main draw** = efficiently priced (within 1-3% of books)
- **Live edges close in 2-3 minutes** — speed matters
- **Weather markets** = high variance, NWS data helps but forecasts shift
- **Always match Odds API outcomes by name, NEVER by array index**
