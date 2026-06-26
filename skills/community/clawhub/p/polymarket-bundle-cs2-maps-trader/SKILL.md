---
name: polymarket-bundle-cs2-maps-trader
description: Trades CS2 BO3 Winner markets when individual map winner probabilities imply a different BO3 outcome on Polymarket. Uses the binomial BO3 model to calculate implied win probability from Map 1, Map 2, and Map 3 prices, then trades the BO3 market when it diverges beyond a minimum violation threshold. Conviction-based sizing scales with the magnitude of the map-vs-BO3 disagreement.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle CS2 Maps BO3 Arbitrage Trader
  difficulty: advanced
---

# Bundle -- CS2 Maps BO3 Arbitrage Trader

> **This is a template.**
> The default signal detects inconsistencies between individual CS2 map winner probabilities and the BO3 match winner market -- remix it with team Elo ratings, map pool veto data, or live scoreboard feeds.
> The skill handles all the plumbing (market discovery, bundle construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

CS2 matches on Polymarket list separate markets for each map winner and the overall BO3 winner:

- "Counter-Strike: NAVI vs FaZe - Map 1 Winner" = 55% (NAVI)
- "Counter-Strike: NAVI vs FaZe - Map 2 Winner" = 60% (NAVI)
- "Counter-Strike: NAVI vs FaZe - Map 3 Winner" = 50% (NAVI)
- "Counter-Strike: NAVI vs FaZe (BO3) - IEM Katowice" = 58% (NAVI)

The individual map probabilities **constrain** the BO3 probability via the binomial model. When they don't match, the BO3 market is mispriced.

## Edge

P(BO3 win) must equal P(win M1)*P(win M2) + P(win M1)*P(lose M2)*P(win M3) + P(lose M1)*P(win M2)*P(win M3). Retail traders price the BO3 market independently from individual maps, creating structural mispricings that this skill exploits.

## Signal Logic

1. Discover CS2 markets via get_markets(limit=200) as primary + keyword search fallback
2. Parse each question: extract (match_key, map_number, team_a, team_b) for map winners
3. Parse BO3 winner markets: extract (match_key, team_a, team_b)
4. Group into match bundles: one BO3 market + its individual map markets
5. For each bundle with at least Map 1 + Map 2 + BO3 winner:
   - Calculate implied BO3 probability from map probabilities (binomial model)
   - If Map 3 market exists, use its probability; otherwise assume 0.5
   - Compare implied vs actual BO3 market probability
   - If difference > MIN_VIOLATION: trade the BO3 market toward map-implied probability
6. Size by conviction (CLAUDE.md formula), not flat amount

### Remix Signal Ideas

- **HLTV Elo ratings**: Pull team ratings and recent head-to-head records -- teams with map pool advantages create asymmetric Map 3 probabilities that the default 0.5 assumption misses
- **Map veto prediction**: Use historical veto patterns to predict which maps will be played -- if a team always bans Inferno, the Map 3 probability on Inferno should be different from Mirage
- **Live scoreboard data (PandaScore API)**: Stream real-time round scores during Map 1 -- if one team is dominating, Map 2 and BO3 probabilities should shift before the market adjusts
- **Map-specific win rates**: Fetch team win rates on specific maps from HLTV -- if FaZe has 70% win rate on Nuke but the market prices Map 2 at 55%, that is an additional edge layer

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
| `SIMMER_MIN_VIOLATION` | `0.05` | Min implied-vs-actual BO3 probability difference to trade |

## Edge Thesis

Traditional sportsbooks employ quantitative models that enforce consistency between individual game prices and series prices. Polymarket has no such mechanism -- each market is priced by its own order book. CS2 BO3 markets are particularly vulnerable because:

- Individual map markets attract map-specific bettors who don't consider the BO3 implication
- BO3 markets attract series-level bettors who don't decompose into individual maps
- Map 3 probability is often unknown or assumed at 50%, creating systematic errors
- Live match flow on Map 1 shifts map probabilities before the BO3 market adjusts
- Tournament format changes (upper/lower bracket) affect team motivation asymmetrically across maps
- The binomial constraint is mathematical -- map probabilities must sum correctly to produce the BO3 probability

This skill treats the map winner probabilities as inputs to a binomial model and trades the BO3 market when it diverges from the model's output.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
