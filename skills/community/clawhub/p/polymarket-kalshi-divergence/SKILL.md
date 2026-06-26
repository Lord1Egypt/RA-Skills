---
name: polymarket-kalshi-divergence
description: >
  Cross-platform arbitrage between Kalshi and Polymarket. Monitors 13 Kalshi event
  series (crypto, macro, politics) and compares prices to equivalent Polymarket
  markets. Generates BUY signals when gap exceeds 8% and SELL signals above 10%.
metadata:
  author: "Mibayy"
  version: "2.0.5"
  displayName: "Kalshi-Polymarket Divergence Arb"
  type: "automaton"
  difficulty: "intermediate"
---

# Kalshi-Polymarket Divergence Arb

Cross-platform price divergence trading between Kalshi and Polymarket.

## What It Does

Polls Kalshi's public API for live prices across 13 event series and compares
them to equivalent Polymarket markets found via SimmerClient. When prices diverge
beyond threshold, the cheaper side is likely underpriced.

## Covered Series

| Series | Category | Description |
|--------|----------|-------------|
| KXBTC, KXETH, KXSOL, KXXRP, KXDOGE | Crypto | Price threshold markets |
| KXFED | Macro | Fed rate decisions |
| KXCPI | Macro | CPI prints |
| KXUNEMP | Macro | Unemployment data |
| KXGLD, KXOIL | Commodities | Price threshold markets |
| KXNASDAQ, KXSPY, KXINX | Indices | Index level markets |

## Signal Logic

- **BUY** - Polymarket price is >8% below Kalshi equivalent (Polymarket underpriced)
- **SELL** - Polymarket price is >10% above Kalshi equivalent (Polymarket overpriced)
- Asymmetric thresholds account for Polymarket's typically lower liquidity

## Scheduling

Runs every 5 minutes via cron (`*/5 * * * *`). Managed automaton (auto-executes on schedule).
Dry-run by default. Pass `--live` to execute real trades.

## Requirements

**pip dependencies:** `simmer-sdk`, `requests`

**Environment variables (required):**
- `SIMMER_API_KEY` - get from simmer.markets/dashboard

**Environment variables (optional, all have defaults):**
- `TRADING_VENUE` - defaults to `sim` for paper trading, set to `polymarket` for real
- `KALSHI_BUY_THRESHOLD` - minimum divergence to trigger BUY, defaults to `0.08` (8%)
- `KALSHI_SELL_THRESHOLD` - minimum divergence to trigger SELL, defaults to `0.10` (10%)
- `KALSHI_TRADE_SIZE` - trade size in USD, defaults to `20.0`

## Usage

```bash
python kalshi_divergence.py                  # dry run (default, no trades)
python kalshi_divergence.py --live           # real trades via SimmerClient
python kalshi_divergence.py --live --quiet   # cron mode
```

## Trade Execution Path

1. Fetches Kalshi public prices via HTTPS GET (no auth needed)
2. Finds matching Polymarket markets via `SimmerClient.find_markets()`
3. Compares prices, applies thresholds (BUY >8%, SELL >10%)
4. If `--live`: calls `SimmerClient.trade()` with market_id, side, amount, reasoning
5. If dry-run (default): logs the signal but does NOT execute any trade

## Security

- All trades go through `SimmerClient.trade()` only. No direct CLOB or wallet access.
- Only required credential is `SIMMER_API_KEY`. No other secrets needed.
- No wallet private keys are required or read by this script.
- Dry-run is the default. The `--live` flag must be explicitly passed to execute trades.

> Remixable Template: Fork this skill to add new Kalshi series, adjust
> divergence thresholds, or add position sizing based on gap magnitude.
