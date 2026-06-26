---
name: polymarket-candle-cross-asset-divergence-trader
description: Detects cross-asset divergence in Polymarket crypto 5-minute interval markets. When normally correlated assets like BTC and ETH show contradictory candle directions in overlapping time windows, the divergence tends to close as the less liquid coin converges toward BTC. This is the candlestick equivalent of pairs trading -- exploiting temporary breakdowns in crypto correlation structure.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Candle Cross-Asset Divergence Trader
  difficulty: advanced
---

# Candle -- Cross-Asset Divergence Trader

> **This is a template.**
> The default signal detects cross-asset divergence between BTC and other crypto coins on 5-minute interval markets and trades the convergence using conviction-based sizing. The skill handles all the plumbing (interval parsing, divergence detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval markets for BTC, ETH, SOL, and XRP: "Will Bitcoin be Up or Down in the 10:50AM-10:55AM ET interval?" These resolve to YES (up) or NO (down) based on actual price movement. Crypto assets are highly correlated -- when BTC moves, ETH/SOL/XRP typically follow within minutes. But on Polymarket's discrete 5-minute intervals, this correlation occasionally breaks down: BTC shows UP (>55%) while ETH shows DOWN (<45%) in the same time window. This divergence is structurally temporary because the underlying correlation reasserts itself. The less liquid coin (ETH/SOL/XRP) tends to converge toward BTC's direction.

## Edge

Unlike generic correlation trading that requires continuous price feeds and complex cointegration models, this skill operates on Polymarket's discrete binary outcomes where the divergence signal is unambiguous:

1. **Structural correlation** -- BTC, ETH, SOL, and XRP share macro drivers (risk appetite, USD strength, regulatory news) that create persistent positive correlation on 5-minute timeframes
2. **Liquidity hierarchy** -- BTC interval markets are more liquid and efficiently priced; when BTC and a follower coin disagree, BTC is more likely correct because it incorporates information faster
3. **Discrete binary resolution** -- each interval resolves to UP or DOWN, meaning a divergence between BTC=UP and ETH=DOWN must close by resolution time; one of them is wrong, and structural correlation says the follower is more likely wrong
4. **Market segmentation** -- Polymarket participants trading ETH intervals may not simultaneously monitor BTC intervals, creating temporary informational inefficiency across correlated assets

## Signal Logic

1. Discover crypto interval markets via keyword search (`Bitcoin Up or Down`, `Ethereum Up or Down`, `Solana Up or Down`, `XRP Up or Down`) with a `get_markets(limit=200)` fallback
2. Parse each question to extract (coin, date, start_time_minutes) using regex
3. Group markets by (date, time_window) to find overlapping intervals across coins
4. For each window with BTC + at least one follower coin, compare candle directions:
   - UP: probability > 0.55
   - DOWN: probability < 0.45
   - NEUTRAL: 0.45-0.55 (ignored)
5. Detect divergence: BTC and follower show opposite directions with divergence >= `DIV_THRESHOLD`
6. Trade the follower coin toward BTC's direction (convergence trade):
   - BTC UP + follower DOWN -> buy YES on follower
   - BTC DOWN + follower UP -> sell NO on follower
7. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Weighted correlation** -- use historical 5-minute correlation coefficients between BTC and each follower to weight the divergence signal; higher historical correlation means stronger convergence expectation
- **Volume-gated divergence** -- only trade divergences where BTC's interval has high volume (confident signal) and the follower has low volume (inefficient pricing)
- **Multi-coin divergence** -- if BTC is UP but ALL followers are DOWN, the signal is weaker (BTC might be the outlier); if only one follower diverges while others agree with BTC, the signal is stronger
- **Time decay** -- divergences detected early in the 5-minute window have more time to converge; weight signals by remaining time to interval resolution
- **Cascade detection** -- if a BTC move triggers ETH convergence 5-10 minutes later in historical data, use the lag to front-run the convergence on the next interval

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
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_DIV_THRESHOLD` | `0.08` | Min divergence between BTC and follower coin |

## Edge Thesis

Crypto assets on Polymarket's 5-minute interval markets exhibit strong positive correlation driven by shared macro factors. When BTC and a follower coin (ETH, SOL, XRP) show contradictory candle directions in the same time window -- BTC UP while ETH DOWN, or vice versa -- this divergence is structurally temporary. BTC, being the most liquid and efficiently priced, is more likely correct. The follower coin's interval market is mispriced and tends to converge toward BTC's direction before resolution. The skill exploits this convergence with conviction-based sizing that scales with the distance from the trading threshold.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
