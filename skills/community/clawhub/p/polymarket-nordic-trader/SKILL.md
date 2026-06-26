---
name: polymarket-nordic-trader
description: Trades Polymarket prediction markets focused on Scandinavian and Nordic events — Swedish politics, Norwegian economy, Danish infrastructure, Nordic business milestones (Spotify, Northvolt, Klarna), local weather extremes, and regional sports outcomes. Use when you want to capture alpha on underserved Nordic markets where local knowledge is a structural edge.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Nordic & Scandinavian Trader
  difficulty: beginner
---

# Nordic & Scandinavian Trader

> **This is a template.**  
> The default signal is keyword discovery + Swedish/Nordic news feed monitoring — remix it with Riksdagen API for legislative tracking, SCB (Statistics Sweden) data releases, Affärsvärlden market feeds, or Spotify investor relations signals.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Nordic markets are one of the most underserved categories on global prediction platforms. Traders with genuine local knowledge — Swedish politics, Scandinavian business news, Nordic weather patterns — hold structural information advantages over global retail traders.

This skill trades:
- **Swedish politics** — Government formation, Riksdag legislative milestones
- **Nordic business** — Spotify profitability, Northvolt recovery, Klarna/unicorn IPOs
- **Infrastructure** — Förbifart Stockholm, Malmö Arena, high-speed rail announcements
- **Sports** — Champions League Nordic teams, Swedish/Norwegian international competitions
- **Local weather** — Stockholm heatwaves, Öresund ice crossing, Oslo snowfall records
- **Culture** — Melodifestivalen viewership, Way Out West attendance

Key edge: the vast majority of Polymarket liquidity is US/global retail. Nordic-specific markets will have mispriced odds whenever the resolver requires local knowledge.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Local Edge Bias

1. Discover markets matching Nordic/Scandinavian keywords
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `local_edge_bias()` — combines CET timezone timing with domain confidence
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Local Edge Bias (built-in, no API required)

`local_edge_bias()` multiplies conviction using two factors simultaneously:

**Factor 1 — CET Timezone Window**

Nordic news breaks during CET business hours (approx 06:00–18:00 UTC). Polymarket is US-dominated — repricing on Nordic news takes 2–6 hours. Trading inside the window means information is still fresh.

| Time (UTC) | Multiplier | Why |
|---|---|---|
| 06:00–18:00 | **1.2x** | CET business hours — Nordic news is fresh, US retail hasn't caught up |
| 18:00–06:00 | **0.9x** | Outside window — advantage likely already priced in |

**Factor 2 — Domain Confidence**

| Domain | Multiplier | Why |
|---|---|---|
| Riksdag / politics / elections | **1.20x** | Public structured data, predictable process |
| Nordic tech (Spotify, Klarna, Northvolt) | **1.15x** | Swedish business press is early and detailed |
| SMHI / local weather | **1.10x** | Swedish forecasts published before English-language coverage |
| Sports / culture (Zlatan, Melodifestivalen) | **0.85x** | High randomness, hard to model |

Combined multiplier is capped at **1.40x** to avoid over-sizing on illiquid markets.

Example: Riksdag vote question at 25% during CET hours → conviction 34% × (1.2 × 1.2 = 1.40x capped) = 48% → $10 position. Same question at 01:00 UTC → 34% × (0.9 × 1.2 = 1.08x) = 37% → $7.

### Remix Ideas

- **Riksdagen API**: Feed live voting data into p — trade divergence between parliamentary consensus and market price
- **SMHI API**: Replace market probability with SMHI forecast confidence for weather markets
- **SVT/Di.se RSS**: Monitor Swedish news feeds for events that haven't hit English-language sources yet
- **Avanza/Nordnet sentiment**: Swedish retail stock sentiment as proxy for Nordic tech markets
- **SCB data releases**: Statistics Sweden economic releases as leading indicator for macro markets

## Market Categories Tracked

```python
KEYWORDS = [
    'Sweden', 'Sverige', 'Stockholm', 'Malmö', 'Göteborg',
    'Norway', 'Norge', 'Oslo', 'Denmark', 'Danmark', 'Copenhagen',
    'Finland', 'Helsinki', 'Nordic', 'Scandinavian',
    'Spotify', 'Northvolt', 'Klarna', 'Ericsson', 'Volvo', 'IKEA',
    'Riksdag', 'Melodifestivalen', 'Zlatan', 'Allsvenskan',
    'SMHI', 'Öresund',
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $20 USDC | Nordic markets may be illiquid |
| Min market volume | $1,000 | Accept lower liquidity for edge opportunity |
| Max bid-ask spread | 20% | Niche markets have wider spreads |
| Min days to resolution | 3 | Local events can resolve quickly |
| Max open positions | 8 | Diversify across Nordic themes |

## Local Knowledge Edge

### Information Advantage Examples
- **Förbifart Stockholm**: A Swedish civil engineer knows the tunnel's actual completion status better than US retail traders
- **Northvolt bankruptcy**: Swedish business press covered the restructuring in detail months before English-language coverage
- **SMHI winter forecasts**: Local seasonal weather outlooks are published in Swedish first
- **Melodifestivalen**: SVT viewership trends visible to Swedish residents immediately

### Timing Edge
Swedish/Nordic news typically breaks in CET timezone (UTC+1/+2). US-dominated Polymarket markets take 2–6 hours to reprice on Nordic news.

## Key Data Sources

- **SMHI** (Weather): https://www.smhi.se/
- **Riksdagen** (Parliament): https://data.riksdagen.se/
- **SCB** (Statistics): https://www.scb.se/
- **SVT Nyheter**: https://www.svt.se/nyheter/
- **Di.se** (Business): https://www.di.se/

## Installation & Setup

```bash
clawhub install polymarket-nordic-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs every 15 minutes (`*/15 * * * *`). Nordic events follow business hours (CET); tighter polling during 06:00–22:00 CET recommended in remixes.

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
| `SIMMER_MAX_POSITION` | `20` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `1000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.20` | Max bid-ask spread (0.20 = 20%, wider for niche markets) |
| `SIMMER_MIN_DAYS` | `3` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
