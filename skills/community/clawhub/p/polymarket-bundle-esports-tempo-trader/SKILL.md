---
name: polymarket-bundle-esports-tempo-trader
description: Trades tempo inconsistencies across Dota2 and esports game props on Polymarket. Within the same game first blood timing correlates with kill pace and Ends in Daytime implies a fast stompy game with fewer total kills while rampage and ultra kill require high kill counts. When these tempo indicators contradict each other it is a structural mispricing sized by conviction.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Esports Tempo Trader
  difficulty: advanced
---

# Bundle -- Esports Tempo Trader

> **This is a template.**
> The default signal detects tempo inconsistencies between first blood, kills O/U, daytime ending, rampage, and ultra kill props within the same Dota2/esports game -- remix it with draft data, hero pick rates, or live match feeds.
> The skill handles all the plumbing (market discovery, bundle construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Dota2 and other esports matches on Polymarket spawn multiple correlated game-level props: first blood, kills O/U, daytime ending, ultra kill, and rampage. These props collectively describe the "game tempo" -- whether the game will be fast and aggressive or slow and methodical. When tempo indicators contradict each other, one or more props are mispriced. This skill detects and trades those inconsistencies.

## Edge

Each prop within a game is priced by its own order book. Retail traders price "First Blood" and "Kills O/U 50.5" independently, but these are deeply correlated:

- **First blood high + kills low**: Early aggression strongly correlates with higher overall kill pace. If first blood is expected at 70% but kills O/U OVER is at 35%, the kills market hasn't absorbed the aggression signal.
- **Daytime ending high + kills high**: "Ends in Daytime" means the game finishes before nightfall cycles accumulate -- a fast, stompy game. Fast games end before late-game teamfights generate high kill counts. Both being high is contradictory.
- **Rampage/ultra kill high + kills low**: Multi-kill streaks (4+ kills in quick succession) mechanically require a high overall kill count. You cannot have frequent rampages in a 30-kill game.

No sportsbook would allow these contradictions, but Polymarket has no cross-prop consistency enforcement.

## Signal Logic

1. Discover active esports game props via keyword search + `get_markets(limit=200)` as primary fallback
2. Parse each question: extract match_key, game_number, prop_type (first_blood, daytime, kills_ou, rampage, ultra_kill), line_value
3. Filter non-esports markets with regex
4. Group into tempo bundles by (match_key, game_number)
5. Compute tempo score from all available props -- aggregate aggressive vs passive signals
6. Detect inconsistencies:
   - Daytime high + kills O/U high (fast game = fewer kills)
   - First blood high + kills O/U low (early aggro = more kills)
   - Rampage/ultra kill high + kills O/U low (multi-kills need high kills)
7. Trade the prop that deviates most from the tempo consensus
8. Size by conviction (inconsistency magnitude), not flat amount

### Remix Signal Ideas

- **Draft data (Dotabuff/OpenDota)**: Aggressive drafts with teamfight heroes predict higher kill totals -- feed hero composition into tempo expectations before comparing to market prices
- **Lane matchup analysis**: Volatile lane matchups (e.g., both mid heroes are gankers) predict early first blood -- use hero data to sharpen first blood expectations
- **PandaScore live feed**: Stream real-time game state during BO3 -- if Game 1 was a stomp with 60+ kills, Game 2 tempo props should shift
- **Patch meta tracking**: After Dota2 patches that buff teamfight items or nerf split-push strategies, kill totals shift systematically -- historical patch data predicts tempo direction

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
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day for live games) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_VIOLATION` | `0.04` | Min tempo inconsistency magnitude to trigger a trade |

## Edge Thesis

Dota2 game props form a "tempo bundle" where all indicators should tell a consistent story about how the game will play out. Traditional sportsbooks enforce this consistency through centralized line-setting. Polymarket has no such mechanism -- each prop is its own independent order book. Esports tempo props are especially vulnerable because:

- First blood, kills, daytime, and multi-kill props are deeply correlated but priced independently
- Retail traders specialize in one prop type (e.g., kills markets) without checking adjacent tempo indicators
- Game-specific knowledge (Dota2 day/night cycle mechanics, teamfight timing) is niche and not widely understood by general prediction market participants
- Multi-game series (BO3/BO5) create separate tempo bundles per game, multiplying the surface area for inconsistencies
- New props added mid-series don't inherit tempo context from earlier games

This skill treats each game's props as a coherent tempo system and trades the prop that deviates most from the consensus.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
