---
name: polymarket-onlyfans-trader
description: Trades Polymarket markets on OnlyFans using three structural edges — celebrity pipeline base-rate mispricing (retail ignores demographic base rates for who joins), regulatory theater fading (ban markets are chronically overpriced because legislative processes take years), and creator earnings seasonality (revenue peaks Nov–Feb around Valentine's Day). Domain-agnostic across join, ban, and earnings market types.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: OnlyFans Trader
  difficulty: intermediate
---

# OnlyFans Trader

> **This is a remixable template.**
> The default signal requires no external API — it uses keyword-derived demographic multipliers, jurisdiction-specific regulatory priors, and date-based earnings seasonality applied on top of standard conviction sizing.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your signal provides the alpha.

## Strategy Overview

OnlyFans is one of the fastest-growing and most widely covered platforms in prediction markets — yet it is systematically mispriced in three distinct and exploitable ways.

**1. Celebrity pipeline bias** — Retail prices "will [celebrity] join OnlyFans?" based on general fame level, treating it as a rare or tabloid-worthy event. The actual base rate by demographic category tells a completely different story: reality TV contestants join at ~40%, Instagram models at ~30%, athletes at ~20%. Markets on reality TV show participants routinely sit at 15–20% — 2–3x below the historical base rate. We buy YES aggressively. Conversely, A-list Hollywood actors are priced at 15–25% when the true base rate is ~5% — tabloid speculation inflates prices above reality. We fade those.

**2. Regulatory theater** — Every 6–12 months a government announces it will "crack down on" or "ban" OnlyFans. These markets are priced by retail on political rhetoric. Legislative reality is different: the average time from "announced review" to enforceable legislation is 3–7 years, court injunctions routinely block enforcement, and VPN workarounds make practical bans largely unenforceable. Of 40+ announced restrictions since 2020, fewer than 3 resulted in enforceable law within 12 months. We systematically buy NO on ban markets.

**3. Creator earnings seasonality** — OnlyFans revenue is strongly seasonal, driven by the gift economy. The two weeks before Valentine's Day (February) is the single highest-revenue period for most creators. Black Friday, Christmas, and New Year also drive subscription spikes. Summer months show 10–20% lower-than-average activity. Earnings milestone markets that don't account for this seasonal structure are systematically off.

## The Core Insight: Three Different Market Types, Three Different Edges

This skill classifies each market before trading it:

| Market type | Example | Edge | Direction |
|---|---|---|---|
| `join` | "Will [celebrity] join OnlyFans?" | Pipeline base-rate × season | Standard YES/NO |
| `ban` | "Will OnlyFans be banned in [country]?" | Regulatory theater fade | Lean NO |
| `earnings` | "Will [creator] earn $X by [date]?" | Earnings seasonality | YES in peak, NO in trough |

## Signal Logic

### Step 1 — Market classification (`_classify_market`)

Keywords route each market to a type:
- `ban`, `banned`, `restrict`, `blocked`, `shutdown`, `illegal`, `law` → `ban`
- `join`, `joining`, `create`, `start`, `sign up`, `open` → `join`
- `earn`, `revenue`, `million`, `subscriber`, `ipo`, `valuation` → `earnings`

### Step 2 — Type-specific bias multiplier

**Celebrity pipeline multiplier** (join markets only):

Parsed from question keywords — no external lookup needed.

| Demographic | Signals | Historical base rate | Multiplier |
|---|---|---|---|
| Reality TV contestant | "bachelor", "love island", "big brother", "real housewives", "survivor", "too hot to handle", "love is blind", "90 day fiance" + 20 more | ~40% | **1.35x** |
| Influencer / model | "influencer", "instagram model", "tiktok", "playboy", "fitness model" | ~30% | **1.20x** |
| Athlete / sports personality | "nfl", "nba", "ufc", "footballer", "wrestler" | ~20% | **1.10x** |
| Musician (pop/hip-hop) | "rapper", "singer", "pop star", "r&b" | ~15% | **1.00x** |
| A-list actor | "oscar winner", "hollywood actor", "movie star", "emmy" | ~5% (but often priced at 15–25%) | **0.75x** (fade) |
| Unknown | — | — | 1.00x |

**Regulatory theater multiplier** (ban markets only):

Jurisdiction determines how aggressively we fade the YES side:

| Jurisdiction | Reason | Multiplier |
|---|---|---|
| US / federal | First Amendment constraints make platform bans near-impossible | 0.90x |
| UK / Britain | Age verification laws exist, but full bans face strong opposition | 0.95x |
| EU / Europe | GDPR enforcement risk, not platform bans | 0.90x |
| Australia | eSafety Office has powers but full bans historically blocked by courts | 0.85x |
| Authoritarian (China, Russia, UAE, Saudi, Iran) | Real risk but still overpriced for speed | 1.10x |
| Generic | — | 1.00x |

**Earnings seasonality multiplier** (earnings + join markets):

| Period | Driver | Multiplier |
|---|---|---|
| November – February | Holiday gifting, Valentine's Day ramp-up | **1.20x** |
| March – April | Post-peak normalization | 1.00x |
| May – October | Summer trough — lower subscription activity | **0.85x** |

### Step 3 — Combined bias

```
join:     pipeline_mult × season_mult   (capped 0.65–1.40x)
ban:      regulatory_mult               (regulatory theater dominates)
earnings: season_mult                   (1.20x in Nov–Feb, 0.85x in summer)
```

### Combined Examples (TODAY: March 22, 2026)

| Market | Type | Pipeline | Season | Regulatory | Final bias |
|---|---|---|---|---|---|
| "Will Love Island contestant X join OnlyFans?" — March | join | 1.35x | 1.00x | — | **1.35x** |
| "Will [Oscar-winner] join OnlyFans?" — December | join | 0.75x | 1.20x | — | **0.90x** |
| "Will OnlyFans be banned in the US?" | ban | — | — | 0.90x | **0.90x (lean NO)** |
| "Will [creator] earn $1M by January?" — November | earnings | — | 1.20x | — | **1.20x** |
| "Will [creator] reach 100k subscribers by August?" | earnings | — | 0.85x | — | **0.85x** |

### How Sizing Works

With defaults (YES_THRESHOLD=38%, NO_THRESHOLD=62%, MIN_TRADE=$5, MAX_POSITION=$30):

Reality TV contestant join market — March (1.35x bias):

| Price p | Conviction | Biased conviction | Size |
|---|---|---|---|
| 38% | 0% | 0% | $5 floor |
| 25% | 34% | 46% | $14 |
| 15% | 61% | 82% | $25 |
| 5% | 87% | 100% capped | $30 |

### Keywords Monitored

```
join onlyfans, joining onlyfans, onlyfans account, start onlyfans,
create onlyfans, onlyfans page, sign up onlyfans,
onlyfans ban, ban onlyfans, onlyfans banned, onlyfans restrict,
onlyfans blocked, onlyfans regulation, onlyfans law,
onlyfans illegal, onlyfans shutdown, shut down onlyfans,
onlyfans earnings, onlyfans revenue, onlyfans subscribers,
onlyfans million, onlyfans income, onlyfans top creator,
onlyfans ipo, onlyfans valuation, onlyfans creator fund,
onlyfans policy, onlyfans adult content, onlyfans
```

### Remix Signal Ideas

- **Social media signal detection**: Wire a Twitter/X search for "[celebrity name] onlyfans" mention spikes — a 5x increase in mentions in 48 hours is a strong leading indicator that a market priced at 15% should reprice to 35–50%; the public announcement typically follows within 2–4 weeks of the social media buildup
- **Reality TV show calendar**: Build a lookup of reality TV show air dates — contestants historically announce OnlyFans accounts 2–8 weeks post-finale when media attention is highest; a market resolving 3 months after a season finale that's priced at 20% for a female contestant is almost certainly underpriced
- **Legislative calendar**: For ban markets, wire in legislative calendar data (congress.gov for US, parliament.uk for UK) — if no bill has been introduced or assigned to committee, the ban market for "within 12 months" should be ≤5%; if a bill has passed committee, the multiplier should flip from fade to back
- **Valentine's Day countdown**: Hardcode an additional spike multiplier for earnings markets where the resolution date lands within 7 days of February 14 — this single week drives ~8–12% of annual creator revenue; markets systematically undervalue this concentration
- **Creator tier classification**: Extend `_classify_market` to distinguish top-100 creators (known, named in question) from mid-tier — top creators have more predictable earnings trajectories; mid-tier has higher variance that the market tends to underprice on both tails

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
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume — lower bar since OnlyFans markets tend to be smaller |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Buy NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
