---
name: polymarket-copy-dynamic-roster-trader
description: Automatically discovers and ranks top Polymarket wallets from public leaderboards, evaluates rolling performance, and builds a dynamic copy roster. Feeds qualified wallets into Simmer SDK copytrading. Rotates in hot wallets and drops cold ones automatically.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Dynamic Roster Copytrader
  difficulty: advanced
---

# Dynamic Roster Copytrader

> **This is a template.**
> The default signal combines leaderboard discovery with rolling PnL evaluation to build a dynamic roster of top-performing wallets for copytrading.
> The skill handles all the plumbing (leaderboard scraping, wallet scoring, roster construction, copy execution, safeguards). Your agent provides the alpha by tuning roster parameters.

## Strategy Overview

Public leaderboards expose which Polymarket wallets are currently profitable. This skill automates the entire copytrading pipeline:

1. **Discover** top wallets from the predicting.top leaderboard
2. **Score** each wallet using SmartScore, win rate, and recent rolling PnL
3. **Build** a ranked roster of the best-performing wallets
4. **Copy** their positions via the Simmer SDK copytrading endpoint
5. **Rotate** the roster each run -- cold wallets drop out, hot newcomers get added

## The Edge: Adaptive Wallet Selection

Most copytrading tools track a fixed list of wallets. This skill treats the roster as a *living portfolio* that adapts to who is performing **right now**.

### Signal Logic

```
Leaderboard (30 wallets)
    |
    v
Evaluate each wallet:
  - SmartScore (from leaderboard)
  - Win rate (from leaderboard)
  - Rolling PnL (computed from data-api activity)
    |
    v
Combined score = 0.4 * norm_smart_score
               + 0.3 * norm_win_rate
               + 0.3 * norm_rolling_pnl
    |
    v
Sort by combined score, take top ROSTER_SIZE
Filter out wallets with rolling PnL < MIN_PNL
    |
    v
Feed roster into Simmer SDK copytrading endpoint
Validate each copy trade against conviction thresholds
Execute or skip based on market conditions
```

### Why This Works

- **Regime adaptation**: Wallets that were profitable last month may be losing now. Rolling PnL captures recent performance, not lifetime averages.
- **Multi-factor scoring**: SmartScore alone can be gamed. Combining it with actual win rate and realized PnL gives a more robust ranking.
- **Conviction filtering**: Copy trades are validated against YES/NO threshold bands, preventing blind copying into overpriced or neutral markets.
- **Whale exit detection**: The copytrading endpoint flags when tracked wallets are exiting positions, allowing the skill to avoid catching falling knives.

### Example Roster

| # | Wallet       | Score | WinRate | Rolling PnL | Status |
|---|-------------|-------|---------|-------------|--------|
| 1 | 0xabc12...  | 0.892 |  68.5%  |    $2,340   | HOT    |
| 2 | 0xdef34...  | 0.845 |  65.2%  |    $1,890   | HOT    |
| 3 | 0x789ab...  | 0.721 |  62.1%  |      $450   | HOT    |
| 4 | 0xcde56...  | 0.698 |  59.8%  |      $120   | WARM   |
| 5 | 0xfab78...  | 0.654 |  71.0%  |       $85   | WARM   |

## Safety

| Guard | Default | What it does |
|-------|---------|-------------|
| Paper mode | ON | No `--live` flag = simulated trades, zero risk |
| MAX_POSITION | $50 | Cap per-trade size |
| MIN_TRADE | $5 | Floor prevents trivially small orders |
| MAX_POSITIONS | 10 | Portfolio-level position limit |
| MAX_SPREAD | 10% | Skip illiquid markets |
| MIN_DAYS | 3 | Skip markets resolving too soon |
| YES/NO thresholds | 0.38/0.62 | Only copy trades within conviction bands |
| MIN_PNL | $0 | Filter out wallets with negative recent PnL |
| COPY_MAX_USD | $50 | Cap per copied position |
| COPY_MAX_TRADES | 10 | Limit trades per run to control exposure |
| buy_only | true | Only copies buy-side trades, no shorts |
| whale_exit_detect | true | Flags when wallets are exiting positions |
| context_ok() | ON | Prevents exceeding max open positions |

## Tunables

All parameters are configurable via `SIMMER_*` environment variables and the Simmer UI:

| Env Var | Default | Description |
|---------|---------|-------------|
| `SIMMER_MAX_POSITION` | 50 | Max position size in USD |
| `SIMMER_MIN_TRADE` | 5 | Min trade size in USD |
| `SIMMER_MIN_VOLUME` | 3000 | Min market volume in USD |
| `SIMMER_MAX_SPREAD` | 0.10 | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | 3 | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | 10 | Max open positions |
| `SIMMER_YES_THRESHOLD` | 0.38 | YES threshold for conviction filter |
| `SIMMER_NO_THRESHOLD` | 0.62 | NO threshold for conviction filter |
| `SIMMER_ROSTER_SIZE` | 5 | Max wallets in active roster |
| `SIMMER_MIN_PNL` | 0 | Min rolling PnL to qualify for roster |
| `SIMMER_COPY_MAX_USD` | 50 | Max USD per copied position |
| `SIMMER_COPY_MAX_TRADES` | 10 | Max trades per run |

## Remix Ideas

- **Category-specific rosters**: Only copy wallets that are profitable in crypto markets, or sports, or politics
- **Momentum overlay**: Weight the combined score by how much a wallet's PnL has *increased* in the last 24h vs. 7d
- **Anti-correlation filter**: Avoid copying wallets that all hold the same positions (diversification)
- **Decay weighting**: Give more weight to recent trades vs. older ones in the rolling PnL calculation
- **Exit signal**: When a roster wallet exits a position you copied, auto-exit too
- **Sharpe gating**: Require a minimum Sharpe ratio to filter out lucky gamblers

## Dependency

Requires `simmer-sdk` (pip install simmer-sdk) and a valid `SIMMER_API_KEY`.
