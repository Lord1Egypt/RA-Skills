---
name: polymarket-geopolitics-trader
description: Trades Polymarket prediction markets on geopolitical events — wars, ceasefires, sanctions, diplomatic breakthroughs, and regime changes. Use when you want to capture alpha on international relations markets using fear-premium correction and regional news timezone windows.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Geopolitics & Conflict Trader
  difficulty: advanced
---

# Geopolitics & Conflict Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `geopolitics_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Geopolitical markets are systematically mispriced by retail traders in two ways: they overweight dramatic, scary outcomes relative to documented conflict research base rates, and they reprice slowly when breaking news hits during Asian or European business hours while US retail is asleep. This skill corrects both without any external API.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Geopolitical Bias

1. Discover active geopolitical markets on Polymarket using conflict/diplomacy keywords
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `geopolitics_bias()` — combines fear-premium correction with regional news timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Geopolitics Bias (built-in, no API required)

Two compounding structural edges:

**Factor 1 — Fear/Narrative Premium Correction**

Retail systematically overprices dramatic, scary outcomes and underprices boring-but-likely ones. Conflict research databases (ACLED, ICG) document base rates that deviate sharply from media-driven market pricing:

| Event type | Why retail misprices it | Multiplier |
|---|---|---|
| Nuclear / WMD use | Post-WWII base rate is near-zero; media panic inflates | **0.65x** |
| Coup / regime change | Retail overprices drama; ~50% actual success rate | **0.75x** |
| Full invasion / occupation | Retail anchors to worst-case escalation | **0.80x** |
| Ceasefire / peace deal / truce | Only ~40% of ceasefires hold within 6 months | **0.80x** |
| Sanctions / embargo | ~30–40% achieve stated objectives; overestimated | **0.85x** |
| UN vote / Security Council | P5 veto patterns are well-documented; procedural | **1.10x** |
| Diplomatic breakthrough | Boring — retail consistently underprices it | **1.15x** |

**Factor 2 — Regional News Timing Window**

Polymarket is US-dominated. Markets take 15–45 min to reprice events that break during Asian or European business hours when US retail is asleep:

| Region | Active window (UTC) | Multiplier | Rationale |
|---|---|---|---|
| Asia/Pacific (China, Taiwan, NK, Japan) | 00:00–08:00 | **1.20x** | US asleep, repricing lag open |
| Asia/Pacific | 13:00–22:00 | **0.95x** | US prime time — priced quickly |
| Europe/Middle East (Ukraine, Russia, Iran, Israel, NATO) | 06:00–14:00 | **1.15x** | US just waking, partial lag |
| Europe/Middle East | 18:00–04:00 | **0.95x** | Off-hours, less news flow |

Combined and capped at **1.35x**. A diplomatic breakthrough (1.15x) during Asia active hours (1.20x) → 1.35x cap. A nuclear market at any time → 0.65x floor.

### Keywords Monitored

```
war, ceasefire, sanctions, NATO, Ukraine, Russia, China, Taiwan, Iran,
nuclear, UN, diplomacy, invasion, treaty, military, missile, coup,
election interference, espionage, regime change, Security Council,
veto, peace deal, summit, Gaza, Israel, North Korea, DPRK,
South China Sea
```

### Remix Signal Ideas

- **GDELT Project**: Real-time global event database — feed event velocity into `p` to trade divergence between conflict data and market pricing
- **ACLED conflict data**: Armed conflict location and event intensity scores — use as leading indicator for escalation/de-escalation markets
- **UN Security Council voting records**: P5 veto pattern analysis for UN vote markets
- **ICG (International Crisis Group) alerts**: Early-warning signals for crisis escalation before markets react


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
| `SIMMER_MIN_VOLUME` | `20000` | Min market volume filter (USD) — geopolitical markets need liquidity |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `5` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
