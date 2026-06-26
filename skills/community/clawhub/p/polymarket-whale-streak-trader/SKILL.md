---
name: polymarket-whale-streak-trader
description: Tracks rolling win rate per whale wallet and only follows wallets on a verified hot streak. Dynamically promotes and demotes wallets based on recent performance, ensuring you only copy currently-winning traders.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Whale Streak Trader
  difficulty: advanced
---

# Whale Streak Trader

## Strategy overview

Most whale-following strategies treat all top wallets equally. This skill adds a critical filter: **only follow wallets currently on a hot streak**. Each run evaluates every leaderboard wallet's rolling win rate over their most recent trades and classifies them into three tiers:

| Status | Condition | Action |
|--------|-----------|--------|
| **HOT** | Win rate >= `HOT_WIN_RATE` (default 65%) | Follow positions, apply streak boost |
| **WARM** | Between cold and hot thresholds | Ignore -- not confident enough |
| **COLD** | Win rate <= `COLD_WIN_RATE` (default 45%) | Drop entirely -- wallet is underperforming |

This creates a **dynamic roster** that adapts every run. A whale who was HOT last week but started losing gets demoted automatically. A previously WARM wallet that hits a winning streak gets promoted.

## Signal logic

### Rolling win rate calculation

For each wallet, the skill fetches recent activity and processes the last N trades (configurable via `STREAK_WINDOW`):

1. Track entry prices per (market, outcome) pair
2. When a sell or redeem event occurs, compare exit price to average entry price
3. Count wins (exit > entry) and losses (exit <= entry)
4. Compute `win_rate = wins / (wins + losses)`

### Streak-boosted conviction

When a HOT wallet's position aligns with the standard conviction signal:

1. Base conviction from standard YES/NO threshold bands
2. Streak multiplier: `1 + min(0.5, (win_rate - HOT_WIN_RATE) / (1 - HOT_WIN_RATE))`
3. Final conviction: `min(1.0, base_conviction * streak_mult)`
4. Size: `max(MIN_TRADE, round(conviction * MAX_POSITION, 2))`

A whale with 65% win rate (at threshold) gets 1.0x multiplier. A whale with 82.5% gets 1.25x. A whale at 100% gets the max 1.5x.

### Alignment requirement

The skill only trades when:
- The whale's position direction (YES/NO) matches the standard conviction signal direction
- The market passes spread, volume, and days-to-resolution gates
- The context check (flip-flop, slippage) passes

## Edge thesis

Raw whale-following is noisy. Even the best traders go through cold streaks, strategy shifts, or experiment with new approaches. By filtering to only currently-hot wallets, this skill:

- **Removes noise** from lucky traders who got on the leaderboard by chance
- **Avoids degraded traders** whose edge may have eroded
- **Captures momentum** -- traders on winning streaks often have identified a temporary market inefficiency
- **Self-corrects** -- no manual curation needed; the roster updates every run

The streak boost further rewards consistency: a wallet with 80% win rate over 30 trades gets more capital allocated than one barely clearing the 65% threshold.

## Remix ideas

- Weight positions by whale PnL magnitude, not just win rate
- Add a "comeback" tier: wallets that were COLD but are now rapidly improving
- Cross-reference multiple whale positions on the same market for consensus scoring
- Track streak duration (how many consecutive runs a wallet has been HOT) as an additional signal
- Add sector-specific whale tracking (crypto whales, politics whales, etc.)

## Safety and execution

| Parameter | Default | Description |
|-----------|---------|-------------|
| Paper mode | Yes | Default behavior, no real money at risk |
| `--live` flag | Required | Must explicitly pass to trade real funds |
| Spread gate | 10% | Skips illiquid markets |
| Volume gate | $3,000 | Skips thin markets |
| Days gate | 5 days | Avoids near-resolution markets |
| Flip-flop check | On | Prevents rapid position reversals |
| Slippage check | 15% | Skips high-slippage markets |
| Max positions | 8 | Hard cap on concurrent positions |

## Credentials

| Variable | Required | Description |
|----------|----------|-------------|
| `SIMMER_API_KEY` | Yes | Simmer SDK API key |

## Tunables

All tunables are prefixed with `SIMMER_` and adjustable from the Simmer UI.

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMMER_MAX_POSITION` | 40 | Max position size in USD |
| `SIMMER_MIN_TRADE` | 5 | Min trade size in USD |
| `SIMMER_MIN_VOLUME` | 3000 | Min market volume in USD |
| `SIMMER_MAX_SPREAD` | 0.10 | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | 5 | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | 8 | Max open positions |
| `SIMMER_YES_THRESHOLD` | 0.38 | YES signal threshold |
| `SIMMER_NO_THRESHOLD` | 0.62 | NO signal threshold |
| `SIMMER_HOT_WIN_RATE` | 0.65 | Min win rate to classify as HOT |
| `SIMMER_COLD_WIN_RATE` | 0.45 | Max win rate before classified as COLD |
| `SIMMER_STREAK_WINDOW` | 30 | Number of recent trades to evaluate |
| `SIMMER_LEADERBOARD_LIMIT` | 20 | Top N wallets to scan from leaderboard |

## Dependency

- `simmer-sdk` (pip)
