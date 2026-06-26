---
name: polymarket-music-entertainment-trader
description: Trades Polymarket prediction markets on music streaming milestones, album chart performance, Grammy nominations, concert tour revenues, and music industry deals. Use when you want to capture alpha on entertainment markets using Spotify/Billboard data signals and artist momentum indicators.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Music & Entertainment Trader
  difficulty: beginner
---

# Music & Entertainment Trader

> **This is a template.**  
> The default signal is keyword discovery + Spotify Charts API momentum — remix it with Billboard chart position tracking, TikTok trending audio API, Apple Music chart feeds, or social media velocity metrics for artist momentum.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Record labels now monitor Polymarket the way Wall Street monitors stocks — as real-time demand signals for artist momentum. This creates an unusual information flow:

- **Artists/labels with inside momentum** push prices UP before numbers confirm
- **Retail fans** bid on emotional attachment, often overpaying for beloved artists
- **Data-driven traders** can fade fan-driven overpricing and capture industry-informed flows

This skill trades:
- **Streaming milestones** — First-week equivalents, billion-stream thresholds
- **Chart performance** — Billboard 200 #1, Hot 100 chart positions
- **Awards** — Grammy nominations/wins, VMAs, AMAs outcomes
- **Tour revenue** — Gross threshold markets for major arena tours
- **Industry deals** — Catalog sales, platform launches, licensing deals

## Signal Logic

### Default Signal: Conviction-Based Sizing with Sentiment Bias

1. Discover active music/entertainment markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `sentiment_bias()` multiplier based on market type and artist category
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Sentiment Bias (built-in, no API required)

Different market types have systematic mispricing patterns in music. `sentiment_bias()` adjusts conviction based on known retail behavior:

| Market type | Bias | Why |
|---|---|---|
| Megastar fan markets (Taylor Swift, Beyoncé, BTS) | **0.75x** | Fan bias inflates YES; emotionally driven, high noise |
| Awards ceremonies (Grammy, Oscar, VMA) | **0.85x** | Fan voting + label politics = hard to model reliably |
| Streaming / chart milestones (Spotify, Billboard) | **1.15x** | Data available before market reprices — lean in |
| Emerging global genres (Afrobeats, K-pop, Latin) | **1.20x** | Systematically underweighted by US-centric retail traders |
| Other | **1.00x** | No systematic bias detected |

Example: Afrobeats streaming milestone at 25% → conviction 34% × 1.2x = 41% → $6 position. Same market for a Beyoncé milestone → 34% × 0.75x = 26% → $5 (floor, trade cautiously).

### Remix Ideas

- **Spotify Charts API / Chartmetric**: Replace `market.current_probability` with stream velocity-implied probability — trade the divergence between real-time data and market price
- **TikTok Trending**: Viral audio as leading indicator for streaming momentum (48–72h lag to market)
- **Ticketmaster/StubHub**: Secondary ticket prices as proxy for tour gross markets
- **RIAA certification tracker**: Monitor certifications approaching milestone thresholds

## Market Categories Tracked

```python
KEYWORDS = [
    'Taylor Swift', 'Bad Bunny', 'Beyoncé', 'Drake', 'Kendrick',
    'Spotify', 'Billboard', 'Grammy', 'streaming', 'album',
    'chart', 'tour', 'concert', 'certification', 'RIAA',
    'K-pop', 'Afrobeats', 'Latin music', 'country', 'TikTok music',
    'music catalog', 'record label', 'music deal',
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $15 USDC | Entertainment markets are retail-driven |
| Min market volume | $2,000 | Lower bar; community markets matter |
| Max bid-ask spread | 15% | Entertainment markets can be illiquid |
| Min days to resolution | 7 | Streaming data needs time to settle |
| Max open positions | 10 | Diversify across artists and categories |

## Behavioral Edge

### Fan Bias
Music fans are strongly emotionally attached. For beloved artists (Taylor Swift, BTS), markets consistently overprice YES outcomes by 8–15% vs streaming data expectations. Short-term this means NO positions on fan-favorite markets are structurally profitable.

### Recency Momentum
Conversely, artists trending hard on TikTok are underpriced for 48–72 hours before mainstream media coverage. Early entry on breakout markets captures the lag.

## Key Data Sources

- **Spotify Charts**: https://charts.spotify.com/charts/overview/global
- **Billboard API**: https://www.billboard.com/charts/
- **Chartmetric**: https://chartmetric.com/ (paid, powerful)
- **RIAA Database**: https://www.riaa.com/gold-platinum/

## Installation & Setup

```bash
clawhub install polymarket-music-entertainment-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs every 30 minutes (`*/30 * * * *`). Chart data updates weekly; streaming data daily. No need for tight polling.

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
| `SIMMER_MAX_POSITION` | `15` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `2000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.15` | Max bid-ask spread (0.15 = 15%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
