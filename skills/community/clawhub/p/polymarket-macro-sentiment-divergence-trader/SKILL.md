---
name: polymarket-macro-sentiment-divergence-trader
description: Detects macro sentiment divergence across Polymarket prediction markets. When positive-sentiment categories (sports winners, tech milestones, entertainment, crypto UP) and negative-sentiment categories (geopolitical escalation, catastrophe, disease outbreaks, crypto DOWN) are both priced high simultaneously, that is logically inconsistent. Trades against the stale side of the divergence.
metadata:
  author: snetripp
  version: "1.0"
  displayName: Macro Sentiment Divergence Trader
  difficulty: advanced
---

# Macro Sentiment Divergence Trader

> **This is a template.**
> The default signal classifies markets into positive/negative sentiment buckets, computes a divergence index, and trades against the stale side when macro sentiment is logically inconsistent.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Prediction markets collectively reflect macro sentiment. "Positive" markets (sports favorites winning, tech milestones being hit, crypto going UP, entertainment events succeeding) and "negative" markets (geopolitical escalation, catastrophe events, disease outbreaks, crypto going DOWN) should not both be priced high simultaneously. If the average probability of positive-sentiment markets is 0.65 and the average probability of negative-sentiment markets is 0.60, both sides are saying "likely" -- but the world cannot be both great and terrible at the same time. One side is stale.

The structural edge: retail traders price individual markets in isolation. They don't cross-reference whether their collective bets are internally consistent. A sports fan pricing "Lakers win championship" at 70% is not checking whether "major recession in 2026" is also at 65%. But those two bets are in tension -- championship attendance, sponsorship revenue, and betting volumes all correlate with economic health.

The divergence formula: `positive_index + negative_index - 1.0`. When both indices exceed 0.5, the sum exceeds 1.0 and the divergence is positive. A divergence of 0.15+ means the collective market is pricing in logically contradictory macro states.

## Signal Logic

### Default Signal: Sentiment Divergence Detection

1. Scan ALL active markets via `get_markets(limit=200)` plus targeted keyword search
2. Classify each market as positive-sentiment, negative-sentiment, or unclassified
3. Compute `positive_index` = average probability of positive-sentiment markets
4. Compute `negative_index` = average probability of negative-sentiment markets
5. `divergence = positive_index + negative_index - 1.0`
6. If divergence > `SIMMER_DIVERGENCE_THRESHOLD` (default 0.15):
   - Identify which side has LESS recent movement (the "stale" side)
   - Trade AGAINST the stale side -- those markets haven't repriced to new information
7. Conviction-based sizing with divergence magnitude as a boost factor

### Sentiment Classification

**Positive sentiment** (things going well):
- Sports favorites winning (champion, victory, gold medal, Super Bowl, finals)
- Tech milestones (launch, milestone, breakthrough, IPO, market cap, trillion)
- Entertainment success (box office, Oscar, Grammy, streaming record)
- Crypto UP (bitcoin above, btc above, new all-time high)

**Negative sentiment** (things going badly):
- Geopolitical escalation (war, invasion, conflict, sanctions, military, nuclear)
- Catastrophe events (hurricane, earthquake, tsunami, wildfire, flood, famine)
- Disease outbreaks (pandemic, epidemic, outbreak, bird flu, covid)
- Economic doom (recession, crash, collapse, default, bankruptcy)
- Crypto DOWN (bitcoin below, btc below)

### Stale Side Detection

The side with less recent price movement (closer to 50% on average) is considered stale -- it hasn't repriced to whatever new information caused the other side to move. Distance from 50% serves as a proxy for recency of directional movement.

### Why This Works

- Retail prices individual markets without cross-referencing macro consistency
- Positive and negative macro states are inversely correlated in reality
- When both sides are priced high, at least one side is wrong
- The stale side (less recent movement) is the one that hasn't absorbed new info
- Mean reversion of the stale side toward consistency is the trade

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` -- nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_DIVERGENCE_THRESHOLD` | `0.15` | Min divergence score to trigger trades |
| `SIMMER_MIN_BUCKET_SIZE` | `3` | Min markets required per sentiment bucket |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
