---
name: polymarket-bundle-dota2-bo3-trader
description: Trades structural inconsistencies between Dota 2 BO3 winner, individual game winners, and game handicap markets on Polymarket. P(BO3 win) must equal f(P(Game1), P(Game2), P(Game3)) and P(handicap -1.5) must equal P(win both games). When these constraints are violated, it is structural arbitrage sized by conviction.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Dota 2 BO3 Structure Trader
  difficulty: advanced
---

# Bundle -- Dota 2 BO3 Structure Trader

> **This is a template.**
> The default signal is structural inconsistency detection between BO3 winner, game winner, and handicap markets -- remix it with Elo ratings, draft data, or live match feeds.
> The skill handles all the plumbing (market discovery, match grouping, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Dota 2 BO3 matches spawn multiple related markets on Polymarket: the overall BO3 winner, individual Game 1/2/3 winners, and game handicap lines (-1.5 / +1.5). These markets must be structurally consistent -- the BO3 win probability is a mathematical function of the individual game probabilities. When they diverge, it is pure structural arbitrage.

Example: If P(Team A wins Game 1) = 60% and P(Team A wins Game 2) = 55%, then P(Team A wins BO3) should be approximately 70%. If the BO3 market prices Team A at 55%, it is underpriced by 15%.

## Edge

Each market in a Dota 2 BO3 bundle is priced by its own independent order book. Retail participants trade each market in isolation -- they bet on "Team A wins Game 1" without considering how that price constrains the BO3 winner or handicap markets. Professional sportsbooks enforce consistency across related lines; Polymarket does not. The result is persistent structural inconsistencies between mathematically linked markets.

## Signal Logic

1. Discover active Dota 2 markets via keyword search + `get_markets(limit=200)` as primary fallback
2. Parse each question to extract:
   - "Dota 2: Team A vs Team B - Game N Winner" -> (match_key, game_number)
   - "Dota 2: Team A vs Team B (BO3)" -> (match_key, bo3_winner)
   - "Game Handicap: Team A (-1.5) vs Team B (+1.5)" -> (match_key, handicap_team, handicap_value)
3. Group by match_key
4. For each match with BO3 + game winners:
   - Calculate implied BO3 from game probabilities: `P(BO3) = P(G1)*P(G2) + P(G1)*(1-P(G2))*P(G3) + (1-P(G1))*P(G2)*P(G3)`
   - Compare implied BO3 to market BO3 price
   - Check handicap consistency: `P(handicap -1.5 covers) ~ P(G1) * P(G2)` (must win both games for 2-0)
5. Trade inconsistencies exceeding `SIMMER_MIN_INCONSISTENCY` (default 8%)
6. Size by conviction (inconsistency magnitude), not flat amount

### Remix Signal Ideas

- **OpenDota API**: Pull team Elo ratings and recent match history -- compare Elo-implied game win probabilities to market prices for an additional edge layer
- **Draft-phase data**: Dota 2 drafts dramatically affect game-level win probability -- if a team drafts a late-game composition, their Game 1 probability drops but Game 3 rises, creating systematic mispricing in early-game markets
- **PandaScore live feed**: Stream real-time match data during a BO3 -- after Game 1 result is known, Game 2/3 and BO3 markets should adjust instantly but often lag by minutes
- **Hero win rate data**: Cross-reference the drafted heroes against Dotabuff/OpenDota hero win rates for the current patch to estimate game-level probabilities more accurately than market prices reflect

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
| `SIMMER_MIN_INCONSISTENCY` | `0.08` | Min structural inconsistency to trigger a trade |

## Edge Thesis

Professional sportsbooks employ line-setters who enforce mathematical consistency across BO3 winner, game winner, and handicap lines for the same match. Polymarket has no such mechanism -- each market is an independent order book. Dota 2 BO3 markets are particularly vulnerable because:

- Three game winner markets plus BO3 winner plus handicap lines create 5+ related markets per match
- Each market attracts different participants (BO3 bettors vs game-level bettors vs handicap traders)
- Directional flow on one market (e.g., big bet on Game 1 winner) does not propagate to the BO3 or handicap markets
- Draft-phase information affects game-level probabilities asymmetrically but BO3 markets don't adjust
- Tournament context (elimination vs group stage) changes how teams approach individual games vs the series
- After Game 1 result, the conditional probabilities shift dramatically but market repricing is slow

This skill enforces the structural constraint P(BO3) = f(P(G1), P(G2), P(G3)) and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
