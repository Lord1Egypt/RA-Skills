---
name: polymarket-bundle-cross-coin-5min-trader
description: Trades cross-coin divergence in 5-minute crypto Up/Down bundles on Polymarket. BTC, ETH, SOL, and XRP move together in practice -- when one coin diverges from the group consensus in the same 5-min window, it is likely to revert. Sizes by conviction with divergence magnitude scaling.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Cross-Coin 5min Divergence Trader
  difficulty: advanced
---

# Bundle -- Cross-Coin 5min Divergence Trader

> **This is a template.**
> The default signal is cross-coin divergence detection within 5-minute crypto Up/Down bundles -- remix it with on-chain correlation data or additional coins.
> The skill handles all the plumbing (market discovery, time window grouping, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists "Bitcoin Up or Down", "Ethereum Up or Down", "Solana Up or Down", and "XRP Up or Down" markets for the same 5-minute windows throughout the day. Crypto assets are highly correlated -- when BTC moves up, ETH/SOL/XRP almost always follow. When one coin's market price diverges from the group consensus, it is structural mispricing that should revert.

Example: In the 10:05 AM ET window, if BTC=Up(60%), ETH=Up(55%), SOL=Down(40%), then SOL is the outlier. The group consensus is ~52% Up, but SOL is priced at 40% -- a 12% deviation that should close as correlated price action propagates.

## Edge

Crypto correlation is the strongest cross-asset relationship in financial markets. BTC, ETH, SOL, and XRP have 30-day rolling correlations consistently above 0.80. Within a 5-minute window, the correlation is even higher because macro moves dominate and idiosyncratic moves are negligible. Polymarket prices each coin's Up/Down market independently -- different order books, different liquidity pools, different retail participants. When one coin's order book gets hit by a directional flow that doesn't appear in the others, the resulting price divergence is a mean-reversion opportunity.

## Signal Logic

1. Discover active crypto Up/Down 5-minute markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question: extract coin (BTC/ETH/SOL/XRP), date, and time window
3. Normalize time windows to 5-minute buckets for cross-coin matching
4. Group markets by (date, time_bucket) -- find windows where 2+ coins have markets
5. For each window: compute group consensus (mean probability across all coins in the window)
6. Find outliers: any coin deviating > `SIMMER_MIN_DEVIATION` (default 10%) from group mean
7. Trade outlier toward group mean: buy YES if below, sell NO if above
8. Size by conviction (deviation magnitude), not flat amount

### Remix Signal Ideas

- **On-chain correlation feed**: Pull real-time BTC/ETH/SOL/XRP price feeds from CoinGecko or Binance API -- compute rolling 5-min correlation and weight the mean-reversion trade by current correlation strength
- **Volume-weighted consensus**: Instead of simple mean, weight each coin's contribution to the group consensus by its Polymarket volume -- higher-volume coins anchor the consensus more strongly
- **Momentum filter**: Check if the outlier coin has idiosyncratic news (e.g., SOL network outage) that justifies decoupling -- skip those divergences
- **Multi-window confirmation**: Require divergence to persist across 2+ consecutive 5-min windows before trading -- filters out noise from order book mechanics

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
| `SIMMER_MIN_DEVIATION` | `0.10` | Min deviation from group mean to trigger a trade |

## Edge Thesis

Traditional crypto exchanges maintain cross-asset consistency through arbitrage bots that trade correlated pairs in milliseconds. Polymarket has no such mechanism -- each coin's Up/Down market is an independent order book with its own retail participants. 5-minute crypto Up/Down markets are particularly vulnerable because:

- Short time windows mean correlation is near-maximum (macro dominates, idiosyncratic noise is minimal)
- Each coin attracts different retail communities (BTC maxis, ETH DeFi traders, SOL memecoin traders)
- Directional flow on one coin doesn't propagate to the others
- New 5-min windows open frequently, creating fresh opportunities every few minutes
- Retail prices each coin in isolation rather than as a correlated basket

This skill treats the cross-coin bundle as a correlated group and trades the outlier back toward the consensus.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
