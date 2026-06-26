---
name: polymarket-whale-contrarian-trader
description: Detects smart money divergence where top-performing whale wallets take positions opposite to retail consensus. When markets are at probability extremes but whales bet against the crowd, trades with the whales using conviction-boosted sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Whale Contrarian Trader
  difficulty: advanced
---

# Whale Contrarian Trader

## Strategy Overview

This skill exploits information asymmetry between retail traders and top-performing whales on Polymarket. When a market's probability sits at an extreme (above 70% or below 30%), it reflects strong retail consensus. If multiple top leaderboard wallets are simultaneously taking the **opposite** side, it signals that smart money disagrees with the crowd.

The skill fetches the public Polymarket leaderboard, tracks recent whale activity, cross-references it against markets at probability extremes, and trades in the whale's direction when enough whales independently oppose retail consensus.

## Signal Logic

1. **Fetch leaderboard** -- Pull top 50 wallet addresses from the public leaderboard API.
2. **Fetch wallet activity** -- For each whale, retrieve recent trades from the Polymarket data API.
3. **Identify extreme markets** -- Markets where probability > CONTRARIAN_THRESHOLD (70%) or < 1 - CONTRARIAN_THRESHOLD (30%).
4. **Detect opposition** -- For each extreme market, count whales trading the opposite direction from retail consensus.
5. **Generate signal** -- If at least MIN_WHALE_OPPOSITION whales (default: 2) are on the contrarian side, generate a trade signal in the whale's direction.
6. **Conviction sizing** -- Base conviction from threshold bands, boosted by a whale multiplier: `1.0 + min(0.4, (whale_count - 1) * 0.1)`.

## Edge Thesis

Whale wallets that appear on the Polymarket leaderboard have demonstrated sustained profitability. Their edge typically comes from:

- **Superior information**: Access to domain experts, proprietary data, or faster news processing.
- **Better models**: Quantitative models that more accurately estimate true probabilities.
- **Behavioral discipline**: Less susceptible to the narrative biases that push retail to extremes.

When retail has pushed a market to a probability extreme (the crowd is very confident), and multiple whales independently disagree, the expected value of following smart money is positive. The more whales that converge on the contrarian side, the stronger the signal.

This is not a guarantee -- whales can be wrong. But systematic tracking of whale-vs-retail divergence at extremes has a positive expected edge over time.

## Remix Ideas

- **Sector-specific whale tracking**: Filter whale activity to specific market categories (politics, crypto, sports) where certain whales have demonstrated domain expertise.
- **Whale quality weighting**: Weight signals by whale PnL rank -- a top-5 whale opposing retail is stronger than a top-50 whale.
- **Time decay**: Weight recent whale trades more heavily than older ones (e.g., last 24h vs last 7 days).
- **Volume-weighted opposition**: Instead of counting whale wallets, sum the dollar volume of contrarian whale trades.
- **Momentum confirmation**: Only trade if the whale contrarian activity is increasing over time (more whales joining the opposite side).

## Safety

| Guard | Default | Purpose |
|---|---|---|
| Paper mode | ON | `--live` flag required for real trades |
| MAX_SPREAD | 8% | Skip illiquid markets |
| MIN_DAYS | 7 | Avoid near-resolution noise |
| MAX_POSITIONS | 6 | Cap portfolio exposure |
| MIN_VOLUME | $5,000 | Skip thin markets |
| MIN_WHALE_OPPOSITION | 2 | Require multiple independent whale signals |
| Flip-flop guard | ON | SDK discipline check |
| Slippage guard | 15% | SDK slippage check |

## Tunables

| Env Var | Default | Description |
|---|---|---|
| SIMMER_MAX_POSITION | 40 | Max position size in USD |
| SIMMER_MIN_TRADE | 5 | Min trade size in USD |
| SIMMER_MIN_VOLUME | 5000 | Min market volume in USD |
| SIMMER_MAX_SPREAD | 0.08 | Max bid-ask spread |
| SIMMER_MIN_DAYS | 7 | Min days until resolution |
| SIMMER_MAX_POSITIONS | 6 | Max simultaneous positions |
| SIMMER_YES_THRESHOLD | 0.38 | YES threshold for conviction sizing |
| SIMMER_NO_THRESHOLD | 0.62 | NO threshold for conviction sizing |
| SIMMER_CONTRARIAN_THRESHOLD | 0.70 | Probability extreme threshold (retail consensus) |
| SIMMER_MIN_WHALE_OPPOSITION | 2 | Min whales required on contrarian side |

## Dependency

- `simmer-sdk` (pip)
- `SIMMER_API_KEY` environment variable
