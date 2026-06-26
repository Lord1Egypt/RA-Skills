---
name: polymarket-macro-risk-regime-trader
description: Detects macro risk regimes (risk-on vs risk-off) by scanning ALL Polymarket categories simultaneously. When crypto drops, geopolitical escalation rises, and commodity stress increases, the regime is risk-off. Trades markets in other categories that have not repriced to the new regime yet.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Macro Risk Regime Trader
  difficulty: advanced
---

# Macro Risk Regime Trader

> **This is a template.**
> The default signal classifies all markets into categories, computes cross-category sentiment scores, and trades lagging markets that haven't repriced to the detected regime -- remix it with VIX data, treasury yields, or funding rates.
> The skill handles all the plumbing (market discovery, category classification, regime detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Markets across Polymarket are interconnected but reprice at different speeds. When a macro shock hits (war escalation, oil spike, crypto crash), the directly affected categories move first while markets in other categories lag behind. This skill reads the "regime" from three indicator categories -- crypto, geopolitics, and commodities -- and then trades markets in OTHER categories that are still priced for the old regime.

## Edge

Cross-category regime detection captures repricing lag that single-category skills miss:

1. **Multi-signal confirmation** -- A single category moving could be noise; three categories moving in the same risk direction is a macro regime shift
2. **Repricing lag** -- When crypto drops 10% and geopolitical risk spikes, sports and weather markets that are tangentially affected take hours to reprice
3. **Retail compartmentalization** -- Polymarket traders specialize in categories; a crypto trader may not watch geopolitical markets and vice versa, creating cross-category information gaps
4. **Regime persistence** -- Once a risk-off regime is established, it tends to persist for days, giving lagging markets time to converge

## Signal Logic

1. Discover ALL active markets via `get_markets(limit=200)` (primary) + keyword `find_markets()` (supplement)
2. Classify each market into a category: crypto, geopolitics, commodity, sports, weather, other
3. Compute category sentiment scores:
   - **crypto_score**: average probability of BTC/ETH "Up or Down" markets (>0.5 = bullish)
   - **geo_risk_score**: average probability of escalation markets (higher = more risk)
   - **commodity_stress**: average probability of oil/commodity threshold markets (higher = more stress)
4. Determine regime:
   - **RISK-OFF**: crypto_score < 0.45 AND geo_risk > 0.60 AND commodity_stress > 0.50
   - **RISK-ON**: crypto_score > 0.55 AND geo_risk < 0.40
   - **NEUTRAL**: mixed signals -- no trades
5. In risk-off: find non-driving-category markets at YES >= 62% that should be lower -- sell NO
6. In risk-on: find non-driving-category markets at YES <= 38% that should be higher -- buy YES
7. Conviction scales with distance from threshold; size = `max(MIN_TRADE, conviction * MAX_POSITION)`

### Remix Signal Ideas

- **VIX overlay**: Wire real-time VIX index into regime detection -- VIX > 25 confirms risk-off even if Polymarket categories are ambiguous
- **Treasury yield curve**: Inverted yield curve + risk-off regime = stronger conviction on downside trades
- **Funding rate divergence**: If crypto perpetual funding rates are deeply negative while Polymarket crypto markets haven't fully repriced, conviction increases
- **Regime transition speed**: Track how fast the regime shifted -- a sudden regime change (within 2 hours) creates larger repricing gaps than a gradual one

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
| `SIMMER_REGIME_CRYPTO_THRESHOLD` | `0.45` | Crypto score below this = bearish signal for regime |
| `SIMMER_REGIME_GEO_THRESHOLD` | `0.60` | Geo risk score above this = elevated risk signal |
| `SIMMER_REGIME_COMMODITY_THRESHOLD` | `0.50` | Commodity stress above this = stress signal |

## Edge Thesis

Polymarket categories are siloed by trader specialization. Crypto traders watch crypto, geopolitics traders watch conflict markets, but very few traders monitor ALL categories simultaneously. When a macro regime shift occurs -- crypto drops, geopolitical escalation rises, commodities stress -- the directly affected categories reprice within minutes. But markets in other categories (sports, weather, elections) that have subtle correlations to macro risk take hours or days to adjust. This skill acts as a cross-category radar, detecting the regime from the fast-moving indicator categories and trading the slow-moving laggards before they converge. The edge is structural: as long as Polymarket traders remain category-specialized, cross-category repricing lag will persist.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
