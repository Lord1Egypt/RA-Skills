---
name: polymarket-copy-early-mover-trader
description: Identifies which whale wallet consistently enters markets first before others follow. Copies the lead indicator whale's fresh positions before the herd pushes prices away. The edge is getting in early alongside the most predictive wallet.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Copy Early Mover Trader
  difficulty: advanced
---

# Copy Early Mover Trader

> **This is a template.**
> The default signal identifies the single most predictive "lead indicator" whale wallet -- the one that consistently enters markets before other whales follow -- and copies its freshest positions.
> The skill handles all the plumbing (leaderboard scraping, activity fetching, timeline construction, early-mover detection, signal validation). Your agent provides the alpha by tuning window and freshness parameters.

## Strategy Overview

Not all whale wallets are created equal. Some consistently move first into markets, and other whales follow within hours. This skill finds that lead indicator wallet and copies its fresh entries before the herd pushes prices away.

1. **Discover** top wallets from the predicting.top leaderboard
2. **Fetch** recent trade activity for each wallet
3. **Build** a per-market entry timeline: who entered first, who followed
4. **Score** each wallet by how often it was the confirmed first mover (lead score)
5. **Find** fresh positions from the top early mover(s) that haven't been crowded yet
6. **Validate** each copy trade against conviction-based thresholds with a lead-score boost
7. **Execute** trades on markets where the early mover's direction aligns with the base signal

## The Edge: First-Mover Price Advantage

When a whale enters a market, the price moves. The first whale in gets the best price; followers push it further in the same direction. By identifying *who* tends to move first -- and confirming that followers actually pile in -- this skill isolates the most predictive wallet and copies its freshest entries before the crowd.

### Signal Logic

```
Leaderboard (top N wallets)
    |
    v
Fetch recent BUY activity per wallet
    |
    v
Build entry timeline per market:
  - Group BUY trades by market title
  - Sort by timestamp (earliest first)
    |
    v
For each market:
  - First entry = early mover candidate
  - Count followers entering same side within EARLY_WINDOW_HOURS
  - Track per-wallet lead score (markets led across all history)
    |
    v
Filter: followers >= MIN_FOLLOWERS AND entry < FRESHNESS_HOURS old
    |
    v
Find fresh entries from top early mover(s):
  - Positions opened very recently by the lead wallet
  - These are the entries where followers haven't piled in yet
    |
    v
Match to Simmer markets -> compute_early_mover_signal:
  - Base signal must align with mover direction
  - Lead score boost: mult = 1 + min(0.4, lead_score * 0.1)
  - Conviction = min(1.0, base_conviction * lead_mult)
  - Size = max(MIN_TRADE, conviction * MAX_POSITION)
    |
    v
Execute trade
```

### Why This Works

- **Information asymmetry**: The first whale into a market often has proprietary information or superior analysis. Followers are reacting to the whale's move, not the underlying signal.
- **Price impact**: Each follower pushes the price further, creating slippage. Being early means getting the pre-impact price.
- **Lead score validation**: A wallet that was first once could be lucky. A wallet that was first in 5+ markets with confirmed followers is a genuine lead indicator.
- **Freshness filter**: Only copies positions opened within the last N hours, ensuring the entry price hasn't already been pushed away by followers.
- **Conviction alignment**: The early mover's direction must agree with the base conviction signal, preventing blind copying into overpriced markets.

### Example Dashboard

```
  EARLY MOVER DASHBOARD
  ================================================================
  Wallet         | LeadScore | MktsLed | AvgFollowers
  ----------------------------------------------------------------
  0xabc1234567.. |         7 |       4 |          2.5
  0xdef8901234.. |         4 |       3 |          1.7
  0x567890abcd.. |         2 |       2 |          1.0
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
| EARLY_WINDOW_HOURS | 6h | How close a follower must enter to confirm the early mover |
| MIN_FOLLOWERS | 1 | Minimum followers required to validate a lead signal |
| FRESHNESS_HOURS | 48h | Only copy positions opened within this window |
| context_ok() | ON | Prevents exceeding max open positions |

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
| `SIMMER_EARLY_WINDOW_HOURS` | 6 | Hours after first entry to count as follower |
| `SIMMER_MIN_FOLLOWERS` | 1 | Min whale followers to confirm lead signal |
| `SIMMER_FRESHNESS_HOURS` | 48 | Max age of position to copy (hours) |
| `SIMMER_LEADERBOARD_LIMIT` | 15 | Top N wallets to scan from leaderboard |

## Remix Ideas

- **Category-specific movers**: Only track early movers in crypto markets, or politics, or sports
- **Lead score decay**: Weight recent lead events more heavily than older ones
- **Contrarian mode**: When the lead wallet exits a position, take the opposite side
- **Multi-mover consensus**: Require 2+ early movers to agree on direction before copying
- **Follower velocity**: Weight signals higher when followers pile in faster (shorter time gap)
- **Size-weighted leads**: A whale that moves first with $10k is more meaningful than one with $100
- **Exit signal**: When the early mover exits, auto-close the copied position

## Dependency

Requires `simmer-sdk` (pip install simmer-sdk) and a valid `SIMMER_API_KEY`.
