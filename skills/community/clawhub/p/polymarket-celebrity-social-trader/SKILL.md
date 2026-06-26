---
name: polymarket-celebrity-social-trader
description: Trades Polymarket prediction markets on celebrity events, viral social media moments, Elon Musk tweet counts, influencer milestones, and reality TV outcomes. Exploits fan loyalty overcrowding and data-trackable metric gaps (Social Blade, posting cadence, boxing records) that retail ignores.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Celebrity & Social Media Trader
  difficulty: beginner
---

# Celebrity & Social Media Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `celebrity_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Celebrity markets look chaotic but split cleanly into two camps: **data-trackable** (subscriber growth rates, tweet cadence, athletic records) and **emotionally-driven** (fan loyalty, feuds, relationships). The data-trackable ones have genuine structural edges. The emotional ones are traps for anyone who doesn't understand that retail here is trading *feelings*, not probability.

The single most important insight in this domain: **megastar fan bases are the worst market makers on Polymarket**. They overcrowd YES on anything involving their idol, creating systematic NO edges that the bias function captures.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Celebrity Bias

1. Discover active celebrity and social media markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `celebrity_bias()` — combines market type predictability with weekend repricing lag
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Celebrity Bias (built-in, no API required)

Two structural edges:

**Factor 1 — Market Type Predictability**

Celebrity markets are NOT uniformly unpredictable. The key is distinguishing what has data behind it:

| Market type | Multiplier | Why |
|---|---|---|
| Subscriber / follower / view milestones | **1.25x** | Social Blade publishes daily growth data — "will MrBeast reach 400M by X" is calculable from the trend; retail never checks |
| Elon Musk / high-volume poster tweet count | **1.20x** | Documented consistent cadence (~350–400 posts/week); markets misprice on vibes not data |
| Boxing / MMA / combat sport outcome | **1.15x** | Athletic records, training camp signals, fight history exist; retail prices fame not skill |
| Reality TV voting outcome | **1.10x** | Nielsen Social Content Ratings track engagement correlating with votes |
| Awards (Oscars, Grammys, Emmy, BAFTA) | **0.85x** | Efficiently priced by dedicated awards-circuit followers — less edge |
| Celebrity relationship / breakup / divorce | **0.80x** | Tabloid-narrative noise — rival fanbases overprice both directions |
| Celebrity beef / feud reconciliation | **0.75x** | Fans desperately want YES; historical reconciliation base rate is low — fade hard |
| Megastar fan-favourite markets (Taylor Swift, Beyoncé, BTS, etc.) | **0.75x** | Fan loyalty is the dominant pricing force — not information. This is the most dangerous overcrowded trade in the category |

**Factor 2 — Weekend Repricing Lag**

Social media metrics (subscribers, streams, tweet counts, chart positions) update continuously. But Polymarket market makers are least active Friday evening through Sunday. Social media activity peaks on weekends. The gap between real-world metric movement and market repricing is widest on weekends.

| Condition | Multiplier |
|---|---|
| Metric-based question (subscribers, streams, tweets, charts) + Friday–Sunday | **1.15x** |
| All other combinations | **1.00x** |

Combined and capped at **1.35x** — intentionally lower cap than data-driven domains (crypto capped at 1.40x) because celebrity markets have inherently higher narrative noise. A subscriber milestone question on a Saturday → 1.25 × 1.15 = **1.35x cap**. A Taylor Swift fan-favourite market at any time → **0.75x** — trade near the MIN_TRADE floor.

### The Fan Loyalty Trap — Why 0.75x for Megastars

This deserves its own section. Markets involving Taylor Swift, Beyoncé, BTS, and similar artists are *structurally mispriced* by their fanbases in a predictable direction: always too bullish on positive outcomes. "Will Taylor Swift announce a world tour?" gets bid to 70% when the base rate for any artist is 20%. "Will BTS reunite before X?" gets bid to 65% by fans who are pricing their wish, not the probability.

The 0.75x dampener does not mean *avoid* these markets — it means *size down* and be especially alert to NO signals when p ≥ NO_THRESHOLD, because that is where the fan-bid overcrowding creates the most exploitable gap.

### Keywords Monitored

```
Elon Musk, tweet, X post, YouTube, subscribers, viral, TikTok views,
celebrity, divorce, relationship, beef, reality TV, The Bachelor,
Oscars, Golden Globes, social media, followers, Instagram, MrBeast,
Logan Paul, boxing, Jake Paul, influencer, Taylor Swift, Beyoncé,
Grammy, Emmy, streaming, Spotify streams, chart, Billboard, feud,
reconcile, breakup
```

### Remix Signal Ideas

- **Social Blade API**: Daily subscriber growth rates for YouTube/TikTok/Twitch — compare published trajectory to Polymarket milestone probability, trade the divergence
- **Spotify Charts API**: Real-time streaming data for "will artist reach X streams" markets
- **Nielsen Social Content Ratings**: Social engagement scores correlating with reality TV votes
- **X/Twitter API v2**: Elon's actual posting cadence — compare to market's implied tweet count probability


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
| `SIMMER_MAX_POSITION` | `20` | Max USDC per trade — lower ceiling reflects domain noise |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.12` | Max bid-ask spread (12%) — wider tolerance for niche markets |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
