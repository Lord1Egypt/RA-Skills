---
name: polymarket-micro-pulse-revert-trader
description: Trades mean-reversion on crypto 5-minute interval markets after detecting a single extreme probability pulse (p > 70% or p < 30%) on Polymarket.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Micro Pulse Revert Trader
  difficulty: advanced
---

# Micro Pulse Revert Trader

> **This is a template.**
> The default signal is single-pulse mean-reversion detection in 5-minute crypto Up/Down markets -- remix it with volume filters, multi-pulse confirmation, or cross-coin pulse clustering.
> The skill handles all the plumbing (market discovery, interval parsing, pulse detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists "Bitcoin Up or Down", "Ethereum Up or Down", "Solana Up or Down", and "XRP Up or Down" markets for the same 5-minute windows throughout the day. When a single interval shows an extreme probability reading -- above 70% (extreme Up) or below 30% (extreme Down) -- retail conviction is overextended. The next interval tends to mean-revert rather than continue. The skill trades tiny amounts ($2-$10) on the next interval in the opposite direction.

Example: In the 10:05 AM ET window, BTC shows p=75% (extreme Up pulse, above PULSE_HIGH=0.70). The skill looks at the 10:10 AM window. If that next interval has p >= NO_THRESHOLD (0.58), it trades NO with conviction-scaled sizing. Pulse conviction = (0.75 - 0.70) / (1 - 0.70) = 0.167. Target conviction = (p - 0.58) / (1 - 0.58). Combined conviction averages both, producing a size between $2 and $10.

## Edge

This is a MEAN-REVERSION play targeting retail overreaction in short-duration markets. When a 5-minute interval reaches extreme probability (>70% or <30%), it reflects a burst of one-sided retail flow. These extreme readings are unsustainable because the underlying crypto asset's 5-minute return distribution is roughly symmetric around 50% -- a 75% reading implies the market is pricing in a directional move that rarely materializes at that magnitude. The next interval resets as new participants enter without the same directional bias, and the extreme probability snaps back toward the mean.

## Signal Logic

1. Discover active crypto Up/Down 5-minute markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question: extract coin (BTC/ETH/SOL/XRP), date, and time window
3. Group intervals by (coin, date) and sort chronologically
4. Walk consecutive pairs: if interval[i] has p > `PULSE_HIGH` (default 0.70), it is an extreme Up pulse; if p < `PULSE_LOW` (default 0.30), it is an extreme Down pulse
5. After extreme Up pulse: trade the NEXT interval as NO (mean-revert down) if p >= `NO_THRESHOLD` or pulse is strong enough (p >= 0.48 and pulse >= 0.75)
6. After extreme Down pulse: trade the NEXT interval as YES (mean-revert up) if p <= `YES_THRESHOLD` or pulse is strong enough (p <= 0.52 and pulse <= 0.25)
7. Conviction combines pulse intensity AND target market position -- stronger pulse + better target price = higher conviction
8. Size by conviction, not flat amount -- micro sizing (MAX_POSITION=10)

### Remix Signal Ideas

- **Multi-pulse confirmation**: Require 2 consecutive extreme intervals before trading the 3rd (stronger signal, fewer trades)
- **Cross-coin pulse clustering**: If BTC and ETH both pulse Up in the same window, increase conviction on all reversion trades
- **Pulse magnitude tiers**: Use graduated thresholds (70%, 80%, 90%) with increasing conviction multipliers for more extreme pulses
- **Volume-weighted pulses**: Only trigger on pulses backed by above-average Polymarket volume in that interval

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
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `15` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.42` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.58` | Sell NO only if market probability >= this |
| `SIMMER_PULSE_HIGH` | `0.70` | Extreme Up pulse trigger (previous interval p > this) |
| `SIMMER_PULSE_LOW` | `0.30` | Extreme Down pulse trigger (previous interval p < this) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
