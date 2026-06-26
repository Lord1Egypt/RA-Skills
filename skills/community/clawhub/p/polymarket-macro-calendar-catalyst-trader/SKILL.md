---
name: polymarket-macro-calendar-catalyst-trader
description: Trades Polymarket prediction markets that resolve near known calendar catalyst events (FOMC meetings, major tournament finals, geopolitical summits, crypto halvings, space launches). Markets near 50% resolving during catalyst windows are underpriced for movement -- Polymarket prices direction, not volatility. These coiled springs will move sharply, and macro analysis provides directional signal.
metadata:
  author: snetripp
  version: "1.0"
  displayName: Calendar Catalyst Trader
  difficulty: advanced
---

# Calendar Catalyst Trader

> **This is a template.**
> The default signal matches market resolution dates to a calendar of known catalyst events and trades coiled springs (markets near 50%) with boosted conviction when a directional hint exists from macro analysis.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Known calendar events create predictable volatility windows. FOMC meetings happen on a fixed 6-week cycle. The Super Bowl, NBA Finals, World Cup, and Wimbledon have known dates months in advance. Geopolitical summits (G7, UN General Assembly, COP) and crypto events (halvings, protocol upgrades) are scheduled well ahead. Markets that resolve during or shortly after these events WILL move sharply -- but Polymarket prices direction, not volatility.

The structural edge: a market sitting at 50% that resolves the day after an FOMC meeting is a coiled spring. The Fed will either cut, hold, or hike -- and the market will snap to 20% or 80% in hours. The expected move is huge, but the market price doesn't reflect that. Similarly, a "Will Team X win the championship?" market at 48% the day before the final is about to move to either ~5% or ~95%. The 48% price is correct in expectation but massively underpriced for the magnitude of movement.

Why this works:
- Calendar events are public knowledge, but resolution-date proximity to catalysts is not priced as a factor
- Markets near 50% have maximum convexity -- any directional signal produces outsized returns
- Catalyst categories carry macro directional hints (crypto events historically bullish, geopolitical summits often disappoint, sports finals confirm favorites)
- The CATALYST_BOOST multiplier (default 1.25x) converts this timing edge into larger position sizes

## Signal Logic

### Default Signal: Catalyst Window Detection

1. Scan ALL active markets via `get_markets(limit=200)` plus targeted keyword search
2. For each market, check if its resolution date falls within `SIMMER_CATALYST_WINDOW` days (default 3) of any known catalyst event
3. Fallback: match market question text to catalyst categories via keyword matching
4. For catalyst-adjacent markets:
   - **Coiled springs** (price between 0.40-0.60): use macro directional hint from catalyst category, apply CATALYST_BOOST to conviction
   - **Standard threshold** (below YES_THRESHOLD or above NO_THRESHOLD): apply CATALYST_BOOST to standard conviction
   - **Coiled + no direction hint** (e.g., FOMC): skip -- genuinely uncertain direction

### Catalyst Calendar

| Category | Events | Directional Hint |
|---|---|---|
| **FOMC** | 8 meetings/year on fixed 6-week cycle | None (genuinely uncertain) |
| **Sports** | Super Bowl, NBA Finals, World Cup, Wimbledon, US Open, World Series | YES (favorites tend to be confirmed) |
| **Geopolitical** | G7, UN General Assembly, COP climate summit, US elections | NO (summits often disappoint, status quo persists) |
| **Crypto** | Bitcoin halving cycle milestones, Ethereum upgrades | YES (historically bullish events) |
| **Space** | SpaceX Starship, Artemis launches | YES (modern launch success >95%) |

### Coiled Spring Logic

Markets between 40-60% resolving within the catalyst window are "coiled springs":
- They WILL move sharply in one direction
- Even a weak directional signal is valuable at these prices
- The CATALYST_BOOST multiplier (default 1.25x) increases position size
- Proximity factor: closer to catalyst = stronger boost

### Why Directional Hints Work

- **Sports YES**: Championship finals disproportionately confirm the higher-seeded/favored team. The 48% market for the favorite is slightly underpriced.
- **Geopolitical NO**: Peace summits, climate agreements, and diplomatic deadlines more often fail than succeed. Markets at 55% for "will agreement be reached" are slightly overpriced.
- **Crypto YES**: Every major crypto catalyst (halvings, ETF approvals, protocol upgrades) has historically been followed by price appreciation. Markets pricing crypto milestones near 50% tend to resolve YES.
- **Space YES**: SpaceX has a >97% success rate on Falcon 9. Starship is improving rapidly. Markets near 50% for "successful launch" are underpriced.
- **FOMC None**: Fed decisions are genuinely uncertain. No directional hint -- we skip coiled springs for FOMC but still trade markets outside the threshold bands.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` -- nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_CATALYST_WINDOW` | `3` | Days window around catalyst events |
| `SIMMER_CATALYST_BOOST` | `1.25` | Conviction boost multiplier for catalyst-adjacent markets |
| `SIMMER_COIL_LOW` | `0.40` | Coiled spring lower bound |
| `SIMMER_COIL_HIGH` | `0.60` | Coiled spring upper bound |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
