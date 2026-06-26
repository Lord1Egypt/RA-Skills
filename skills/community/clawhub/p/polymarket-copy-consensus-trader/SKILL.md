---
name: polymarket-copy-consensus-trader
description: Only trades Polymarket markets where 3+ top whale wallets independently agree on direction. Filters out noisy single-wallet signals and focuses on high-conviction consensus among smart money. Conviction-boosted sizing scales with the number of agreeing whales.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Copy Consensus Trader
  difficulty: advanced
---

# Copy Consensus Trader

> **This is a template.**
> The default signal requires multi-wallet consensus before trading -- remix it with SmartScore weighting, time decay on activity, or sector-specific consensus thresholds.
> The skill handles all the plumbing (leaderboard fetching, activity aggregation, consensus building, conviction-boosted sizing, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

A single whale can be wrong, manipulating, or hedging a larger position elsewhere. But when 3+ independent smart-money wallets all bet the same direction on the same market, the signal is fundamentally different. This skill fetches top wallets from the public predicting.top leaderboard, pulls each wallet's recent activity from the Polymarket data API, and builds a consensus map aggregating net positions across all wallets per market.

Only markets where the majority side has at least 3 wallets AND opposition is minimal (fewer than half the consensus count) qualify as tradeable signals. This strict filter eliminates noisy single-wallet signals and focuses capital on the highest-conviction setups where smart money independently agrees.

## Signal Logic

### Step 1: Fetch Leaderboard

Top wallets are fetched from `predicting.top/api/leaderboard`. The skill tracks up to 20 wallets (configurable via `SIMMER_LEADERBOARD_LIMIT`).

### Step 2: Fetch Wallet Activity

For each wallet, recent trades (up to 80) are fetched from the Polymarket data API (`data-api.polymarket.com`). Net positions are extracted per market: if a wallet has more YES volume than NO volume on a market, that counts as a YES position.

### Step 3: Build Consensus Map

All wallet positions are aggregated into a consensus map:

```
market_title -> {yes_wallets: set, no_wallets: set, yes_volume, no_volume}
```

### Step 4: Find Consensus Signals

Markets are filtered to those where:
- The majority side has >= `MIN_CONSENSUS` wallets (default: 3)
- Opposition is clean: either zero opposing wallets OR opposing < consensus / 2

Signals are sorted by wallet count descending, then total volume descending.

### Step 5: Trade with Consensus Boost

For each consensus signal:
1. Find matching Simmer market via progressive keyword search
2. Run standard `compute_signal()` -- conviction-based sizing per CLAUDE.md
3. Only trade if consensus direction matches signal direction (dual confirmation)
4. Apply consensus boost: `extra_whales * CONSENSUS_BOOST` (capped at 50%)
5. Boosted conviction = `base_conviction * (1 + boost)`, capped at 1.0
6. Check `context_ok()` for flip-flop and slippage safeguards

### Conviction Sizing (base, before consensus boost)

| p | conviction | size |
|---|-----------|------|
| 38% | 0% | $5 (floor) |
| 30% | 21% | $10.50 |
| 20% | 47% | $23.50 |
| 0% | 100% | $50 |

### Consensus Boost Example

With 5 wallets agreeing (MIN_CONSENSUS=3, CONSENSUS_BOOST=0.20):
- Extra whales: 5 - 3 = 2
- Boost: 2 * 0.20 = 0.40 (40% conviction increase)
- Base conviction 0.47 becomes min(1.0, 0.47 * 1.40) = 0.658
- Size: max(5, round(0.658 * 50, 2)) = $32.90

## Edge Thesis

The core edge is that **independent agreement among multiple smart-money wallets is a much stronger signal than any single wallet's position**:

1. **Noise reduction**: Single wallets can be hedging, testing, or making mistakes. Multiple wallets agreeing independently filters all of that out.
2. **Information aggregation**: Each whale may have access to different information sources. Consensus means multiple independent information channels point the same way.
3. **Reduced manipulation risk**: One whale can manipulate a market. Coordinating 3+ independent wallets to all manipulate the same market in the same direction is far harder.
4. **Conviction scaling**: The more whales that agree, the stronger the position sizing -- reflecting the exponentially decreasing probability that all of them are wrong.

## Remix Ideas

- **SmartScore weighting**: Weight each wallet's vote by their SmartScore -- a 95-score whale counts more than a 70-score whale
- **Time decay**: Weight recent activity (last 24h) more heavily than older positions (last 7d)
- **Sector filtering**: Only count consensus within categories each whale historically performs best in
- **Anti-correlation**: Track which wallets tend to disagree -- if historically uncorrelated wallets suddenly agree, that is an even stronger signal
- **Dynamic thresholds**: Raise MIN_CONSENSUS during high-volatility regimes, lower it during quiet periods

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` -- it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority -- keep this credential private. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `50` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (0.08 = 8%) |
| `SIMMER_MIN_DAYS` | `5` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_MIN_CONSENSUS` | `3` | Min wallets that must agree for a consensus signal |
| `SIMMER_CONSENSUS_BOOST` | `0.20` | Extra conviction per whale beyond minimum (capped at 0.50 total) |
| `SIMMER_LEADERBOARD_LIMIT` | `20` | How many top wallets to track from the leaderboard |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
