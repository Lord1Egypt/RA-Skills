---
name: polymarket-simmer-fastloop
displayName: Polymarket Simmer FastLoop Trader
description: Trade Polymarket BTC/ETH/SOL 5/15-minute fast markets with momentum and order book filters.
version: "1.1.0"
author: "Xuano47"
tags: ["polymarket", "trading", "btc", "eth", "sol"]
env:
  - SIMMER_API_KEY
  - TRADING_VENUE
---

# Polymarket Simmer FastLoop Trader

> [!TIP]
> **This is a template.** The default signal is a **Mean Reversion** strategy using Binance momentum exhaustion and L2 order book imbalance.
> Remix it with alternative signals like trend-following momentum, social sentiment feeds, or cross-venue arbitrage models.
> The skill handles all the **plumbing** (market discovery, fee-accurate EV math, position tracking). Your agent provides the **alpha**.

Automated trading skill for Polymarket BTC/ETH/SOL 5-minute and 15-minute fast markets.

> **Default is paper mode.** Use `--live` for real trades.

## Strategy

When the latest 5-minute candle shows a rapid spike (momentum > threshold) the script buys the **reverse side**, capturing the pullback. Signals are filtered by:

- **Momentum**: Binance 1-minute candles, configurable threshold (default 1.0%).
- **Order Book Imbalance** (optional): Top 20 levels of Binance L2 book confirm directional bias.
- **NOFX Institutional Netflow**: Filters trades using institutional flow data.
- **Time-of-Day Filter**: Skips low-liquidity hours (02:00–06:00 UTC) by default.
- **Fee-Accurate EV**: Only trades when divergence exceeds fee breakeven + buffer.
- **Volatility-Adjusted Sizing**: High volatility reduces position size automatically.
- **Pre-Caching (Ignition)**: On every run, the skill scans and caches upcoming market IDs to disk (`fast_markets_cache.json`). At market open, the Simmer API briefly hides the market — the skill uses the cache to execute trades during this "API blackout" window, ensuring no opportunity is missed.

## Setup

### 1. Get Simmer API Key
- Register at [simmer.markets](https://simmer.markets).
- Go to **Dashboard** -> **SDK** tab.
- Copy your API key: `export SIMMER_API_KEY="your-key-here"`.

### 2. Required Environment Variables

| Variable | Required | Description | Values |
|----------|----------|-------------|--------|
| `SIMMER_API_KEY` | **Yes** | Your Simmer SDK key | Get from [simmer.markets](https://simmer.markets) |
| `TRADING_VENUE` | **Yes** | Execution environment | `simmer` (Paper) or `polymarket` (Live) |
| `WALLET_PRIVATE_KEY` | Optional | Your Polymarket wallet key | Required only if `TRADING_VENUE="polymarket"` |

- **`simmer`** (Default): Paper Trading. Simulates trades using virtual funds. No real USDC needed.
- **`polymarket`**: Real Trading. Connects to Polymarket. You **must** have USDC in the wallet.

> [!WARNING]
> Never share your `WALLET_PRIVATE_KEY` or `SIMMER_API_KEY`. The SDK signs trades locally; your private key is never transmitted.

## Quick Start

```bash
pip install simmer-sdk
export SIMMER_API_KEY="your-key-here"

# Paper mode (default)
python polymarket-simmer-fastloop.py

# Live trading
python polymarket-simmer-fastloop.py --live

# Check win rate and P&L stats
python polymarket-simmer-fastloop.py --stats

# Resolve expired trades against real outcomes
python polymarket-simmer-fastloop.py --resolve

# Quiet mode for cron
python polymarket-simmer-fastloop.py --live --quiet
```

## Cron Setup

**OpenClaw:**
```bash
openclaw cron add \
  --name "Simmer FastLoop" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run: cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet. Show output summary." \
  --announce
```

**Linux crontab:**
```
*/5 * * * * cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet
```

## All Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `entry_threshold` | 0.05 | Min divergence from 50c |
| `min_momentum_pct` | 1.0 | Min % asset move to trigger |
| `max_position` | 5.0 | Max $ per trade |
| `signal_source` | binance | binance or coingecko |
| `lookback_minutes` | 5 | Candle lookback window |
| `min_time_remaining` | 60 | Skip if < N seconds left |
| `target_time_min` | 90 | Prefer markets with >= N seconds left |
| `target_time_max` | 210 | Prefer markets with <= N seconds left |
| `asset` | BTC | BTC, ETH, or SOL |
| `window` | 5m | 5m or 15m |
| `volume_confidence` | true | Skip low-volume signals |
| `require_orderbook` | false | Require order book confirmation |
| `time_filter` | true | Skip 02:00–06:00 UTC |
| `vol_sizing` | true | Adjust size by volatility |
| `fee_buffer` | 0.05 | Extra edge above fee breakeven |
| `daily_budget` | 10.0 | Max spend per UTC day |
| `starting_balance` | 1000.0 | Paper portfolio starting balance |

## 🎨 Remixing the Signal

This skill is a **remixable template**. We distinguish between **Plumbing** (Infrastructure) and **Alpha** (Strategy).

### Core Components:
*   **The Plumbing (Structural)**: Market discovery (Gamma/Simmer fallback), Pre-Caching, execution via Simmer SDK, and fee-accurate EV calculations.
*   **The Alpha (Replaceable)**: The decision-making logic inside `run_strategy` where `side` is determined based on CEX signals.

### How to Remix:
1. **Find the Signal logic**: In `polymarket-simmer-fastloop.py`, look for the `run_strategy` function around line ~950.
2. **Modify the Decision**: 
   - Swap the `side = "no"` and `side = "yes"` logic to change from Mean Reversion to Trend Following.
   - Replace `get_momentum` with your own model or API (e.g., custom XGBoost classifier or GPT-4o signal).
3. **Refine Execution**: Edit `calculate_position_size` to implement custom risk management formulas.

*Use this template to bypass the complexity of Polymarket's order book and focus entirely on your strategy logic.*

## Troubleshooting

**"Momentum below threshold"** — Asset move is too small. Lower `min_momentum_pct` if needed.

**"Order book imbalance: neutral"** — Market is balanced, signal skipped when `require_orderbook=true`.

**"Time filter: low liquidity window"** — Current hour is 02–06 UTC. Set `time_filter=false` to override.
