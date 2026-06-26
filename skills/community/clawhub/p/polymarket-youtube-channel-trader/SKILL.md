---
name: polymarket-youtube-channel-trader
description: "Trades Polymarket YouTube channel markets (subscriber milestones, view-count races). Requires SIMMER_API_KEY for trade execution via simmer-sdk. Paper trading by default, real trades only with --live flag."
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: YouTube Channel Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# YouTube Channel Trader

> **This is a remixable template.**
> The default signal requires no external API — it uses hardcoded channel volatility profiles, a first-hour view velocity model, and day-of-week timing applied on top of standard conviction sizing. Wire in YouTube Data API v3 for live subscriber counts and view velocity, and the edge sharpens dramatically.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your signal provides the alpha.

## Strategy Overview

The top 10 YouTube channels are treated as distinct financial assets — each with its own volatility profile, growth trajectory, and event calendar. Subscriber counts are market cap. Subscriber deltas are daily returns. View velocity on a new video is trading volume.

Prediction markets on YouTube milestones are systematically mispriced because retail treats all channels the same. They don't. MrBeast has 10× the daily growth volatility of Cocomelon. A milestone 5% above current subscribers has a completely different probability for these two channels.

Three structural edges compound:

**1. First-hour view velocity mispricing**
When a major channel drops a video, view counts do not accumulate uniformly over 24 hours. MrBeast captures ~55% of his 24-hour views in the first hour. A market asking "will this video reach 5M views in the first 2 hours?" is a first-passage probability question. Retail prices it as a terminal probability. The same structural gap that makes BTC weekend markets exploitable makes YouTube flash markets exploitable.

**2. Channel volatility profiles**
Each of the top 10 channels has a measurable daily subscriber growth σ. Children's content (Cocomelon, Kids Diana Show, Like Nastya, Vlad and Niki) has σ ≈ 0.02%/day — extremely stable, like a stablecoin. Milestone markets are fairly priced. MrBeast has σ ≈ 0.25%/day with positive skew (viral videos spike subscribers; nothing crashes them). Milestone markets for MrBeast chronically underprice the upside tail. PewDiePie has high σ with slight negative skew — comeback/retirement uncertainty dominates.

**3. Weekend posting window**
MrBeast has posted 62% of his top-100 most-viewed videos on Friday–Sunday UTC. WWE's major PPV events are almost exclusively on weekends (70%). The timing edge is structurally identical to BTC weekend volatility: enter on Thursday–Friday before the drop, capture the pricing gap before the market reprices on actual view velocity.

## The Ten Assets

| Channel | Subs (M) | Daily σ | Skew | Weekend post % | First-hour % | Content type |
|---|---|---|---|---|---|---|
| MrBeast | 370 | 0.25% | +0.40 | 62% | 55% | viral_challenge |
| T-Series | 275 | 0.04% | +0.10 | 45% | 30% | music |
| Cocomelon | 178 | 0.02% | +0.05 | 40% | 20% | children |
| SET India | 175 | 0.03% | +0.05 | 50% | 25% | tv_content |
| Kids Diana Show | 128 | 0.02% | +0.05 | 38% | 18% | children |
| PewDiePie | 111 | 0.15% | −0.05 | 30% | 45% | commentary |
| Like Nastya | 122 | 0.02% | +0.05 | 42% | 18% | children |
| Vlad and Niki | 120 | 0.02% | +0.05 | 40% | 18% | children |
| Zee Music Company | 108 | 0.04% | +0.10 | 48% | 28% | music |
| WWE | 101 | 0.08% | +0.20 | 70% | 40% | sports_entertainment |

## Signal Logic

### Three multipliers — one per structural edge

**First-hour velocity multiplier** (applied when question contains time-bounded language):

```
velocity_edge = channel.first_hour_pct / 0.30    (normalised to average)
mult = 1.0 + (velocity_edge - 1.0) × 0.40
```

| Channel | first_hour_pct | velocity_mult |
|---|---|---|
| MrBeast | 55% | **1.33x** |
| PewDiePie | 45% | **1.20x** |
| WWE | 40% | **1.13x** |
| T-Series / Zee Music | 28–30% | **1.00x** |
| Children's channels | 18–20% | **0.84x** |

Triggered by: "first hour", "in 2 hours", "in 5 minutes", "in 10 minutes", "within 24 hours", "first day"

**Volatility profile multiplier**:

```
vol_mult   = 1.0 + channel.daily_vol × 2.0
skew_bonus = channel.skew × 0.5
combined   = vol_mult + skew_bonus   (capped 0.80–1.30x)
```

| Channel | daily_vol | skew | vol_mult |
|---|---|---|---|
| MrBeast | 0.25% | +0.40 | **1.30x cap** |
| PewDiePie | 0.15% | −0.05 | **1.28x** |
| WWE | 0.08% | +0.20 | **1.26x** |
| T-Series / Zee | 0.04% | +0.10 | **1.13x** |
| Children's channels | 0.02% | +0.05 | **0.80x** |

