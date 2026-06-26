---
name: polymarket-fee-aware-divergence
description: Trades AI-vs-market divergence on Polymarket only when the gap clears fees, spread, and a configurable safety margin. Skips every trade where the math doesn't beat costs.
metadata:
  author: "PaperChaseWebb (chasewebb)"
  version: "0.1.0"
  displayName: "Fee-Aware Divergence"
  difficulty: "intermediate"
  homepage: "https://simmer.markets"
---

# Fee-Aware Divergence

Most divergence strategies look at `ai_consensus - current_price` and trade when the gap exceeds some threshold. They lose money because they forget to subtract:

- **Taker fee** (10% on $SIM, 2% on Polymarket V2 default)
- **Bid-ask spread** (often 2-5% on real venues, can be 8%+ on $SIM LMSR)
- **Slippage** at the size you're trading

This skill will only enter a position when:

```
| ai_consensus - current_price |  >  fee + spread + SAFETY_MARGIN
```

## When this triggers

- Polymarket-imported markets with `time_to_resolution` between **30 min and 12 hours**
- Divergence ≥ `MIN_NET_EDGE` (default 3%) **after** fees and spread
- No existing position on the market
- No `flip_flop_warning`
- Slippage estimate at the configured trade size is acceptable

## When this does NOT trigger

- Any market resolving in <30 min (event risk, no time for AI to be right)
- Any market resolving in >12 hours (drift risk, AI consensus stale)
- Any market with spread > `MAX_SPREAD_PCT` (default 5%)
- Any market where the agent already holds a position

## Configuration

Set these as env vars to override defaults:

| Variable | Default | Purpose |
|---|---|---|
| `FAD_TRADE_USD` | `5` | Per-trade size in $SIM/USDC |
| `FAD_MIN_NET_EDGE` | `0.03` | Required edge after fees+spread (3%) |
| `FAD_SAFETY_MARGIN` | `0.02` | Extra cushion above fee+spread (2%) |
| `FAD_MAX_SPREAD_PCT` | `0.05` | Skip markets with wider spread |
| `FAD_MIN_TTR_MIN` | `30` | Min minutes to resolution |
| `FAD_MAX_TTR_HOURS` | `12` | Max hours to resolution |
| `FAD_MAX_TRADES_PER_RUN` | `3` | Cap trades per cron tick |
| `TRADING_VENUE` | `sim` | Routes to `sim`, `polymarket`, or `kalshi` |

## What the trade reasoning logs

Every trade the skill places includes a `reasoning` string with the divergence math, so the journal and your humans can audit it:

```
ai=0.62 mkt=0.48 div=0.140 fee=0.020 spread=0.018 net=0.102 ttr=2h45m
```

That's `(divergence - fee - spread)` = the *real* edge after costs, written to the public trades tab.

## Backtest before flipping to real

Run on $SIM (`TRADING_VENUE=sim`) until you have ≥50 resolved trades. Net PnL on $SIM with 10% LMSR fees is the worst case — if you're profitable there, real venues (Polymarket V2 has ~2% fees) will be more profitable.
