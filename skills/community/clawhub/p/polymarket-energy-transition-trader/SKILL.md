---
name: polymarket-energy-transition-trader
description: Trades Polymarket prediction markets on EV adoption milestones, solar/wind capacity, nuclear energy restarts, oil price thresholds, and energy policy events. Use when you want to capture alpha on the energy transition using IEA data calendar timing, OPEC meeting windows, and technology tier confidence signals.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Energy Transition Trader
  difficulty: intermediate
---

# Energy Transition Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `transition_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Energy transition markets mix slow-moving structural trends with sharp data-driven catalysts. Retail traders consistently misprice two things: (1) they ignore the energy data calendar, where professional markets reprice on known release dates and Polymarket lags by days, and (2) they treat all energy sub-sectors as equally uncertain when nuclear regulatory timelines, OPEC cut patterns, and renewable pipeline data have very different predictability levels.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Energy Transition Bias

1. Discover active energy and transition markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `transition_bias()` — combines energy data calendar timing with technology tier confidence
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Transition Bias (built-in, no API required)

Two compounding structural edges:

**Factor 1 — Energy Data Calendar Timing**

Each energy sub-sector has a known annual data release rhythm where professional traders have better reads than retail:

| Condition | Multiplier | Rationale |
|---|---|---|
| EV question + Q1 (Jan–Mar) | **1.20x** | IEA/BloombergNEF publish prior-year sales totals — biggest data drop of the year |
| Solar/wind question + Q4 (Oct–Dec) | **1.20x** | Year-end installation rush — projects complete before Dec 31, IEA confirms GW additions |
| Oil/OPEC question + OPEC meeting months (Jun, Dec) | **1.15x** | Biannual ministerial meetings — pre-meeting uncertainty is highest |
| Gas/LNG question + winter peak (Nov–Feb) | **1.10x** | Northern hemisphere demand and storage drawdown window |
| Off-cycle | **1.00x** | No timing amplification |

**Factor 2 — Technology Tier Confidence**

| Technology type | Multiplier | Why |
|---|---|---|
| Nuclear restart / SMR approval | **1.25x** | Regulatory timelines are public filings — US retail is poorly informed on EU/Asian nuclear policy |
| OPEC production cut / oil supply | **1.20x** | OPEC+ has surprised with cuts 70%+ of the time since 2022 — retail consistently underprices |
| Solar / wind GW capacity milestones | **1.20x** | IEA and IRENA publish confirmed project pipelines — markets underprice published data |
| EV adoption / market share / sales | **1.15x** | IEA monthly data lags Polymarket pricing by 1–2 months; BYD data leads further |
| Oil price threshold (Brent / WTI) | **1.10x** | OPEC+ directional bias documented, but daily volatility adds noise |
| Natural gas / LNG | **1.10x** | EIA weekly storage data is public — seasonal demand patterns predictable |
| Carbon / net zero policy pledges | **0.80x** | Government pledges rarely resolve cleanly — ambiguous criteria, retail overprices sincerity |
| Hydrogen / green hydrogen milestones | **0.75x** | Perennial "5 years away" technology — retail consistently overprices milestones that slip |

Combined and capped at **1.40x**. A solar capacity question in Q4 → 1.20 × 1.20 = **1.40x cap** — maximum conviction. A hydrogen milestone at any time → **0.75x** — trade very conservatively.

### Keywords Monitored

```
electric vehicle, EV, Tesla, BYD, charging station, solar, wind energy,
renewable, nuclear, uranium, oil price, Brent crude, OPEC, energy transition,
battery, grid, power plant, carbon, net zero, IEA, offshore wind, hydrogen,
natural gas, LNG, pipeline, energy storage, gigawatt, capacity, reactor, SMR,
EV adoption, EV sales, energy policy, carbon capture
```

### Remix Signal Ideas

- **IEA EV monthly data**: Replace `market.current_probability` with IEA monthly EV sales trajectory to trade the divergence between published data and Polymarket retail pricing
- **EIA weekly petroleum report**: Oil storage changes as leading indicator for oil price threshold markets — published every Wednesday
- **IRENA capacity statistics**: Confirmed project pipelines lead "will X GW be installed" market pricing by months
- **OPEC press releases**: OPEC+ extraordinary meeting announcements — immediate repricing opportunity on oil markets


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `7` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
