# Polymarket Executor 🎯

**Autonomous multi-strategy trading bot for Polymarket prediction markets**

Part of the **Wesley Agent Ecosystem** — built for OpenClaw autonomous AI agent.

---

## What It Does

Scans all Polymarket markets 24/7 for profitable opportunities using 3 strategies:

| Strategy | Risk | Win Rate | Frequency |
|---|---|---|---|
| Parity Arbitrage | ZERO | 100% | 5–20/day |
| Tail-End Trading | Very Low | 95–98% | 10–30/day |
| Logical Arbitrage | Low | 90–95% | 2–10/day |

**Markets:** Crypto, Politics, Sports, Economics, Tech, Entertainment, Weather — everything on Polymarket.

---

## Key Features

- 📄 **Paper mode** — validates strategy before risking real money
- 🧠 **Adaptive** — reads `learned_config.json` updated by optimizer every 6h
- ⚖️ **Kelly Criterion** — optimal position sizing per trade
- 🛡️ **Circuit breakers** — auto-halts at -15% daily loss
- 📱 **Telegram alerts** — real-time scan reports and trade notifications
- 🔄 **Self-improving** — writes `performance_metrics.json` for optimizer

---

## Files

```
polymarket-executor/
├── SKILL.md                    ← OpenClaw integration
├── README.md                   ← This file
├── CONFIGURATION.md            ← Setup guide
├── SYSTEMD_SETUP.md            ← Run as system service
└── polymarket_executor.py      ← Main trading bot
```

**Runtime files (auto-created in WORKSPACE):**
```
paper_trades.json               ← Paper trade log
portfolio.json                  ← Capital & positions
performance_metrics.json        ← Strategy stats
learned_config.json             ← Optimizer parameters
live_trades.jsonl               ← Real trades (live mode)
```

---

## Quick Start

```bash
# Paper mode — no credentials needed
python3 polymarket_executor.py

# Live mode — after paper validation
export PAPER_MODE=false
export POLYMARKET_API_KEY=...
export POLYMARKET_SECRET=...
export POLYMARKET_PASSPHRASE=...
python3 polymarket_executor.py
```

---

## Ecosystem

```
polymarket-executor    ← This skill (trading engine)
polymarket-optimizer   ← Adjusts parameters every 6h
```

---

## Requirements

- Python 3.7+ (standard library only — no pip install needed)
- Polymarket account + API credentials (live mode only)
- USDC on Polygon network (live mode only)
- Residential proxy for VPS (live mode only — CLOB POST blocked on datacenter IPs)

---

## Performance Targets

| Mode | Capital | Monthly ROI | Win Rate |
|---|---|---|---|
| Conservative | $1,000+ | 8–15% | 92–98% |
| Balanced | $5,000+ | 12–20% | 88–92% |
| Aggressive | $10,000+ | 15–30% | 80–90% |

*Paper trading validates these numbers before any real capital is deployed.*

---

**License:** MIT | **Author:** Georges Andronescu (Wesley Armando)
**GitHub:** https://github.com/georges91560/polymarket-executor
