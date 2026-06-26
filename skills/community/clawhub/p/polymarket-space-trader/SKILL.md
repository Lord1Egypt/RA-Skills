---
name: polymarket-space-trader
description: Trades Polymarket prediction markets on space launches, SpaceX milestones, satellite deployments, Mars missions, and commercial spaceflight outcomes. Use when you want to capture alpha on the rapidly growing space exploration market with 22% CAGR and clear binary resolution criteria.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Space & Launch Trader
  difficulty: intermediate
---

# Space & Launch Trader

> **This is a template.**  
> The default signal is keyword discovery + FAA/SpaceX launch schedule alignment — remix it with NASA launch manifest APIs, TLE (Two-Line Element) satellite tracking data, or social media sentiment from SpaceX/Blue Origin announcements.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Space prediction markets have shown $120M+ cumulative volume (2020–2025) with 22% CAGR. Polymarket currently lists 106+ active space markets. This skill trades:

- **SpaceX milestones** — Starship orbital tests, launch counts, Starlink constellation size
- **Mars missions** — NASA/private mission announcements and landing events
- **Commercial spaceflight** — Blue Origin, Virgin Galactic, Axiom Space timelines
- **Satellite & telecom** — Orbital congestion, direct-to-cell launch milestones
- **Regulatory events** — FAA approvals, international launch cadence comparisons

Key insight: volatility spikes ~25% around launch events, creating short-window entry opportunities for informed traders.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Operator Reliability Bias

1. Discover active space/launch markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `mission_bias()` multiplier based on operator track record in the question
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Mission Bias (built-in, no API required)

Retail traders apply uniform skepticism across all space markets, ignoring the vast difference in historical reliability between operators. `mission_bias()` encodes documented success rates directly into position sizing:

| Operator / Mission | Track record | Multiplier |
|---|---|---|
| Falcon 9 / Starlink deployments | ~98% mission success | **1.35x** |
| SpaceX / Crew Dragon (general) | ~95% success | **1.25x** |
| Starship (test vehicle) | Rapidly improving, ~60%+ | **1.10x** |
| Blue Origin / New Glenn | Lower cadence, less proven | 0.90x |
| NASA Artemis / SLS | Chronic delays, over-budget | 0.80x |
| Mars missions (any operator) | Retail overprice enthusiasm | 0.75x |
| Virgin Galactic | Multiple delays, financial struggles | **0.70x** |

Example: Falcon 9 launch success market at 25% → conviction 34% × 1.35x = 46% → $14 position. NASA SLS timeline market at same price → 34% × 0.80x = 27% → $8.

### Remix Ideas

- **FAA NOTAM filings**: Public Notice to Air Missions filed days ahead of launch — feed scheduled probability into p to trade divergence with market
- **Next Spaceflight / Rocket Watch**: Public launch calendars as leading probability signal
- **NASA API**: Real-time mission status and telemetry feeds
- **Satellite TLE data**: Verify actual Starlink constellation count vs market claims before milestone markets resolve

## Market Categories Tracked

```python
KEYWORDS = [
    'SpaceX', 'Starship', 'Starlink', 'Falcon 9', 'Crew Dragon',
    'launch', 'rocket', 'Mars', 'Moon', 'lunar',
    'NASA', 'Artemis', 'SLS', 'Blue Origin', 'New Glenn',
    'Virgin Galactic', 'Axiom', 'satellite', 'orbital', 'ISS',
    'FAA', 'launch window', 'ESA', 'JAXA',
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $30 USDC | Space markets have good liquidity |
| Min market volume | $2,500 | Space community is engaged |
| Max bid-ask spread | 8% | Tighter than climate markets |
| Min days to resolution | 3 | Short-window launch events are tradable |
| Max open positions | 6 | Space events cluster by launch window |

## Volatility Note

Space markets spike sharply on anomaly news. If a launch is scrubbed, NO prices spike immediately. The skill detects these via context flip-flop warnings and pauses during high-volatility windows unless edge is strong.

## Installation & Setup

```bash
clawhub install polymarket-space-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs every 10 minutes (`*/10 * * * *`). Launch events can resolve rapidly; tighter loop than other categories.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` — it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority — keep this credential private. Do not place a live-capable key in any environment where automated code could call `--live`. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `2500` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (0.08 = 8%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
