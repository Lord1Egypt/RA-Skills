---
name: polymarket-candle-morning-star-trader
description: Trades crypto "Up or Down" 5-minute interval markets on Polymarket by detecting Morning Star (DOWN-doji-UP bottom reversal) and Evening Star (UP-doji-DOWN top reversal) candlestick patterns. When the 4th interval hasn't fully priced in the reversal, there is edge in trading the new trend direction. Conviction scales with the lag distance from the expected reversal price.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Morning Star Trader
  difficulty: advanced
---

# Candle Morning Star Trader

> **This is a template.**
> The default signal detects Morning Star and Evening Star reversal patterns in crypto 5-min interval markets and trades the reversal continuation on the 4th interval -- remix it with volume spikes, real-time price feeds, or RSI confirmation.
> The skill handles all the plumbing (market discovery, interval parsing, pattern detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists hundreds of live crypto "Up or Down" 5-minute interval markets per day across Bitcoin, Ethereum, and Solana. Each asks whether a coin will go up or down in a specific 5-minute window (e.g. "Bitcoin Up or Down - March 29, 10:50AM-10:55AM ET").

The "Morning Star" is a classic three-candle bottom reversal pattern:
1. Strong DOWN interval (p < 0.43) -- establishes bearish momentum
2. Doji/neutral interval (0.47 < p < 0.53) -- indecision, selling exhausts
3. Strong UP interval (p > 0.57) -- buyers take control, reversal confirmed

If the 4th interval hasn't fully priced in the reversal (still below 0.55), the continuation trade has edge. The "Evening Star" is the bearish mirror: UP -> doji -> DOWN signals a top reversal.

## Edge

Star reversal patterns work because they capture a structural shift in market sentiment:

1. **Exhaustion detection** -- The doji (neutral) candle after a strong move signals that the prior trend is running out of steam; this is the single most reliable reversal signal in candlestick analysis
2. **Confirmation candle** -- The third candle moving strongly in the opposite direction confirms the reversal; two signals (exhaustion + reversal) compound the probability
3. **Lag exploitation** -- Polymarket prices each 5-min interval somewhat independently; the 4th interval often hasn't incorporated the reversal signal from the preceding three
4. **Multi-coin coverage** -- Scanning Bitcoin, Ethereum, and Solana multiplies pattern opportunities by 3x

## Signal Logic

1. Discover active crypto "Up or Down" 5-min interval markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question to extract coin, date, and time window (e.g. "Bitcoin", "March 29", "10:50AM", "10:55AM")
3. Group by (coin, date) and sort by time window
4. Scan for three consecutive intervals matching:
   - Morning Star: p1 < (0.5 - STAR_BODY), p2 within (0.5 +/- STAR_DOJI), p3 > (0.5 + STAR_BODY)
   - Evening Star: p1 > (0.5 + STAR_BODY), p2 within (0.5 +/- STAR_DOJI), p3 < (0.5 - STAR_BODY)
5. After detecting pattern, check the 4th interval:
   - Morning Star + 4th < 0.55: buy YES (reversal not fully priced)
   - Evening Star + 4th > 0.45: buy NO (reversal not fully priced)
6. Conviction scales with lag distance from expected reversal price
7. Size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **Volume spike confirmation**: Morning/Evening Stars are strongest when the doji candle has unusually high volume -- it means the exhaustion was contested, making the reversal more meaningful
- **RSI divergence**: If RSI on the underlying coin was oversold during the DOWN candle of a Morning Star, the reversal has higher probability
- **Pattern completeness score**: Weight patterns where the UP candle fully retraces the DOWN candle (or vice versa) higher than partial retracements
- **Time-of-day filter**: Reversals at session opens (US, Asia, Europe) are more reliable than mid-session; weight signals by proximity to session boundaries
- **Double star detection**: Two Morning Stars within 30 minutes = extremely strong bottom signal; increase conviction 2x

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-session) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_STAR_BODY` | `0.07` | Min distance from 0.5 for strong candles (UP/DOWN) |
| `SIMMER_STAR_DOJI` | `0.03` | Max distance from 0.5 for the middle doji candle |

## Edge Thesis

Morning Star and Evening Star are among the most reliable reversal patterns in technical analysis. They work because they encode a three-phase narrative: (1) the prevailing trend pushes hard, (2) momentum exhausts and the market pauses (doji), (3) the opposing side takes control with a strong counter-move. In Polymarket's 5-min interval structure, each interval is priced somewhat independently by participants who focus on the current window rather than the sequence. This means the 4th interval after a completed star pattern often hasn't incorporated the reversal signal, creating a lag that this skill exploits. The pattern is rare enough (requires exact sequencing of three candle types) that when it appears, it carries genuine informational content.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
