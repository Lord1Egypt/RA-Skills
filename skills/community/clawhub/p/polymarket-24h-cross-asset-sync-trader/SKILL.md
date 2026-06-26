---
name: polymarket-24h-cross-asset-sync-trader
description: Trades cross-asset correlation divergences in 5-minute crypto "Up or Down" markets on Polymarket. When BTC, ETH, SOL, DOGE, XRP, and BNB have overlapping time windows, highly correlated assets should move together. A divergence (e.g., BTC Up at 55% but ETH Down at 55% in the same 5-min slot) almost always corrects. This skill detects the outlier and trades it toward the group consensus, sizing by conviction.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: 24h Cross-Asset Sync Trader
  difficulty: advanced
---

# 24h Cross-Asset Sync Trader

> **This is a template.**
> The default signal is cross-asset divergence detection in 5-minute crypto "Up or Down" markets — remix it with additional correlation models, momentum overlays, or real-time price feeds.
> The skill handles all the plumbing (market discovery, window grouping, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute "Up or Down" markets for multiple crypto assets in the same time window:

- "Bitcoin Up or Down - March 28, 4:05AM-4:10AM ET"
- "Ethereum Up or Down - March 28, 4:05AM-4:10AM ET"
- "Solana Up or Down - March 28, 4:05AM-4:10AM ET"

Each market is traded independently by retail. But crypto assets are highly correlated — BTC/ETH at ~0.85, BTC/SOL at ~0.75. When the group consensus says "Up" but one asset diverges to "Down," the outlier almost always snaps back.

This skill groups markets by time window, computes the consensus direction, identifies outliers, and trades the correction.

## The Edge: Crypto Correlation Arbitrage

In traditional markets, pairs traders exploit correlated instruments that temporarily diverge. This is the prediction market equivalent for short-duration crypto bets.

### How It Works

1. **Group by window**: Find all "Up or Down" markets sharing the same 5-minute time slot
2. **Compute consensus**: Average the "Up probability" across all assets in the window
3. **Detect outliers**: Find assets whose direction or magnitude deviates from the group mean
4. **Trade the correction**: Bet the outlier moves toward consensus

### Example

| Asset | Direction | Probability | Up Prob |
|-------|-----------|-------------|---------|
| BTC   | Up        | 58%         | 58%     |
| ETH   | Up        | 56%         | 56%     |
| SOL   | Up        | 54%         | 54%     |
| DOGE  | Down      | 55%         | 45%     |

Group mean Up probability: 53%. DOGE diverges at 45% (8% deviation). Trade: buy YES on DOGE (bet it goes Up like the rest).

## Why This Works

1. **Retail trades in silos** — most users view each asset's market independently and don't cross-reference correlated assets in the same window
2. **High correlation is structural** — crypto assets move together because they share macro drivers (risk-on/off, USD strength, regulatory news)
3. **5-minute windows amplify correlation** — in such short periods, idiosyncratic moves are rare; the dominant factor is market-wide sentiment
4. **Mean-reversion is fast** — divergences in correlated assets correct within minutes as arbitrageurs and market makers step in

## Signal Logic

1. Discover all crypto "Up or Down" markets via keyword search
2. Parse each question: extract asset (BTC/ETH/SOL/DOGE/XRP/BNB), date, time window
3. Group into windows by (date, start-end time)
4. For each window with 2+ assets:
   - Compute the group mean "Up probability"
   - Identify assets deviating by more than `MIN_DIVERGENCE`
   - Determine trade direction: push the outlier toward consensus
5. Rank by deviation magnitude
6. Trade only opportunities that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (divergence magnitude + threshold distance), not flat amount

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
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_DIVERGENCE` | `0.04` | Min cross-asset divergence to trigger a trade |

## Edge Thesis

Crypto assets share macro risk factors: BTC dominance, USD index, regulatory headlines, and institutional flow. In a 5-minute window, the probability that BTC goes Up while ETH goes Down is very low — their 5-min return correlation exceeds 0.80.

When Polymarket shows a divergence across correlated assets in the same time slot, it is almost always due to:

- **Asymmetric liquidity** — one asset's market has a large directional order that hasn't been arbitraged
- **Stale pricing** — the market maker on one asset hasn't updated to reflect the latest tick
- **Retail noise** — a speculator has moved one market without considering cross-asset consistency

This skill treats the multi-asset window as a correlation lattice and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
