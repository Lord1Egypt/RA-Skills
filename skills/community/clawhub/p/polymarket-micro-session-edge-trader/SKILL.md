---
name: polymarket-micro-session-edge-trader
description: Trades session-transition mean-reversion in 5-minute crypto "Up or Down" markets on Polymarket, fading directional bursts that occur during US, Asia, and Europe session opens.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Micro Session Edge Trader
  difficulty: advanced
---

# Micro Session Edge Trader

> **This is a template.**
> The default signal is session-transition burst detection and mean-reversion in 5-minute crypto "Up or Down" markets -- remix it with additional session models, volume overlays, or cross-asset filters.
> The skill handles all the plumbing (market discovery, interval parsing, session detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Crypto markets trade 24/7, but liquidity and volatility are not evenly distributed. Three key session transitions create predictable volatility bursts in Polymarket's 5-minute "Up or Down" markets (BTC, ETH, SOL, XRP):

- **US_OPEN** (9:30-10:00 ET): NYSE opens, institutional flow hits crypto
- **ASIA_OPEN** (20:00-20:30 ET): Tokyo/Hong Kong come online
- **EU_OPEN** (3:00-3:30 ET): London session begins

The first 2 five-minute intervals after a session open tend to move directionally (the "burst"). The 3rd interval frequently reverts as the initial impulse fades and mean-reversion kicks in. The skill detects confirmed bursts and trades the fade.

Example: US_OPEN session, BTC markets:

| Interval | Time | Direction | Probability |
|----------|------|-----------|-------------|
| 1st | 9:30-9:35 | Up | 62% |
| 2nd | 9:35-9:40 | Up | 65% |
| 3rd (fade target) | 9:40-9:45 | Up | 58% |

Burst confirmed: 2 consecutive Up intervals (avg 63.5%). Fade: sell NO on the 3rd interval (bet it reverts Down). Conviction = (0.58 - 0.48) / 0.30 = 0.33, burst_strength boost = (0.635 - 0.55) / 0.45 = 0.19, combined = min(1.0, 0.33 + 0.3 * 0.19) = 0.39, size = max($2, 0.39 * $10) = $3.87.

## Edge

Session transitions are the most volatile periods in any market. In crypto, where 24/7 trading means no single "close" to anchor overnight risk, the US, Asia, and Europe opens create mini-opens with predictable burst-then-revert patterns. Institutional flow arrives in waves creating directional pressure that overshoots. Retail 5-minute market participants pile into the burst direction, pushing prices past fair value. After the initial burst, market makers and contrarian flow bring prices back toward equilibrium. Polymarket's 5-minute interval markets are priced by retail participants who chase the burst direction, creating a systematic overshoot that reverts within 1-2 intervals. The timing is predictable -- session opens happen at the same time every day.

## Signal Logic

1. Discover all crypto "Up or Down" 5-minute markets via keyword search (BTC, ETH, SOL, XRP)
2. Parse each question: extract asset, date, start time, end time (as minutes since midnight ET)
3. Group intervals by (asset, date), sort chronologically
4. For each session window (US_OPEN 9:30-10:00, ASIA_OPEN 20:00-20:30, EU_OPEN 3:00-3:30):
   - Find intervals whose start time falls within the window
   - Check if first 2 intervals show same directional bias (both Up or both Down)
   - If confirmed burst: the 3rd interval (or first after window) is the fade target
5. Fade direction is opposite to burst: up-burst -> sell NO, down-burst -> buy YES
6. Filter out past intervals (only trade upcoming/current based on ET clock)
7. Conviction scales with threshold distance + burst strength boost (how extreme the burst average was)
8. Size by conviction, not flat amount -- micro sizing (MAX_POSITION=10)

### Remix Signal Ideas

- **Volume confirmation**: Only trade fades when the burst intervals had above-average Polymarket volume
- **Multi-session confluence**: Weight fades higher when 2+ session windows overlap or when multiple coins burst simultaneously
- **Exchange correlation feed**: Pull real-time BTC/ETH/SOL/XRP prices from Binance to confirm the on-chain momentum matches Polymarket burst
- **Adaptive windows**: Dynamically adjust session window boundaries based on historical burst timing data

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
| `SIMMER_MAX_POSITION` | `10` | Max USDC per trade at full conviction (micro) |
| `SIMMER_MIN_TRADE` | `2` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `1000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.12` | Max bid-ask spread |
| `SIMMER_MAX_POSITIONS` | `15` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.42` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.58` | Sell NO only if market probability >= this |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
