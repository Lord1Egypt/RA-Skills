---
name: polymarket-coffee-trader
description: Trades Polymarket coffee markets using three compounding seasonal edges unique to the global coffee market — Brazil frost window mispricing, harvest cycle awareness, and ENSO phase (La Niña/El Niño). Conviction scales with distance to threshold and a seasonal bias multiplier that peaks in July (peak Brazil frost risk) and compresses in October–April when frost is meteorologically impossible.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Coffee Seasonal Trader
  difficulty: intermediate
---

# Coffee Seasonal Trader

> **This is a remixable template**
> The default signal requires no external API — it uses date-derived seasonal multipliers (frost calendar, harvest cycle, ENSO phase) applied on top of standard price-threshold conviction sizing.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your signal provides the alpha.

## Strategy Overview

Coffee is one of the world's most weather-sensitive commodities — and one of the most predictably seasonal. Three structural patterns repeat every year, and Polymarket participants systematically misprice all three:

**1. Brazil frost window** — Commercially damaging frost in Brazil's coffee belt (Cerrado Mineiro, Sul de Minas, Mogiana) is only physically possible during June–August. Polar air masses (friagens) push north from Patagonia into Brazil's southern highlands exclusively in winter. Yet retail traders price frost optionality into coffee price markets year-round. A market asking "will arabica hit $5?" in January embeds a frost premium that cannot materialize for six more months. We fade it. In July, we back the same trade at higher conviction.

**2. Brazil harvest cycle** — The main arabica harvest runs April–September. Post-harvest (October–January), supply is at its seasonal peak and well-understood by the market — price spike markets are overpriced. Pre-harvest (February–March), inventory draws down and supply anxiety is legitimate.

**3. ENSO phase (La Niña / El Niño)** — La Niña brings drought stress to Brazil's coffee belt, tightening arabica supply. El Niño brings excess rainfall to Vietnam, disrupting Robusta logistics. Current ENSO phase is set via `SIMMER_ENSO_PHASE` env var (update quarterly from NOAA).

## The Core Insight: Frost Optionality Has an Expiry Date

The single most important edge in this skill:

```
Brazil frost is only possible in June, July, August.

A coffee price spike market in October through May contains frost
optionality with zero meteorological value.

Retail doesn't know this. They price "could there be a frost?" as a
year-round background risk. We know the frost calendar.
```

The historical record confirms: every major Brazilian coffee frost event (1975, 1994, 1997, 2000, 2021) occurred between June 15 and August 31. None have occurred outside this window in the modern record.

This gives us a clean seasonal on/off signal:

| Period | Frost possible? | Our adjustment |
|---|---|---|
| July | Yes — peak risk | 1.30x conviction |
| June / August | Yes — shoulder | 1.15x conviction |
| May / September | No — but market transitioning | 1.05x |
| October – April | No — meteorologically impossible | 0.80x (fade frost premium) |

## Signal Logic

### Default Signal: Conviction-Based Sizing with Coffee Seasonal Bias

1. Discover active coffee markets via keyword sweep (prices, crop, weather, futures)
2. Gate: must be a genuine coffee market (`_is_coffee_market`)
3. Gate: spread ≤ MAX_SPREAD, days to resolution ≥ MIN_DAYS
4. Compute `coffee_seasonal_bias(question)` = frost_mult × harvest_mult × enso_mult, capped 0.65–1.40x
5. Conviction = `(threshold - p) / threshold × bias` (YES) or `(p - threshold) / (1 - threshold) × bias` (NO)
6. Size = `max(MIN_TRADE, conviction × MAX_POSITION)`

### The Three Multipliers

**Frost window multiplier** (date-derived, no API needed):

| Month | Label | Multiplier |
|---|---|---|
| July | JULY(peak-frost) | 1.30x |
| June, August | FROST-SHOULDER | 1.15x |
| May, September | FROST-MARGINAL | 1.05x |
| October – April | NO-FROST | 0.80x |

**Harvest cycle multiplier**:

