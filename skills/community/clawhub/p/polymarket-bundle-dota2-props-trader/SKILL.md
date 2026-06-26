---
name: polymarket-bundle-dota2-props-trader
description: Trades bundle inconsistencies across correlated Dota 2 match props on Polymarket. A single match spawns 28+ prop markets (kills O/U, roshan, barracks, rampage, first blood, ultra kill, daytime) that are fundamentally correlated -- high-kill games have more roshan fights, more barracks destroyed, more rampages. When one prop implies high action but another implies low, this skill detects the inconsistency and trades the outlier toward the action-score consensus. Conviction scales with inconsistency magnitude.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Dota 2 Props Trader
  difficulty: advanced
---

# Bundle Dota 2 Props Trader

> **This is a template.**
> The default signal detects action-score inconsistencies across correlated Dota 2 match props -- remix it with OpenDota API data, hero draft analysis, or live match feeds.
> The skill handles all the plumbing (market discovery, prop parsing, bundle grouping, inconsistency detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

A single Dota 2 match on Polymarket spawns 28+ prop markets:

- "Total Kills Over/Under 47.5" = 58%
- "Total Kills Over/Under 50.5" = 52%
- "Both Teams Beat Roshan?" = 30%
- "Will Any Barracks Be Destroyed?" = 45%
- "Will There Be a Rampage?" = 15%
- "First Blood Before 3:00?" = 62%
- "Will There Be an Ultra Kill?" = 22%
- "Will the Game End in Daytime?" = 40%

These props are fundamentally **correlated**. High-kill games feature more teamfights, which means more roshan contests, more barracks pushes, more multi-kill sprees. When the kills O/U market implies a high-action game but another prop implies low action, the bundle is internally inconsistent -- and one of them is wrong.

## Edge

Polymarket prices each prop in isolation via its own order book. There is no mechanism to enforce cross-prop consistency the way a professional sportsbook would. This creates systematic mispricings:

1. **Correlated props priced independently** -- Retail traders bet on "Roshan?" without checking what the kills market implies about game action level
2. **Action-score anchor** -- The kills O/U market is the most liquid and best-priced prop; it serves as a reliable anchor for what kind of game to expect
3. **Thin liquidity on exotic props** -- Rampage, ultra kill, and daytime markets have much less volume, making them more prone to mispricing
4. **Multi-game series multiply opportunities** -- BO3 matches have separate prop bundles for Game 1, Game 2, and Game 3, tripling the surface area

## Signal Logic

1. Discover active Dota 2 prop markets via `get_markets(limit=200)` as primary discovery (Dota markets often missed by `find_markets`) + keyword search supplement
2. Parse each question to extract: match_key, game_number, prop_type, prop_value
3. Prop types recognized: `kills_ou` (with threshold), `roshan`, `barracks`, `rampage`, `first_blood`, `ultra_kill`, `daytime`
4. Group by (match_key, game_number) into bundles
5. Compute **action score** from kills O/U markets (weighted average, higher thresholds weighted more)
6. For each boolean prop, compute expected probability given the action score:
   - High-action props (roshan, barracks, rampage, ultra_kill, first_blood): should be HIGH when action score is HIGH
   - Low-action props (daytime): should be LOW when action score is HIGH (high-action games extend into night phases)
7. Trade props where actual probability diverges from expected by more than `MIN_INCONSISTENCY` (default 10%)
8. Conviction scales with inconsistency magnitude (30% gap = full conviction)

### Remix Signal Ideas

- **OpenDota API**: Pull hero picks for the match draft -- teamfight-heavy drafts (Enigma, Magnus, Tidehunter) predict higher kill totals and more action; split-push drafts (Nature's Prophet, Tinker) predict lower kills but faster barracks destruction
- **Team aggression profiles**: Some teams (e.g. Spirit, Tundra) historically play high-kill games averaging 55+ kills/game; others (e.g. Gaimin Gladiators) play disciplined low-kill styles averaging 40-45 kills. Weight the action score by team identity
- **Patch meta analysis**: Major Dota patches shift average game length and kill totals. After 7.36 (teamfight meta), average kills jumped 15%; after 7.35 (laning meta), they dropped 10%. Track patch timing to adjust the action-score baseline
- **Live kill feed**: During a BO3, if Game 1 had 65 kills, Game 2 and Game 3 action expectations should shift upward -- the teams are in an aggressive mood. Wire in live Game 1 results to adjust Game 2/3 prop expectations
- **Cross-match consistency**: If two different matches from the same tournament have wildly different roshan probabilities despite similar team skill levels, one is likely mispriced

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
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_INCONSISTENCY` | `0.10` | Min action-score inconsistency to trigger a trade |

## Edge Thesis

Professional sportsbooks employ traders who ensure cross-prop consistency: if the kills line moves, the roshan and barracks lines adjust automatically. Polymarket has no such mechanism. Each prop market is its own independent order book with its own participants, most of whom are betting on a single prop without considering the bundle. This creates persistent, exploitable inconsistencies that reform every time a new Dota 2 match is listed. The skill treats the kills O/U probability as the action-score anchor (most liquid, best-priced) and trades the outlier props back toward consistency.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
