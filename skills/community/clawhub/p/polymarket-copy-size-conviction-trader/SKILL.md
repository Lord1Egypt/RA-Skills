---
name: polymarket-copy-size-conviction-trader
description: Weights copytrading by portfolio concentration -- a whale committing 30% of capital to one market signals far more conviction than 2% spread across many. Copies high-concentration positions with proportionally boosted sizing.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Copy Size Conviction Trader
  difficulty: advanced
---

# Copy Size Conviction Trader

> **This is a template.**
> The default signal uses portfolio concentration as a proxy for whale conviction. When a top trader commits a large fraction of their capital to a single market, that is a stronger signal than raw position size or trade count.
> The skill handles all plumbing (leaderboard scraping, activity reconstruction, concentration analysis, signal boosting, safeguards). Your agent provides the alpha by tuning concentration thresholds.

## Strategy Overview

Not all whale positions are equal. A trader who puts $100K into a market might be spreading $5M across 50 markets (low conviction) or concentrating $300K total into 3 markets (high conviction). This skill distinguishes between the two.

1. **Discover** top wallets from the predicting.top leaderboard
2. **Reconstruct** each wallet's portfolio from on-chain trade activity
3. **Measure** portfolio concentration: position_cost / total_portfolio_cost per market
4. **Filter** positions where concentration exceeds MIN_CONCENTRATION threshold
5. **Boost** trade sizing proportional to whale conviction level
6. **Validate** every trade against conviction-based YES/NO threshold bands

## The Edge: Concentration as Conviction

Most copytrading tools treat all whale positions equally. A $50K position from a $5M whale (1% concentration) gets the same weight as a $50K position from a $150K whale (33% concentration). The second whale is clearly more convicted.

### Signal Logic

```
Leaderboard (top N wallets)
    |
    v
For each wallet:
  Fetch 200 most recent trades
  Reconstruct open positions (buys - sells per market)
  Compute concentration = position_cost / total_portfolio_cost
    |
    v
Across all wallets:
  Find markets where any whale has concentration >= MIN_CONCENTRATION
  Aggregate: market -> [(wallet, side, concentration, cost), ...]
  Sort by max concentration descending
    |
    v
For each high-conviction market:
  Match to Simmer market catalog
  Run compute_signal() for base conviction (YES/NO threshold bands)
  Verify whale side aligns with signal direction
  Apply concentration multiplier:
    conc_mult = 1 + min(CONCENTRATION_MULT - 1, concentration / 0.5)
    whale_boost = min(0.3, (num_whales - 1) * 0.1)  [if multiple whales agree]
    boosted_conviction = min(1.0, base_conviction * conc_mult + whale_boost)
    size = max(MIN_TRADE, round(boosted_conviction * MAX_POSITION, 2))
    |
    v
Execute or paper-trade
```

### Why This Works

- **Concentration is observable**: Unlike sentiment or conviction surveys, portfolio concentration is computed directly from on-chain data. It cannot be faked without moving real capital.
- **Asymmetric information**: Whales who concentrate are betting they know something. A 30% portfolio allocation implies the whale expects significant edge in that specific market.
- **Multi-whale convergence**: When multiple independent whales concentrate in the same market, the signal compounds. This is harder to game than a single whale's activity.
- **Conviction alignment**: The skill only trades when whale concentration aligns with the base YES/NO threshold signal, preventing blind copying into neutral or overpriced markets.

### Example Dashboard

| Market                              | Whale        | Conc  | Side | Size   |
|-------------------------------------|-------------|-------|------|--------|
| Will X happen by June 2026?         | 0xabc12...  |  32%  | yes  | $4,200 |
| Federal rate cut in Q3?             | 0xdef34...  |  28%  | no   | $8,100 |
| Federal rate cut in Q3?             | 0x789ab...  |  15%  | no   | $2,900 |
| Bitcoin above $150K by July?        | 0xcde56...  |  22%  | yes  | $6,500 |
| Major tech IPO in 2026?             | 0xfab78...  |  11%  | yes  | $1,800 |

In this example, "Federal rate cut in Q3?" has two whales with high concentration on the same side -- the multi-whale boost kicks in for stronger conviction sizing.

## Safety

| Guard | Default | What it does |
|-------|---------|-------------|
| Paper mode | ON | No `--live` flag = simulated trades, zero risk |
| MAX_POSITION | $50 | Cap per-trade size |
| MIN_TRADE | $5 | Floor prevents trivially small orders |
| MAX_POSITIONS | 8 | Portfolio-level position limit |
| MAX_SPREAD | 10% | Skip illiquid markets |
| MIN_DAYS | 5 | Skip markets resolving too soon |
| MIN_VOLUME | $3,000 | Skip thin markets |
| YES/NO thresholds | 0.38/0.62 | Only trade within conviction bands |
| MIN_CONCENTRATION | 10% | Ignore positions below this portfolio share |
| Side alignment | ON | Whale side must match signal direction |
| context_ok() | ON | Prevents exceeding max open positions |

## Tunables

All parameters are configurable via `SIMMER_*` environment variables and the Simmer UI:

| Env Var | Default | Description |
|---------|---------|-------------|
| `SIMMER_MAX_POSITION` | 50 | Max position size in USD |
| `SIMMER_MIN_TRADE` | 5 | Min trade size in USD |
| `SIMMER_MIN_VOLUME` | 3000 | Min market volume in USD |
| `SIMMER_MAX_SPREAD` | 0.10 | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | 5 | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | 8 | Max open positions |
| `SIMMER_YES_THRESHOLD` | 0.38 | YES threshold for conviction bands |
| `SIMMER_NO_THRESHOLD` | 0.62 | NO threshold for conviction bands |
| `SIMMER_MIN_CONCENTRATION` | 0.10 | Min portfolio concentration to qualify |
| `SIMMER_CONCENTRATION_MULT` | 2.0 | Max multiplier from concentration |
| `SIMMER_LEADERBOARD_LIMIT` | 15 | Top N wallets to analyze |

## Remix Ideas

- **Sector concentration**: Only count concentration within a category (crypto, politics, sports) to find domain-specialist whales
- **Concentration velocity**: Track how concentration *changes* over time -- a whale increasing from 10% to 30% is actively building conviction
- **Inverse concentration**: Fade whales who are *decreasing* concentration (selling down), as this signals loss of conviction
- **Concentration clustering**: Find markets where 3+ whales all have >15% concentration -- crowd conviction premium
- **Time-weighted concentration**: Weight recent positions more heavily than older ones when computing portfolio share
- **Whale-relative sizing**: Instead of a fixed multiplier, size proportional to the whale's actual dollar concentration

## Dependency

Requires `simmer-sdk` (pip install simmer-sdk) and a valid `SIMMER_API_KEY`.
