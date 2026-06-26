---
name: polymarket-whale-momentum-trader
description: Detects when multiple top-performing whale wallets independently enter the same Polymarket market in the same direction within a configurable time window. When 2+ whales agree, trades with conviction-boosted sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Whale Momentum Trader
  difficulty: advanced
---

# Whale Momentum Trader

## Strategy Overview

This skill monitors the top-performing wallets on Polymarket (via the predicting.top leaderboard) and detects **momentum consensus** -- when multiple whale wallets independently enter the same market on the same side within a short time window.

The core insight: when 2+ top-performing traders independently decide to buy the same side of a market within 48 hours, they are likely reacting to the same underlying information edge. This convergence is a stronger signal than any single whale trade.

## Signal Logic

```
1. Fetch leaderboard    -> Top N wallets from predicting.top
2. Fetch activity       -> Recent trades per wallet from Polymarket data API
3. Build momentum map   -> For each market: count YES wallets vs NO wallets
4. Filter signals       -> Markets with MIN_WHALES+ wallets on the same side
5. Match markets        -> Find corresponding Simmer market for each signal
6. Boosted signal       -> Conviction-based sizing + whale consensus boost
7. Trade                -> Place order if whale direction aligns with threshold signal
```

## Edge Thesis

Independent whale agreement is a strong conviction signal because:

- **Information asymmetry**: Top leaderboard wallets consistently outperform. They have better information pipelines, faster reaction times, and deeper domain expertise.
- **Independence filter**: Two wallets trading the same direction within 48 hours suggests they are both reacting to the same underlying catalyst, not copying each other.
- **Consensus premium**: A single whale trade could be noise or portfolio rebalancing. Multiple whales agreeing filters out idiosyncratic trades and isolates genuine conviction.
- **Timing edge**: By monitoring activity within a lookback window (default 48h), the skill catches momentum before it fully reprices into the market.

The conviction boost formula rewards stronger consensus:
- 2 whales: +15% conviction boost
- 3 whales: +30% conviction boost
- 4+ whales: +45-50% conviction boost (capped at 50%)

Critically, the skill only trades when the whale direction **aligns** with the threshold signal (YES below YES_THRESHOLD, NO above NO_THRESHOLD). This prevents chasing whale momentum into already-priced territory.

## Remix Ideas

- **Sector filtering**: Only follow whale consensus in specific market categories (crypto, politics, sports) where whale edge is strongest.
- **Volume weighting**: Weight the momentum signal by USD volume, not just wallet count. A whale putting $50K in is a stronger signal than one putting $500.
- **Decay weighting**: Apply time decay to activities -- trades from 2 hours ago are stronger signals than trades from 46 hours ago.
- **Anti-correlation filter**: If whale A and whale B historically trade opposite directions, discount their "agreement" (they may be the same entity hedging).
- **Leaderboard recency**: Weight wallets by their recent performance (last 30 days) rather than all-time rank.

## Safety

| Control | Setting |
|---------|---------|
| Default mode | Paper (sim) -- zero financial risk |
| Live trading | Requires explicit `--live` flag |
| Max position | $40 per trade (tunable) |
| Min trade | $5 floor prevents trivial orders |
| Max positions | 8 concurrent (tunable) |
| Spread gate | Skips markets with spread > 10% |
| Days gate | Skips markets resolving in < 5 days |
| Flip-flop guard | SDK context check prevents reversals |
| Slippage guard | Skips if slippage > 15% |
| Alignment check | Only trades when whale direction matches threshold signal |

## Tunables

| Env Var | Default | Description |
|---------|---------|-------------|
| `SIMMER_MAX_POSITION` | 40 | Max position size in USD |
| `SIMMER_MIN_TRADE` | 5 | Min trade size in USD |
| `SIMMER_MIN_VOLUME` | 3000 | Min market volume in USD |
| `SIMMER_MAX_SPREAD` | 0.10 | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | 5 | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | 8 | Max concurrent positions |
| `SIMMER_YES_THRESHOLD` | 0.38 | Buy YES below this probability |
| `SIMMER_NO_THRESHOLD` | 0.62 | Buy NO above this probability |
| `SIMMER_MIN_WHALES` | 2 | Min whales agreeing for a signal |
| `SIMMER_LOOKBACK_HOURS` | 48 | Time window for momentum detection |
| `SIMMER_LEADERBOARD_LIMIT` | 15 | Number of top wallets to track |

## Dependencies

- **simmer-sdk**: Simmer trading SDK for market discovery, trading, and context checks.
- **predicting.top API**: Public leaderboard API for top Polymarket wallet addresses.
- **Polymarket Data API**: Public API for fetching wallet trading activity.

No additional pip packages required beyond `simmer-sdk`. All HTTP calls use Python's built-in `urllib`.
