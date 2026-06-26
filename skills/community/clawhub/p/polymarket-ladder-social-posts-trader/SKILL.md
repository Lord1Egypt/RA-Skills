---
name: polymarket-ladder-social-posts-trader
description: Trades distribution-sum violations in social media post-count range markets on Polymarket. Range bins for the same person and date range must sum to ~100% — when they do not, individual bins are mispriced. Also detects local anomalies where a single bin deviates sharply from its neighbors.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Ladder Social Posts Distribution Trader
  difficulty: advanced
---

# Ladder -- Social Posts Distribution Trader

> **This is a template.**
> The default signal is distribution-sum violation detection across social media post-count range markets -- remix it with social media API feeds, posting frequency models, or cross-person correlation analysis.
> The skill handles all the plumbing (market discovery, distribution construction, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists multiple post-count range bins for the same person and date range:

- "Will CZ post 140-159 posts from March 1 to April 1?" = 25%
- "Will CZ post 160-179 posts from March 1 to April 1?" = 30%
- "Will CZ post 180-199 posts from March 1 to April 1?" = 20%

These bins form a **probability distribution** that must sum to ~100%. When they don't, individual bins are mispriced. This skill also detects individual bin anomalies where one bin deviates significantly from its neighbors.

## The Edge: Distribution Arbitrage for Post-Count Markets

In traditional markets, discrete outcome probabilities must sum to 1.0 -- this is a fundamental axiom. On Polymarket, each post-count range bin trades independently with its own order book and liquidity. Retail treats each bin as an isolated bet without checking the full distribution.

### Violation Type 1: Sum Deviation

All bins for a (person, date_range) must sum to ~100%:

```
P(140-159) + P(160-179) + P(180-199) + P(200+) + ... = 100%
```

If the sum is 108%, at least one bin is overpriced -- sell NO on the highest-priced bin. If the sum is 92%, at least one bin is underpriced -- buy YES on the lowest-priced bin.

### Violation Type 2: Neighbor Anomaly

Individual bins that are much higher or lower than their adjacent bins indicate local mispricing:

```
P(140-159) = 25%, P(160-179) = 55%, P(180-199) = 20%
```

The 160-179 bin at 55% is anomalously high relative to its neighbors at 25% and 20%.

## Why This Works

1. **Retail trades in silos** -- most users view each post-count bin independently and don't cross-reference the full distribution
2. **No market maker enforcing consistency** -- unlike bookmakers who balance their book, Polymarket has no mechanism to keep bins summing to 100%
3. **Mathematical, not opinion** -- the violations are provable inconsistencies in the probability axioms
4. **Multiple persons, recurring periods** -- CZ, Khamenei, Trump, Musk, and others create a broad opportunity surface across overlapping date ranges

## Signal Logic

1. Discover all social media post-count range markets via keyword search + `get_markets(limit=200)` fallback
2. Parse each question: extract person, post-count range (low-high), and date range
3. Group into distributions by (person, date_range)
4. For each distribution with 2+ bins:
   - Check if bins sum to ~100% (tolerance configurable via `SIMMER_MIN_VIOLATION`)
   - If sum > 105%: sell NO on the highest-priced bin (most overpriced)
   - If sum < 95%: buy YES on the lowest-priced bin (most underpriced)
   - Check neighbor anomalies (bins deviating from adjacent bins by > 2x tolerance)
5. Rank violations by magnitude
6. Trade only violations that also pass threshold gates (`YES_THRESHOLD` / `NO_THRESHOLD`)
7. Size by conviction (violation magnitude + threshold distance), not flat amount

### Remix Signal Ideas

- **Twitter/X API v2**: Pull real-time post counts per account — compare current posting velocity against the market's implied range to detect when a bin is stale
- **Historical posting frequency model**: Build a Poisson/negative-binomial model from 90 days of posting data per person — the model's CDF gives you a fair price for each bin, and any bin deviating >5% from model price is tradeable
- **Cross-person correlation**: CZ and Khamenei post frequencies may correlate with global events (crypto crashes, geopolitical escalation) — when one person's activity spikes, adjacent persons' bins may be underpriced
- **Time-of-week patterns**: Most public figures post more on weekdays — if you're halfway through the measurement period and the cumulative count is tracking toward a specific bin, bins far from that trajectory are overpriced
- **Sentiment/topic analysis**: Use NLP to detect if a person is in a "high-activity mode" (responding to controversy, product launch) — this predicts higher post counts and shifts the distribution

## Supported Persons

CZ (Changpeng Zhao), Khamenei (Ali Khamenei), Trump (Donald Trump), Musk (Elon Musk), Vitalik (Vitalik Buterin).

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day) |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_MIN_VIOLATION` | `0.05` | Min distribution deviation before trading (5%) |

## Edge Thesis

Social media post-count markets on Polymarket are structured as discrete probability distributions. Each range bin trades independently, but they are mathematically constrained to sum to 100%. When retail order flow pushes individual bins without propagating to the full distribution, the sum deviates -- creating pure mathematical arbitrage. This skill reconstructs the distribution, finds where the axioms break, and trades the repair.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
