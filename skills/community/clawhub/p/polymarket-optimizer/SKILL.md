---
name: polymarket-optimizer
description: Automatic parameter optimizer for polymarket-executor. Reads performance_metrics.json every 6 hours, analyzes win rates and P&L per strategy, adjusts learned_config.json to improve future performance. Also builds paper trade metrics and assesses live trading readiness. Part of the Wesley Agent Ecosystem — mirrors crypto-executor-optimizer pattern.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3"]
      env:
        required: []
        optional:
          - TELEGRAM_BOT_TOKEN
          - TELEGRAM_CHAT_ID
          - WORKSPACE
    network_behavior:
      makes_requests: true
      endpoints_allowed:
        - "https://api.telegram.org/bot*"
      requires_credentials: false
      uses_websocket: false
    security_level: "L1 - Read/Write local files only"
    author: "Georges Andronescu (Wesley Armando)"
    license: "MIT"
    homepage: "https://github.com/georges91560/polymarket-optimizer"
    repository: "https://github.com/georges91560/polymarket-optimizer"
---

# Polymarket Optimizer — Adaptive Parameter Tuner

## 🧠 WHAT IT DOES

Reads trading performance from `polymarket-executor`, analyzes what works, and adjusts parameters automatically.

Runs every **6 hours** via OpenClaw cron job. Zero manual intervention required.

**Input files (written by executor):**
- `performance_metrics.json` — per-strategy win rates, P&L, trade counts
- `paper_trades.json` — all simulated trade records
- `portfolio.json` — capital, positions, daily P&L

**Output files (read by executor at next startup):**
- `learned_config.json` — updated thresholds, Kelly fraction, allocations
- `optimizer_log.jsonl` — full history of every optimization run

---

## ⚡ QUICK START

```bash
cd /data/.openclaw/workspace/skills/polymarket-optimizer
python3 polymarket_optimizer.py
```

Expected output:
```
============================================================
POLYMARKET OPTIMIZER v1.0.0
Run time: 2026-03-05 14:00:00 UTC
============================================================
[CONFIG] Loaded. Optimization #1
[PORTFOLIO] Health: HEALTHY
[PORTFOLIO] Capital: $102.34 | Return: 2.3%
[ANALYSIS] parity_arbitrage: EXCELLENT | WR=100.0% | Trades=8 | P&L=+0.523
[ANALYSIS] tail_end: GOOD | WR=75.0% | Trades=12 | P&L=+0.312
[OPTIMIZER] 2 adjustments made:
  🚀 parity_arb excellent → min_profit 0.020 → 0.015
  📈 parity_arb allocation 30% → 40%
[READINESS] Resolved trades: 8/30
[READINESS] Win rate: 84.6% (need 55%+)
[TELEGRAM] Report sent.
============================================================
OPTIMIZER COMPLETE
============================================================
```

---

## 🔧 WHAT IT ADJUSTS

### Strategy Thresholds

| If strategy is... | Action |
|---|---|
| Poor (WR < 50%) | Raise threshold → trade only best opportunities |
| Underperforming (WR 50–65%) | Slight threshold increase |
| Average (WR 65–80%) | No change |
| Good (WR 65–80%, positive P&L) | No change |
| Excellent (WR > 80%) | Lower threshold → capture more volume |

### Capital Allocation

| If strategy is... | Action |
|---|---|
| Poor | Reduce allocation (min 5–10%) |
| Excellent | Increase allocation (max 50–70%) |

Allocations always normalized to sum to 100%.

### Kelly Fraction

| Portfolio health | Action |
|---|---|
| Critical (return < -10%) | Reduce Kelly → smaller positions |
| Excellent (return > 10%, WR > 65%) | Increase Kelly → larger positions |

### Scan Frequency

| Condition | Action |
|---|---|
| WR > 80% + 20+ trades | Scan faster (min 120s) |
| Portfolio warning/critical | Scan slower (max 600s) |

---

## 📊 LIVE READINESS ASSESSMENT

Every run evaluates whether paper trading results justify going live.

**4 criteria must ALL pass:**

| Criterion | Threshold |
|---|---|
| Resolved trades | ≥ 30 |
| Win rate | ≥ 55% |
| Total P&L | Positive |
| Circuit breaker | Not active |

Telegram report includes readiness status automatically.

---

## 📱 TELEGRAM REPORT

```
🧠 POLYMARKET OPTIMIZER REPORT
🕐 2026-03-05 14:00 UTC
🔄 Optimization #4

Portfolio Health: 🟢 HEALTHY
💰 Capital: $108.45
📈 Return: 8.5%
🎯 Win Rate: 76.9%
📊 Total Trades: 20

Strategy Performance:
  🚀 parity_arbitrage: 100.0% WR | 8 trades | P&L: +0.523
  ✅ tail_end: 75.0% WR | 12 trades | P&L: +0.312

Adjustments Made:
  🚀 parity_arb excellent → min_profit 0.020 → 0.015
  📈 parity_arb allocation 30% → 40%
  ⚖️ Allocations renormalized

Live Trading Readiness:
🔴 NOT YET READY
  ❌ Need 30+ resolved trades
  📊 Progress: 20/30 trades
  🎯 Win rate: 76.9% (need 55%+) ✅
```

---

## 📁 FILES

| File | Location | Description |
|---|---|---|
| `polymarket_optimizer.py` | `skills/polymarket-optimizer/` | Main optimizer script |
| `learned_config.json` | `WORKSPACE/` | Output — read by executor |
| `optimizer_log.jsonl` | `WORKSPACE/` | Full optimization history |

---

## ⏰ CRON JOB

Add to OpenClaw cron configuration:

```
# Run optimizer every 6 hours
0 */6 * * * docker exec openclaw-yyvg-openclaw-1 python3 /data/.openclaw/workspace/skills/polymarket-optimizer/polymarket_optimizer.py
```

---

**Version:** 1.0.0 | **License:** MIT | **Author:** Georges Andronescu (Wesley Armando)
