---
name: polymarket-spread-sniper
description: Snipe mispriced Polymarket markets by comparing AMM price vs live CLOB orderbook midpoint. Buys the underpriced side when edge > 3% on liquid markets. Exits via take-profit or time-stop. Pure algorithm, zero LLM, no outcome prediction needed.
metadata:
  author: "openclaw"
  version: "1.3.0"
  displayName: "Polymarket Spread Sniper"
  difficulty: "intermediate"
---

# Polymarket Spread Sniper

Buys the underpriced side when the Polymarket AMM price diverges from the live CLOB orderbook midpoint. No outcome prediction — pure spread arbitrage. Exits automatically via take-profit or time-stop.

## The Edge

Polymarket has two pricing mechanisms:
1. **AMM** — pool-based price, slower to update
2. **CLOB** — live orderbook, reflects real-money conviction

When they diverge by more than `min_edge` (default 3%), the AMM is mispriced. The skill buys the cheap side and exits when prices converge or the time window closes.

## Quick Start

```bash
export SIMMER_API_KEY=sk_live_...

# Dry run (SIM mode — safe, no real money)
python spread_sniper.py

# Live trading
python spread_sniper.py --live

# Show open positions with P&L
python spread_sniper.py --positions

# P&L summary (realized + unrealized)
python scripts/spread_pnl.py

# P&L history log
python scripts/spread_pnl.py --history
```

## Configuration

All settings can be overridden via environment variables or tuned from the Simmer dashboard.

| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| Min edge | `SIMMER_SPREAD_MIN_EDGE` | 0.03 | Min AMM/CLOB divergence to trade (3%) |
| Min volume | `SIMMER_SPREAD_MIN_VOLUME` | 5000 | Min 24h volume in USD |
| Max position | `SIMMER_SPREAD_MAX_POSITION` | 5.00 | Max USD per trade |
| Max trades/run | `SIMMER_SPREAD_MAX_TRADES` | 3 | Max new trades per scan |
| Min price | `SIMMER_SPREAD_MIN_PRICE` | 0.10 | Never buy below 10¢ |
| Max price | `SIMMER_SPREAD_MAX_PRICE` | 0.90 | Never buy above 90¢ |
| Max hours | `SIMMER_SPREAD_MAX_HOURS` | 24 | Skip markets resolving >24h out |
| Max CLOB spread | `SIMMER_SPREAD_MAX_CLOB_SPREAD` | 0.05 | Skip illiquid books (bid-ask > 5¢) |
| Daily spend cap | `SIMMER_SPREAD_DAILY_MAX` | 100.00 | Max USD deployed per day |
| Take-profit | `SIMMER_SPREAD_TP_PCT` | 0.60 | Exit when 60% of entry edge captured |
| Time-stop | `SIMMER_SPREAD_TS_PCT` | 0.50 | Exit when 50% of market window elapsed |
| Market exclude | `SIMMER_SPREAD_EXCLUDE` | *(68 keywords)* | Comma-separated keywords to skip |

## Exit Logic

Positions are checked on every scan:

- **Take-profit**: exits when CLOB has moved `take_profit_pct × entry_edge` toward fair value
- **Time-stop**: exits when `time_stop_pct` of the market's remaining window has elapsed since entry, or when <2h left regardless

## P&L Tracking

```bash
# Snapshot: realized (from Simmer resolved API) + unrealized (open positions)
python scripts/spread_pnl.py

# Full history log
python scripts/spread_pnl.py --history

# Open positions detail
python scripts/spread_pnl.py --positions
```

Log appended to `spread_pnl.log` on each run. Cron-safe.

## Files

```
spread_sniper.py        # Main bot — scan + entry + exit
config.json             # Runtime config overrides (takes precedence over env vars)
clawhub.json            # ClawHub + automaton config
scripts/
  spread_pnl.py         # P&L tracker (realized via Simmer API + unrealized)
  sim_redeem.py         # Redeem resolved SIM positions
spread_positions.json   # Local position journal
spread_daily.json       # Daily spend state
spread_pnl.log          # P&L snapshot log
```

## Safety

- All credentials loaded from environment — no hardcoded secrets
- Daily spend cap prevents runaway deployment
- CLOB spread filter skips illiquid markets
- Price range filter (10%–90%) avoids near-certain / near-impossible positions
- Extensive keyword exclude list filters out esports, weather, and obscure football markets