| Period | Label | Multiplier |
|---|---|---|
| February – March | PRE-HARVEST | 1.10x |
| April – June | HARVEST-START | 1.05x |
| July – September | HARVEST-PEAK | 1.00x |
| October – January | POST-HARVEST | 0.90x |

**ENSO multiplier** (set via `SIMMER_ENSO_PHASE`):

| ENSO phase | Market type | Multiplier |
|---|---|---|
| `la_nina` | Arabica / Brazil | 1.15x (drought stress → bullish) |
| `la_nina` | Robusta / Vietnam | 1.00x (neutral) |
| `el_nino` | Robusta / Vietnam | 1.15x (logistics disruption → bullish) |
| `el_nino` | Arabica / Brazil | 1.00x (mixed) |
| `neutral` | Any | 1.00x |

### Combined Examples (TODAY: March 22, 2026 — neutral ENSO assumed)

| Scenario | Frost | Harvest | ENSO | Final bias |
|---|---|---|---|---|
| Arabica price spike — March, neutral | 0.80x | 1.10x | 1.00x | **0.88x** |
| Brazil frost event — July, La Niña | 1.30x | 1.00x | 1.15x | **1.40x cap** |
| Robusta supply — October, El Niño | 0.80x | 0.90x | 1.15x | **0.83x** |
| Arabica production — June, neutral | 1.15x | 1.05x | 1.00x | **1.21x** |

### How Sizing Works

With defaults (YES_THRESHOLD=38%, MIN_TRADE=$5, MAX_POSITION=$30):

| Price p | Conviction (no bias) | July + La Niña (1.40x) | Mar off-season (0.88x) |
|---|---|---|---|
| 38% (at threshold) | 0% | $5 floor | $5 floor |
| 30% | 21% | $8.8 | $5.5 |
| 20% | 47% | $19.7 | $12.4 |
| 5% | 87% | $30 (cap) | $23 |

### Keywords Monitored

```
coffee price, arabica price, robusta price, coffee futures, arabica futures,
KC futures, coffee above, coffee below, coffee reaches, coffee exceed,
coffee production, coffee crop, coffee harvest, coffee yield,
brazil coffee, vietnam coffee, colombia coffee, ethiopia coffee,
arabica production, robusta production, coffee bags, million bags,
coffee frost, frost event, frost damage, brazil frost,
coffee drought, coffee rainfall, cerrado, sul de minas,
coffee belt, coffee freeze, coffee, arabica, robusta, coffee market
```

### Remix Signal Ideas

- **ICE Arabica KC1 spot price**: Wire real-time KC1 futures price into `compute_signal` — compute % distance to question threshold and compare to Polymarket probability; when the market implies a different probability than what the options surface suggests, you have a precise edge
- **NOAA ENSO outlook**: Automate `SIMMER_ENSO_PHASE` updates from the monthly NOAA CPC ENSO forecast API (free, JSON) — current hardcoded value updates only when you redeploy; automated updates capture phase transitions earlier than retail
- **Brazil frost model**: Pull the 10-day ECMWF or GFS 850hPa temperature forecast for Minas Gerais (lat -20, lon -45) — if anomalously cold air is forecast to reach the coffee belt within the frost window, spike conviction to 1.40x regardless of calendar month
- **Vietnam rainfall index**: Use CHIRPS precipitation anomaly data for Vietnam's Central Highlands during robusta flowering (Oct–Dec) — anomalous drought during flowering predicts 12–18 month forward supply shortage; fade robusta market prices that haven't incorporated this
- **Brazil biennial cycle**: Track whether current crop year is on-year (high) or off-year (low) in Brazil's biennial production cycle — on-years increase post-harvest supply surplus; off-years tighten; add a ±0.10x multiplier to harvest_cycle_mult accordingly

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
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Buy NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_ENSO_PHASE` | `neutral` | ENSO climate phase: `la_nina`, `el_nino`, or `neutral`. Update quarterly from NOAA CPC. |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
