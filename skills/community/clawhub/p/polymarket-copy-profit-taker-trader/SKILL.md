---
name: polymarket-copy-profit-taker-trader
description: Detects when top whale wallets start taking profits by reducing winning positions, then identifies what markets they rotate INTO. Follows the smart money flow from mature positions into fresh opportunities. Avoids markets whales are exiting.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Copy Profit Taker Trader
  difficulty: advanced
---

# Copy Profit Taker Trader

> **This is a template.**
> The default signal detects whale profit-taking patterns (selling parts of winning positions) and tracks where the freed capital rotates into new markets.
> The skill handles all the plumbing (leaderboard scraping, activity fetching, position change analysis, rotation detection, signal validation). Your agent provides the alpha by tuning thresholds and rotation windows.

## Strategy Overview

When a profitable whale starts reducing exposure in a winning position, the upside is likely exhausted. But the capital doesn't disappear -- it flows into new opportunities. This skill tracks both sides of the equation:

1. **Discover** top wallets from the predicting.top leaderboard
2. **Fetch** full recent trade activity for each wallet (buys AND sells)
3. **Analyze** position changes: for each market, compute buy_total, sell_total, and sell_ratio
4. **Classify** positions: TAKING_PROFIT (sell_ratio >= threshold), ACCUMULATING (low sell_ratio + recent buys), or HOLDING
5. **Detect rotations**: same wallet taking profit in market A AND accumulating in market B within the time window
6. **Validate** rotation targets against conviction-based thresholds with a rotation boost
7. **Execute** trades on rotation entry markets where direction aligns with base signal
8. **Fallback** to standard conviction signals on accumulating markets not being exited

## The Edge: Profit-Taking as Signal + Rotation Tracking

### Why Profit-Taking Matters

Whales don't sell winners randomly. When a top wallet that built a large position starts selling 30%+ of it, they're telling you the easy money is gone. Buying into markets where smart money is exiting is the most common retail mistake.

### Why Rotation Matters

The capital from exits has to go somewhere. When the same wallet sells market A and immediately buys market B, that's a rotation -- and the entry into market B carries the same information edge that made market A profitable in the first place. Coordinated rotations (multiple whales doing the same) amplify the signal.

### Signal Logic

```
Leaderboard (top N wallets)
    |
    v
Fetch full trade history per wallet (buys + sells)
    |
    v
Analyze position changes per market:
  - buy_total, sell_total, sell_ratio = sold/bought
  - Classify: TAKING_PROFIT / ACCUMULATING / HOLDING
    |
    v
Detect rotations:
  - Same wallet: TAKING_PROFIT in market A + ACCUMULATING in market B
  - Within ROTATION_WINDOW_HOURS
  - entry_conviction = new_position_size / exit_value
    |
    v
For rotation entry targets:
  - Match to Simmer market
  - compute_rotation_signal:
    - Base signal must align with entry direction
    - rot_mult = 1 + min(0.4, conviction * 0.3 + (whales-1) * 0.1)
    - Size = max(MIN_TRADE, conviction * MAX_POSITION)
    |
    v
Fallback: standard compute_signal on accumulating (non-exit) markets
    |
    v
Execute trades (paper by default)
```

### Example Dashboards

```
  TAKE-PROFIT DASHBOARD
  ====================================================================
  Wallet         | Market                         | SellRatio | Status
  --------------------------------------------------------------------
  0xabc1234567.. | Will BTC hit $100k by July?    |       42% | TAKING_PROFIT
  0xdef8901234.. | Will ETH merge succeed?        |       65% | TAKING_PROFIT

  ROTATION DASHBOARD
  ====================================================================
  Wallet         | Exit Market            | Entry Market           | Side
  --------------------------------------------------------------------
  0xabc1234567.. | Will BTC hit $100k..   | Will SOL flip ETH..    | buy
  0xdef8901234.. | Will ETH merge suc..   | Will DOGE reach $1..   | buy
```

## Safety

| Guard | Default | What it does |
|-------|---------|-------------|
| Paper mode | ON | No `--live` flag = simulated trades, zero risk |
| MAX_POSITION | $40 | Cap per-trade size |
| MIN_TRADE | $5 | Floor prevents trivially small orders |
| MAX_POSITIONS | 8 | Portfolio-level position limit |
| MAX_SPREAD | 10% | Skip illiquid markets |
| MIN_DAYS | 5 | Skip markets resolving too soon |
| MIN_VOLUME | $3,000 | Skip low-volume markets |
| YES/NO thresholds | 0.38/0.62 | Only trade within conviction bands |
| PROFIT_TAKE_THRESHOLD | 30% | Sell ratio required to classify as take-profit |
| ROTATION_WINDOW_HOURS | 48h | Time window to detect exit+entry as rotation |
| Exit market blacklist | ON | Never trades into markets whales are exiting |
| context_ok() | ON | Prevents exceeding max open positions |

## Credentials

Requires a valid `SIMMER_API_KEY` environment variable. No additional API keys needed -- the skill uses public leaderboard and data APIs.

## Tunables

All parameters are configurable via `SIMMER_*` environment variables and the Simmer UI:

| Env Var | Default | Description |
|---------|---------|-------------|
| `SIMMER_MAX_POSITION` | 40 | Max position size in USD |
| `SIMMER_MIN_TRADE` | 5 | Min trade size in USD |
| `SIMMER_MIN_VOLUME` | 3000 | Min market volume in USD |
| `SIMMER_MAX_SPREAD` | 0.10 | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | 5 | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | 8 | Max open positions |
| `SIMMER_YES_THRESHOLD` | 0.38 | YES threshold for conviction filter |
| `SIMMER_NO_THRESHOLD` | 0.62 | NO threshold for conviction filter |
| `SIMMER_PROFIT_TAKE_THRESHOLD` | 0.30 | Sell ratio to classify as take-profit |
| `SIMMER_ROTATION_WINDOW_HOURS` | 48 | Hours to detect exit+entry as rotation |
| `SIMMER_LEADERBOARD_LIMIT` | 15 | Top N wallets to scan from leaderboard |

## Remix Ideas

- **Category-specific rotations**: Only track rotations within crypto or politics markets
- **Multi-timeframe analysis**: Compare 24h vs 7d sell ratios to distinguish panic selling from strategic profit-taking
- **Partial-exit scaling**: Instead of binary TAKING_PROFIT, scale avoidance by sell_ratio (50% exit = half-avoid)
- **Contrarian exit plays**: When ALL whales exit a market, the price may overshoot down -- contrarian entry
- **Rotation chain tracking**: Follow multi-hop rotations (A -> B -> C)
- **Size-weighted rotations**: Weight rotation signals by dollar amount, not just count
- **Exit velocity**: Fast exits (large sells in short time) are more urgent signals than gradual unwinding

## Dependency

Requires `simmer-sdk` (pip install simmer-sdk) and a valid `SIMMER_API_KEY`.
