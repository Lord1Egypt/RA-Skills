---
name: polymarket-bundle-overwatch-bo3-trader
description: Trades structural arbitrage between Overwatch BO3 series winner markets and individual game winner markets on Polymarket. P(BO3 winner) must be mathematically consistent with P(Game 1 winner) and P(Game 2 winner) -- when it is not, individual game probabilities imply a different BO3 win probability than the market is pricing, creating a free edge that resolves mechanically.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Overwatch BO3 Structural Arb Trader
  difficulty: advanced
---

# Bundle -- Overwatch BO3 Structural Arb Trader

> **This is a template.**
> The default signal detects inconsistencies between Overwatch BO3 series winner markets and individual game winner markets. The skill handles all the plumbing (market parsing, match grouping, implied probability calculation, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists Overwatch match markets in bundles: a BO3 series winner market ("Overwatch: Team A vs Team B (BO3)") alongside individual game winner markets ("Game 1 Winner", "Game 2 Winner", and sometimes "Game 3 Winner"). The BO3 winner probability is **not independent** of the individual game probabilities -- it is a mathematical function of them. When the market prices these inconsistently, the gap is a structural arbitrage that resolves mechanically as the series plays out.

## Edge

The mathematical relationship is exact:

```
P(Team wins BO3) = p1*p2 + p1*(1-p2)*p3 + (1-p1)*p2*p3
```

Where p1, p2, p3 are the probabilities of the team winning Games 1, 2, and 3 respectively. If Game 3 data is unavailable, assume p3 = 0.5 (neutral).

This constraint must hold. When it does not:

1. **Retail prices markets in isolation** -- users bet on BO3 outcomes without checking individual game markets, or vice versa, causing the joint distribution to drift
2. **Resolution forces convergence** -- as each game is played, the BO3 probability must mechanically update; any mispricing is guaranteed to collapse
3. **Niche Overwatch markets have thin coverage** -- lower liquidity means fewer participants enforcing the cross-market constraint
4. **Same structural edge as CS2 maps** -- this is the same arbitrage pattern documented in CS2 map winner vs series winner markets, applied to the Overwatch ecosystem

## Signal Logic

1. Discover Overwatch markets via keyword search (`Overwatch`, `OCS`, `OWL`, `Game 1 Winner`, `Game 2 Winner`, `BO3`, `Virtus.pro`, `Team Peps`) with a `get_markets(limit=200)` fallback
2. Parse each question: extract team names, game number (for game winner markets) or BO3 tag (for series winner markets)
3. Group markets by match (canonical sorted team pair)
4. For each match with a BO3 market + Game 1 and Game 2 winner markets:
   - Compute implied BO3 probability from individual game win probabilities
   - If Game 3 winner market exists, use its probability; otherwise assume 0.5
   - Compare implied BO3 to actual BO3 market probability
5. Trade if the violation exceeds `MIN_VIOLATION` (default 5%):
   - Implied > actual + MIN_VIOLATION: BO3 underpriced -> buy YES if p <= YES_THRESHOLD
   - Implied < actual - MIN_VIOLATION: BO3 overpriced -> sell NO if p >= NO_THRESHOLD
6. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Overwatch stats API** -- pull team win rates, map pool strengths, and hero composition data to compute more accurate game-level probabilities than the market implies
- **Live match data** -- connect to OWL/OCS live feeds; when Game 1 completes, immediately recalculate the implied BO3 and trade the gap before the market fully adjusts
- **Map veto analysis** -- Overwatch map picks affect team win probability; incorporate known map pool strengths for each team to weight individual game probabilities
- **Historical BO3 consistency** -- analyse past Overwatch BO3 results to calibrate the Game 3 assumption (is 0.5 too high or too low for specific team matchups?)
- **Cross-tournament calibration** -- compare pricing consistency across OCS, OWL, and third-party tournaments to detect systematic biases in specific league markets

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
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_VIOLATION` | `0.05` | Min implied-vs-actual BO3 probability gap to trigger a trade |

## Edge Thesis

Overwatch BO3 series winner markets and individual game winner markets form a closed mathematical system. The probability of winning a best-of-3 series is a deterministic function of the probabilities of winning each individual game. When Polymarket prices these markets independently and the implied BO3 probability diverges from the actual BO3 market price, the gap is structural arbitrage. Resolution is mechanical: as each game is played, the BO3 price must converge to the value implied by game outcomes. This skill systematically detects and trades these cross-market inconsistencies.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
