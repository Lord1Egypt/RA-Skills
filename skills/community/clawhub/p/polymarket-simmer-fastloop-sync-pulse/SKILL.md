---
name: polymarket-simmer-fastloop-sync-pulse
displayName: Polymarket Simmer FastLoop Sync Pulse
description: Trade Polymarket BTC/ETH/SOL 5-minute fast markets using a zero-delay Triple-Trigger strategy. Combines Binance momentum, NOFX OI/Netflow (free public API), and L2 Wall detection to choose between Trend Following and Mean Reversion. Pre-Caches market IDs to bypass the Simmer API blackout at market open.
version: "1.0.2"
author: "Xuano47"
tags: ["polymarket", "trading", "btc", "quantitative", "sniper"]
pip:
  - simmer-sdk
env:
  - SIMMER_API_KEY
  - WALLET_PRIVATE_KEY
---

# Polymarket Simmer FastLoop Sync Pulse

> [!TIP]
> **This is a template.** The default signal is a **Triple-Trigger** strategy combining Binance momentum, NOFX institutional flow, and L2 Wall detection.
> Remix it with alternative signals like technical indicators (RSI/MACD), different CEX feeds, or custom LLM-based sentiment.
> The skill handles all the **plumbing** (market pre-caching, Simmer execution, budget safeguards). Your agent provides the **alpha**.

A professional-grade quantitative execution skill for Polymarket's 5-minute binary options.

## 🌟 Core Strategy: Triple-Trigger Sniper

This skill abandons naïve price-breakout logic. Every trade decision requires **three independent confirmations**:

### 1. Momentum & Pin Bar Filter (5m Candles)
- Measures the real momentum of the **previous closed 5-minute candle** on Binance.
- **Pin Bar Rejection**: If the counter-directional wick exceeds `max_pin_bar_tail_pct` (default 30%) of the full candle range, the signal is blocked as a likely exhaustion trap.
- `min_momentum_pct` defaults to **0.01%** — acting as a near-zero-threshold pass-through that relies on the shape filter for quality control.

### 2. NOFX Institutional Flow (300s Window)
- Uses the NOFX API to check the past 300 seconds of Open Interest (OI) and institutional Netflow.
- **Trend trade**: Momentum + OI increasing (> -2%) + net institutional inflow.
- **Reversion trade**: Momentum + OI declining (< +2%) + net institutional outflow.

### 3. Binance L2 Verified Wall Detection
- Scans the Binance L2 order book for large price walls above `min_wall_usd` (default $1,000,000) up to `wall_scan_depth` levels deep.
- **Anti-Spoofing**: When a wall is detected, the script waits 1.5s and checks again. Only a wall that survives both checks is considered a real barrier, filtering out high-frequency spoofing.
- **Usage**: Trend trades avoid walls; Reversion trades require a wall to bounce off.

### 4. Pre-Caching Radar (V8.10 Ignition)
- On every run, the script fetches all upcoming market IDs from the Simmer API and saves them to a local `fast_markets_cache.json`.
- At market open, the Simmer API briefly hides the active market. The skill reads from its local cache to execute trades during this "API blackout", ensuring no opportunity is missed.
- The local cache ensures execution even on a cold start at the exact moment of market open.

## ⚙️ Account Setup

Set the following environment variables:

| Variable | Required | Description |
| :--- | :--- | :--- |
| `SIMMER_API_KEY` | **Yes** | Your Simmer SDK API key |
| `WALLET_PRIVATE_KEY` | Optional | Your EVM wallet private key |
| `AUTOMATON_MAX_BET` | Optional | Override max position size (set by automation platforms) |

- **Without `WALLET_PRIVATE_KEY`**: Runs in **simulation mode** (paper trading, no real money).
- **With `WALLET_PRIVATE_KEY`**: Runs in **live mode** (real USDC on Polymarket).

> [!NOTE]
> **Binance** and **NOFX** are free, public APIs — no additional credentials or accounts are required. The skill reads Binance K-line/L2 data and NOFX OI/Netflow anonymously.

> [!WARNING]
> Never share your `WALLET_PRIVATE_KEY`. The Simmer SDK signs transactions locally — your private key is never transmitted to any server.

## 🚀 Quick Start

