---
name: polymarket-ladder-chess-tournament-trader
description: Trades distribution-sum violations in chess tournament winner markets on Polymarket. Player winner probabilities must sum to ~100% — when the field total deviates beyond threshold, individual player markets are structurally mispriced.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Ladder Chess Tournament Distribution Trader
  difficulty: advanced
---

# Ladder — Chess Tournament Distribution Trader

> **This is a template.**
> The default signal is distribution-sum consistency checking across chess tournament winner markets — remix it with Elo rating feeds, tournament bracket analysis, or live game evaluation engines.
> The skill handles all the plumbing (market discovery, tournament grouping, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists winner-takes-all chess tournament markets where each player has a separate "Will X win?" contract:

- **FIDE Candidates Tournament**: "Will Gukesh win the Candidates?", "Will Caruana win?", "Will Nakamura win?"
- **Chess World Championship**: "Will Carlsen win the World Championship?", "Will Ding Liren win?"
- **Any tournament**: The skill discovers chess tournament markets dynamically via keyword search and broad market scanning

These markets form a probability distribution. Exactly one player wins, so the individual winner probabilities **must** sum to approximately 100%. When retail trades these markets in isolation, the sum drifts — and that is the edge.

## The Edge: Distribution Sum Arbitrage

In a winner-takes-all tournament with N players, the mathematical constraint is:

P(player 1 wins) + P(player 2 wins) + ... + P(player N wins) = 100%

When the sum deviates, the field is structurally mispriced:

- **Sum > 105%**: Players are collectively overpriced. Sell NO on the highest-probability players to capture the reversion.
- **Sum < 95%**: Players are collectively underpriced. Buy YES on the lowest-probability players to capture the reversion.

### Example

| Player Market | Probability |
|---------------|-------------|
| Gukesh wins | 35% |
| Caruana wins | 25% |
| Nakamura wins | 20% |
| Praggnanandhaa wins | 15% |
| Firouzja wins | 12% |
| **Sum** | **107%** |

Violation: sum = 107% > 100%. The field is overpriced by 7%. Trade: sell NO on the highest-probability players (Gukesh, Caruana) where the threshold gate is satisfied, sizing by conviction.

## Why This Works

1. **Retail trades in silos** — users bet on their favourite player without cross-referencing the full field, causing the sum to drift from 100%
2. **Distribution constraints are structural** — exactly one player wins; this is a mathematical fact, not an opinion
3. **Resolution forces convergence** — as the tournament progresses and players are eliminated, the market must price consistently or create guaranteed arbitrage
4. **Niche chess markets have thin coverage** — lower liquidity means fewer market makers enforcing the constraint, so mispricings persist longer

## Signal Logic

1. Discover chess tournament winner markets via keyword search (FIDE, Candidates, chess, championship, grandmaster, GM) with a broad market scan fallback
2. Parse each question: extract player name, tournament name, and event type
3. Group markets by tournament name to form complete player distributions
4. Sum player probabilities per tournament and check for deviations beyond the `MIN_VIOLATION` threshold (default 5%)
5. Identify which side of the distribution is mispriced (overpriced sum vs. underpriced sum)
6. Trade only opportunities that pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (threshold distance + violation magnitude), not flat amount

### Remix Signal Ideas

- **Elo ratings API** — pull live FIDE Elo ratings and compute expected win probabilities via a Bradley-Terry model; trade when the market diverges from Elo-implied odds
- **Tournament bracket analysis** — model the remaining bracket structure (Swiss system, knockout rounds) to compute exact elimination probabilities for each player
- **Historical chess databases** — analyse head-to-head records between specific players at classical/rapid/blitz time controls to identify mispriced matchup markets
- **Live game analysis** — connect a chess engine (Stockfish/Leela) to monitor ongoing games; update tournament win probabilities in real time as games progress
- **Form and fatigue signals** — track recent tournament results, rest days, and travel schedules to adjust short-term win probability estimates

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
| `SIMMER_MAX_SPREAD` | `0.06` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_VIOLATION` | `0.05` | Min distribution-sum deviation to trigger a trade |

## Edge Thesis

Chess tournament winner markets are not independent coin flips. They form a closed probability distribution: exactly one player wins, so the individual winner probabilities must sum to 100%. Prediction markets price each player independently, but the joint distribution must be internally consistent.

When it is not, the inconsistency is a free edge. This skill systematically detects and trades these distribution-sum violations, acting as an automated consistency enforcer for chess tournament prediction markets.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
