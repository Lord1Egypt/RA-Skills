# Polymarket Optimizer 🧠

**Automatic parameter tuner for Polymarket Executor**

Part of the **Wesley Agent Ecosystem** — mirrors `crypto-executor-optimizer` pattern.

---

## What It Does

Runs every 6 hours. Reads performance data from `polymarket-executor`, figures out what's working, and adjusts trading parameters automatically.

No manual configuration needed after setup.

---

## How It Works

```
polymarket-executor trades
        ↓
Writes performance_metrics.json + paper_trades.json + portfolio.json
        ↓
polymarket-optimizer runs (every 6h)
        ↓
Analyzes win rates, P&L, drawdowns per strategy
        ↓
Adjusts learned_config.json:
  - Thresholds (tighter if poor, looser if excellent)
  - Capital allocation (more to winners)
  - Kelly fraction (conservative if drawdown)
  - Scan frequency (faster if performing well)
        ↓
polymarket-executor reads new config at next startup
```

---

## Files

```
polymarket-optimizer/
├── SKILL.md                    ← OpenClaw integration
├── README.md                   ← This file
├── CONFIGURATION.md            ← Setup guide
├── SYSTEMD_SETUP.md            ← Run as system service
└── polymarket_optimizer.py     ← Main optimizer script
```

**Runtime files (auto-created in WORKSPACE):**
```
learned_config.json             ← Output (read by executor)
optimizer_log.jsonl             ← Full optimization history
```

---

## Quick Start

```bash
python3 polymarket_optimizer.py
```

Runs once and exits. Schedule via cron or systemd for automatic operation.

---

## Requirements

- Python 3.7+ (standard library only)
- `polymarket-executor` must have run first (to create input files)
- Telegram bot (optional — for reports)

---

## Ecosystem

```
polymarket-executor    ← Trades, writes metrics
polymarket-optimizer   ← This skill (reads metrics, updates config)
```

---

**License:** MIT | **Author:** Georges Andronescu (Wesley Armando)
**GitHub:** https://github.com/georges91560/polymarket-optimizer