### Step 1: Pre-Warm the Cache (Recommended on First Run)
On first launch, run the script once to populate the local market ID cache. You do **not** need to be near a market window — the script will scan future markets, save them, and exit safely.

```bash
python fastloop_improved.py
```

You should see: `[Ignition] Successfully cached X future market IDs.`

### Step 2: Run the Sniper

```bash
# Dry run — analyzes signals but does NOT place orders
python fastloop_improved.py

# Live mode — places real orders
python fastloop_improved.py --live
```

> **Note**: With no `WALLET_PRIVATE_KEY`, `--live` uses Simmer's virtual $SIM balance (paper trading). Real USDC is only used when a private key is configured.

## ⚙️ All Settings

| Setting | Default | Env Var | Description |
| :--- | :--- | :--- | :--- |
| `min_momentum_pct` | 0.01 | `SIMMER_SPRINT_MOMENTUM` | Min BTC % move in lookback window |
| `max_position` | 10.0 | `SIMMER_MAX_POSITION` | Max USD per trade |
| `daily_budget` | 1000.0 | `SIMMER_DAILY_BUDGET` | Max total spend per UTC day |
| `max_pin_bar_tail_pct` | 0.3 | `SIMMER_PIN_BAR_MAX` | Max wick ratio to filter Pin Bar noise |
| `oi_neutral_zone` | 2.0 | `SIMMER_OI_NEUTRAL` | OI % buffer — changes within ±2% are ignored |
| `min_wall_usd` | 1000000 | `SIMMER_MIN_WALL_USD` | Min USD depth to qualify as a wall |
| `wall_scan_depth` | 50 | `SIMMER_WALL_SCAN_DEPTH` | Number of L2 order book levels to scan |
| `require_orderbook` | false | `SIMMER_ORDERBOOK` | Require L2 wall confirmation |
| `require_funding` | false | `SIMMER_FUNDING` | Require NOFX institutional flow |
| `fee_buffer` | 0.05 | `SIMMER_FEE_BUFFER` | Extra edge required above fee breakeven |

## 🆘 Troubleshooting

| Symptom | Cause | Action |
| :--- | :--- | :--- |
| `No high-conviction signal` | Data signals conflict or no wall found | Normal. The sniper only fires on high-probability setups. |
| `No tradeable markets found` | No Polymarket market is scheduled in this window | Normal. Cache is being updated. Wait for the next market window. |
| `Failed to fetch signal data` | Network or API rate limit | Check Binance / NOFX connectivity. |
| `401 Unauthorized` | Invalid API key | Verify `SIMMER_API_KEY` is set correctly. |

## 🎨 Remixing the Signal

This skill is designed as a **remixable template**. We separate the **Structural Plumbing** (Discovery, Execution, Budget) from the **Signal Alpha**.

### Implementation Architecture:
*   **The Plumbing (Structural)**: Functions like `discover_fast_market_markets`, `get_client`, and the daily budget logic are core infrastructure. 
*   **The Alpha (Replaceable)**: The decision brain lives in `run_fast_market_strategy` (~lines 570-580). 

### How to Remix:
1. **Find the Brain**: Modify `is_trend` or `is_reversion` in `fastloop_improved.py`.
2. **Swap Data Sources**: Replace `fetch_nofx_oi` or `fetch_binance_orderbook` with your own API calls (e.g., Glassnode, Santiment, or a custom model).
3. **Customize Sizing**: Edit `calculate_position_size` to implement Kelly Criterion or fixed-lot strategies.

*The default "Triple-Trigger" is just one example of a high-conviction setup — use this template to wire your own strategy into Polymarket's pipes.*

## 🤖 AI Operator Policy

When running this script as an automated agent, interpret outputs as follows:

**✅ Success — Ignition**: Log contains `[Ignition] Successfully cached X future market IDs.` Cache is populated. This is a successful run even if no trade fires.

**⏳ Normal — Waiting**: Log shows `No tradeable markets found`. This means no market is currently scheduled. The script will find one at the next window.

**❌ True Failure**: `401 Unauthorized`, `SyntaxError`, `AttributeError`, or 10+ consecutive `[API Delay]` messages with no `[Ignition]` line.

*The script's purpose is dual: snipe when conditions are right, and keep the local ID cache fresh at all other times.*
