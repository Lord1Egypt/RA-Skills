---
name: polymarket-macro-crypto-geopolitics-trader
description: Trades the lag between geopolitical escalation markets and crypto price threshold markets on Polymarket. When Iran military action probability rises, BTC threshold markets should reprice lower but often lag behind. Captures the divergence before convergence.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Crypto-Geopolitics Lag Trader
  difficulty: advanced
---

# Crypto-Geopolitics Lag Trader

> **This is a template.**
> The default signal computes geopolitical heat and crypto optimism scores, then trades crypto threshold markets that are lagging behind geopolitical repricing -- remix it with oil futures data, crypto funding rates, or defense ETF flows.
> The skill handles all the plumbing (market discovery, geo/crypto classification, divergence detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Iran military escalation leads to oil price spikes which lead to crypto drops -- this is the well-documented crisis inverse correlation. On Polymarket, geopolitical escalation markets (Iran, Israel, military action) and crypto price threshold markets (Bitcoin above $X) are traded by different communities. When a geopolitical shock hits, the geo markets reprice within minutes but crypto threshold markets often take hours to adjust. This skill detects that lag and trades it.

## Edge

Geo-crypto divergence captures a structural information asymmetry:

1. **Community segregation** -- Geopolitics traders and crypto traders are largely separate populations on Polymarket; they watch different news feeds and react to different catalysts
2. **Causal chain delay** -- The Iran escalation -> oil spike -> crypto drop chain has multiple links; each link adds repricing delay
3. **Anchoring bias** -- Crypto traders anchor to recent BTC price levels and are slow to update threshold market probabilities in response to geopolitical events
4. **Inverse correlation in crisis** -- The BTC-geopolitical risk inverse correlation is strongest during acute crises, which is exactly when the lag is largest

## Signal Logic

1. Discover ALL active markets via `get_markets(limit=200)` (primary) + keyword `find_markets()` (supplement)
2. Classify markets:
   - **Geopolitical escalation**: Iran, Israel, military, war, attack, strike, missile, escalation
   - **Geopolitical de-escalation**: ceasefire, peace, truce, negotiation (inverted for heat calc)
   - **Crypto threshold**: Bitcoin above $X, Bitcoin price, BTC above, ETH above
3. Compute **geo_heat**: weighted average of escalation market probabilities (de-escalation inverted)
   - Higher geo_heat = more conflict expected
4. Compute **crypto_optimism**: average of crypto threshold market probabilities
   - Higher crypto_optimism = market expects crypto to stay above thresholds
5. Detect divergence:
   - **crypto_lagging_high**: geo_heat > 0.60 (hot) but crypto_optimism > 0.50 (still bullish) -- crypto should be lower
   - **crypto_lagging_low**: geo_heat < 0.40 (calming) but crypto_optimism < 0.50 (still bearish) -- crypto should be higher
   - Minimum divergence of CRYPTO_LAG (default 0.10) required to trade
6. Trade crypto threshold markets in the lagging direction:
   - crypto_lagging_high: sell NO on high crypto thresholds (p >= 62%)
   - crypto_lagging_low: buy YES on low crypto thresholds (p <= 38%)
7. Conviction scales with distance from threshold; size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **Oil futures overlay**: Wire Brent crude price data into the signal -- if oil spiked 5%+ in the last hour alongside geo heat, conviction doubles on crypto downside trades
- **Crypto funding rates**: Negative perpetual funding rates confirm bearish sentiment has reached derivatives markets; if funding is still positive during geo heat, the crypto lag is even larger
- **Defense ETF flows**: Rising inflows to defense ETFs (ITA, XAR) during geo escalation confirm institutional risk-off positioning
- **Historical lag measurement**: Track how long crypto took to reprice after previous geo shocks to calibrate the CRYPTO_LAG parameter

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
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_GEO_HOT` | `0.60` | Geo heat threshold for "hot" conflict detection |
| `SIMMER_CRYPTO_LAG` | `0.10` | Minimum geo-crypto divergence required to trade |

## Edge Thesis

Geopolitical escalation and crypto prices are inversely correlated during crises -- when Iran tensions spike, oil rises, risk appetite drops, and crypto falls. But on Polymarket, these asset classes are traded by different communities with different information flows. Geopolitics traders react to OSINT and defense news within minutes. Crypto traders watch on-chain metrics, exchange flows, and CT (Crypto Twitter). The causal chain from geo event to crypto repricing has multiple links: geo event -> oil market reaction -> risk sentiment shift -> crypto repricing. Each link adds delay. This skill sits at the intersection, reading the geo signal and trading the crypto lag before convergence. The edge persists because the two communities remain segregated and the causal chain is indirect enough that crypto traders don't watch geo markets in real time.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