**Weekend posting window multiplier**:

```
base_mult = 0.80 + channel.weekend_post × 0.50
timing    = Thursday→1.15x, Friday→1.10x, Saturday→1.00x, Sunday→0.90x, Mon–Wed→0.85x
combined  = base_mult × timing   (capped 0.70–1.35x)
```

| Channel | weekend_post | Thursday base | Thursday combined |
|---|---|---|---|
| WWE | 70% | 1.15x | **1.35x cap** |
| MrBeast | 62% | 1.11x | **1.28x** |
| SET India | 50% | 1.05x | **1.21x** |
| PewDiePie | 30% | 0.95x | **1.09x** |
| Children's | 38–42% | 0.99x | **1.14x** |

### Flash play examples (5-min / 10-min resolution)

**MrBeast video drops Saturday — "Will video reach 5M views in first hour?" at 28%:**

```
velocity_mult = 1.33x  (fhp=55% >> average)
vol_mult      = 1.30x  (σ=0.25%, skew+0.40)
weekend_mult  = 1.00x  (Saturday, mid-window)
combined bias = 1.33 × 1.30 × 1.00 = 1.729 → capped 1.40x

p=28%, YES_THRESHOLD=38%
conviction = (0.38 - 0.28) / 0.38 × 1.40 = 0.37
size = max($5, 0.37 × $30) = $11
```

**WWE WrestleMania weekend — subscriber milestone market — Thursday entry:**

```
velocity_mult = 1.00x  (no time-bounded language)
vol_mult      = 1.26x  (σ=0.08%, skew+0.20)
weekend_mult  = 1.35x  (wp=70%, Thursday→cap)
combined bias = 1.00 × 1.26 × 1.35 = 1.70 → capped 1.40x
```

**Cocomelon subscriber milestone — any day:**

```
velocity_mult = 0.84x  (fhp=18%, slow accumulation)
vol_mult      = 0.80x  (σ=0.02%, very stable)
weekend_mult  = 1.14x  (wp=40%, Thursday)
combined bias = 0.84 × 0.80 × 1.14 = 0.77x
```
Low-vol children's channels trade at reduced conviction — the skill correctly identifies them as "stablecoins" not worth aggressive sizing.

### Sizing table — MrBeast flash play (bias=1.40x, MAX_POSITION=$30)

| Price p | Conviction | Biased | Size |
|---|---|---|---|
| 38% (threshold) | 0% | 0% | $5 floor |
| 28% | 26% | 37% | $11 |
| 18% | 53% | 74% | $22 |
| 5% | 87% | 100% | $30 cap |

### Keywords monitored

```
mrbeast, mr beast, jimmy donaldson,
t-series, tseries,
cocomelon, coco melon,
set india,
kids diana, diana show, diana and roma,
pewdiepie, pewdie pie, felix kjellberg,
like nastya, nastya,
vlad and niki,
zee music, zeemusic,
wwe, world wrestling, wrestlemania, smackdown, raw channel,
youtube subscribers, youtube milestone, youtube channel,
youtube views, youtube video, most subscribed,
subscriber count, subscriber race, youtube rivalry
```

### Remix signal ideas

- **YouTube Data API v3 (free)**: Wire live subscriber counts and view velocity into `compute_signal` — compare current growth rate to 90-day rolling average; when velocity is 2× average (MrBeast just dropped a video), multiply YES conviction by the velocity ratio; this turns the skill from a timing model into a real-time momentum model
- **First-hour live feed**: During a flash play (5-min/10-min market), poll the YouTube video stats API every 60 seconds and compute the view count accumulation curve; if the first 10 minutes track above the channel's historical P75, back YES on all remaining hour-1 milestones
- **Subscriber rivalry tracker**: The MrBeast vs T-Series subscriber race drove massive Polymarket volume in 2023–24; build a dedicated rivalry module that watches the gap between the #1 and #2 channels and flags markets about rank changes when the gap narrows below 5M
- **PewDiePie return probability**: PewDiePie's irregular posting makes his markets uniquely high-variance; scrape his posting frequency (videos/month) and use a Poisson model to estimate P(posts this week) — wires directly into the weekly/monthly view milestone markets
- **WWE PPV calendar**: Hardcode WWE's annual PPV schedule (WrestleMania, SummerSlam, Royal Rumble, Survivor Series) — these are known subscriber spike events; a 2-week window before each PPV should have weekend_post_mult capped at 1.35x regardless of day-of-week

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`MIN_DAYS=0` by default — this allows same-day flash plays. Set `SIMMER_MIN_DAYS=1` to restrict to longer-horizon markets only.

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `2000` | Min market volume — lower bar for niche YouTube markets |
| `SIMMER_MAX_SPREAD` | `0.09` | Max bid-ask spread — slightly wider to allow flash markets |
| `SIMMER_MIN_DAYS` | `0` | Min days to resolution — 0 enables same-day flash plays |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Buy NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
