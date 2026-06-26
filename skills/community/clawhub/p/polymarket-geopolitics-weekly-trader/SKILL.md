---
name: polymarket-geopolitics-weekly-trader
description: Trades weekly cyclical patterns in geopolitical prediction markets. Military operations spike Mon-Thu, diplomacy clusters around working days, and weekend staleness creates Monday repricing opportunities. Combines day-of-week timing with conviction-based sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Geopolitics Weekly Pattern Trader
  difficulty: advanced
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Geopolitics Weekly Pattern Trader

> **This is a template.**
> The default signal is keyword-based geopolitical market discovery combined with conviction-based sizing and `weekly_pattern_multiplier()` — four weekly cycle factors, no external API required.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Geopolitical news flow follows predictable weekly cycles. Military operations and official statements spike Monday through Thursday during government working hours. Diplomatic announcements — UN sessions, G7/G20 summits, bilateral talks — cluster around Tuesday through Thursday. Weekends see reduced news flow from both Western and non-Western governments, leaving Polymarket prices stale and ripe for Monday repricing.

Polymarket's US-dominated retail base amplifies this pattern: US traders are least active Saturday-Sunday, meaning Friday evening and weekend news breaks sit unpriced for 24-48 hours. Monday mornings bring a wave of repricing as Asian and European news from the weekend flows into the US market open.

This skill exploits four distinct weekly windows:

1. **Weekend Staleness** — Reduced US retail attention on Saturday/Sunday means news isn't fully absorbed. Moderate-probability geopolitical markets (20-40% or 60-80%) are most likely to reprice Monday.

2. **Monday Repricing** — The sharpest window. Weekend events get priced in during Monday 00:00-14:00 UTC as Asian, European, and US sessions open sequentially. Early Monday conviction boost: 1.25x.

3. **Friday Afternoon Unwinding** — Traders reduce risk before the weekend, creating temporary price dislocations as positions are closed. Friday 18:00+ UTC conviction boost: 1.10x.

4. **Midweek Diplomatic Calendar** — UN sessions, G7/G20 meetings, and diplomatic summits cluster Tuesday through Thursday. Markets tagged with diplomatic keywords are more actionable midweek. Tue-Thu diplomatic boost: 1.10x.

## Edge Thesis

The weekly cycle effect in prediction markets is well-documented:

- **Weekend staleness**: US retail dominance on Polymarket means weekday-heavy activity. Friday evening through Sunday sees reduced volume and slower price discovery. News that breaks outside US hours (Asian military operations, European diplomatic announcements) sits unpriced until Monday.

- **Institutional absence**: Unlike equity markets with 24/5 institutional desks, Polymarket has no market makers obligated to maintain fair pricing over weekends. This creates systematic staleness that the Monday session corrects.

- **Geopolitical news cadence**: Government press conferences, UN votes, and military briefings follow working-day schedules. The news cycle itself is cyclical, and markets that depend on government actions are most affected.

- **Position unwinding**: Friday afternoon risk reduction is a cross-asset phenomenon. On Polymarket, it manifests as price drift away from fair value as traders close positions ahead of weekend uncertainty.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Weekly Pattern Multiplier

1. Discover active geopolitical markets via keyword search
2. Gate: must match geopolitics regex filter (war, ceasefire, military, sanctions, NATO, etc.)
3. Gate: spread, days-to-resolution checks
4. Compute base conviction from distance to YES_THRESHOLD / NO_THRESHOLD bands
5. Apply `weekly_pattern_multiplier()` based on current day/hour UTC and market type
6. Final conviction = `min(1.0, base_conviction * weekly_multiplier)`
7. Size = `max(MIN_TRADE, round(conviction * MAX_POSITION, 2))`

### Weekly Pattern Multiplier (built-in, no API required)

| Day / Time (UTC) | Multiplier | Why |
|---|---|---|
| Saturday-Sunday (all day) | **1.15x** | Weekend staleness: US retail absent, news unpriced |
| Monday 00:00-14:00 UTC | **1.25x** | Monday repricing: weekend events flow into market open |
| Monday 14:00+ UTC | **1.05x** | Repricing fading, most adjustment done |
| Friday 18:00+ UTC | **1.10x** | Position unwinding: pre-weekend risk reduction creates dislocations |
| Friday before 18:00 UTC | **1.00x** | Normal trading session |
| Tue-Thu (diplomatic markets) | **1.10x** | Diplomatic calendar: UN, G7/G20, summits cluster midweek |
| Tue-Thu (non-diplomatic) | **1.00x** | Baseline — no weekly pattern edge |

### How Sizing Works at Different Probability Levels

With defaults (YES_THRESHOLD=0.38, MIN_TRADE=$5, MAX_POSITION=$40, Monday AM multiplier=1.25x):

| Market price p | Base conviction | Weekly conviction | Size |
|---|---|---|---|
| 38% (at threshold) | 0% | 0% | $5 (floor) |
| 30% | 21% | 26% | $11 |
| 20% | 47% | 59% | $24 |
| 10% | 74% | 92% | $37 |
| 0% | 100% | 100% capped | $40 |

Weekend multiplier (1.15x) at same levels:

| Market price p | Base conviction | Weekly conviction | Size |
|---|---|---|---|
| 30% | 21% | 24% | $10 |
| 20% | 47% | 54% | $22 |
| 10% | 74% | 85% | $34 |

### Keywords Monitored

```
war, ceasefire, military, strike, Iran, Israel, Gaza, Lebanon,
sanctions, nuclear, troops, conflict, diplomacy, NATO, Ukraine,
Russia, China, Taiwan, meeting, summit, peace
```

### Geopolitics Filter

Regex-based filter ensures only genuine geopolitical markets are traded. Prevents false positives from non-geopolitical uses of keywords (e.g., "labour strike", "lightning strike", "nuclear energy stock").

### Remix Signal Ideas

- **News API velocity by day-of-week**: Wire GDELT or MediaCloud event counts by day into `weekly_pattern_multiplier()` — when actual Monday news volume exceeds the weekly baseline by >2 standard deviations, the repricing window is even sharper; dynamically scale the Monday multiplier up to 1.40x
- **Diplomatic calendar feeds**: Pull UN General Assembly schedule, G7/G20 summit dates, and bilateral meeting announcements from official APIs — boost midweek diplomatic multiplier to 1.20x on days with confirmed high-level meetings; reduce to 1.00x on empty calendar days
- **Weekend volume anomaly detection**: Track Polymarket volume by hour-of-week for geopolitical markets — when weekend volume drops below the 20th percentile of its historical range, the staleness premium is highest; dynamically scale the weekend multiplier
- **Cross-timezone news flow**: Wire Reuters/AP breaking news timestamps — when a story breaks during Asian hours (00:00-08:00 UTC) about a European/ME conflict, the repricing lag is longest; boost to 1.30x for these cross-timezone mismatches

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
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `15000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
