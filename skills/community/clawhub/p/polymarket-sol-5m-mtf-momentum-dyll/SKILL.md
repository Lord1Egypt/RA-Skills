---
name: polymarket-sol-5m-mtf-momentum-dyll
description: Multi-timeframe CEX momentum trading for Polymarket BTC 5-minute fast markets. Aligns 1m/3m/5m Binance returns for directional conviction. Inspired by the #1 Simmer leaderboard trader running 79% WR across 4,000+ trades. Foundation bot with detuned thresholds — tune it, gate it, own the edge.
metadata:
  author: "dyll"
  version: "1.1.0"
  displayName: "SOL 5m MTF Momentum"
  difficulty: "intermediate"
---

# SOL 5m MTF Momentum

> ⚡ **This is a template.** You must configure your `SIMMER_API_KEY` before running.

Raw CEX momentum → Polymarket alpha. When all timeframes align, the signal is undeniable.

This bot reads the battlefield in real-time — 1-minute, 3-minute, and 5-minute Binance SOL/USDT returns voting on direction. When momentum converges across timeframes, it strikes. No hesitation, no second-guessing. Pure directional conviction deployed into Polymarket 5-minute fast markets.

**Inspired by the #1 trader on the Simmer leaderboard** — yanksie, who dominates BTC 5m markets with a 79% win rate across 4,000+ trades. The same multi-timeframe momentum principles applied to SOL. This foundation captures the core multi-timeframe momentum approach that drives that edge.

## The Edge

Three timeframes. One direction. Maximum conviction.

- **r1** (1m return) — noise filter, immediate pulse
- **r3** (3m return) — trend confirmation
- **r5** (5m return) — dominant signal, tiebreaker

Direction = majority vote. Confidence = signal-to-noise ratio scaled against recent volatility. The bot only fires when the math says *go*.

## What This Is — And What It Isn't

This is the **foundation**. The confidence threshold (0.50) is intentionally detuned. Out of the box, it trades. But the real alpha comes from tuning:

- **Confidence threshold** — tighten it, raise your win rate
- **Eval window timing** — when in the 5-minute cycle to strike
- **Additional gates** — order book depth, CLOB flow confirmation, candle body analysis, regime detection

These gates and logic layers can dramatically improve WR beyond the foundation. They're left to the trader to implement. The Ferrari is in the garage — you bring the driving skills.

## Setup

1. Install: `pip install simmer-sdk`
2. Set your API key: `export SIMMER_API_KEY=sk_live_...`
3. Dry run: `python3 mtf_momentum.py`
4. Go live: `python3 mtf_momentum.py --live`

## Configuration

| Parameter | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| Confidence Min | `SIMMER_MTF_CONF_MIN` | 0.50 | Minimum confidence to trade |
| Confidence Scale | `SIMMER_MTF_CONF_SCALE` | 2.1 | Volatility scaling factor |
| Eval Min Age | `SIMMER_MTF_EVAL_MIN_AGE` | 90 | Min market age (seconds) |
| Eval Max Age | `SIMMER_MTF_EVAL_MAX_AGE` | 180 | Max market age (seconds) |
| Trade Size | `SIMMER_MTF_TRADE_SIZE` | 10 | Trade size in $SIM |

## Quick Commands

```bash
# Dry run (paper mode)
python3 mtf_momentum.py

# Live trading
python3 mtf_momentum.py --live

# Show current positions
python3 mtf_momentum.py --positions

# Show config
python3 mtf_momentum.py --config

# Tune confidence threshold
python3 mtf_momentum.py --set conf_min=0.65

# Check portfolio status
python3 scripts/status.py
```

## Example Output

```
⚡ SOL 5m MTF Momentum
==================================================
  [PAPER MODE] Use --live for real trades.

  Config: conf_min=0.50 conf_scale=2.1 eval_window=90-180s size=$10

  Fetching SOL 5m fast markets...
  Found 2 active markets

  📊 SOL 5m — Will BTC go up in the next 5 minutes?
     Market age: 112s (in eval window)
     r1=+0.08% r3=+0.15% r5=+0.22% → UP (3/3 aligned)
     vol=0.0011 conf=0.94 ✅ TRADE
     → BUY YES $10.00 | reason: MTF momentum aligned UP (conf=0.94)
     ✅ Paper trade executed (12.5 shares)

  Summary: 1 signal, 1 trade
```

## Troubleshooting

- **"No active fast markets"** — SOL 5m markets run on a schedule. Wait for the next cycle.
- **"Market age outside eval window"** — The bot only trades during the configured window (90-180s after market open). Adjust `SIMMER_MTF_EVAL_MIN_AGE` / `SIMMER_MTF_EVAL_MAX_AGE`.
- **"Confidence below threshold"** — Momentum isn't strong enough. Lower `SIMMER_MTF_CONF_MIN` for more trades (lower WR) or wait for stronger signals.
- **"simmer-sdk not installed"** — Run `pip install simmer-sdk`.
- **"SIMMER_API_KEY not set"** — Get your key from simmer.markets/dashboard → SDK tab.

## Cron

`*/1 * * * *` — runs every minute, checks market age, trades if in eval window.
