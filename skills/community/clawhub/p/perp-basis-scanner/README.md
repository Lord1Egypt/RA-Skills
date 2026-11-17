# perp-basis-scanner

A cross-exchange spot-vs-perpetual futures basis scanner. Pulls live spot and
perp mark prices from Binance, Bybit, OKX, and Deribit's free public REST
APIs (no API key required) and computes the basis percentage and current
funding rate for each.

## Why

Cash-and-carry / basis trades (long spot, short perp, or vice versa) depend
on the size of the spot-perp spread and the funding rate you'll collect or
pay while holding the position. Checking this manually across four exchanges
is tedious. This script does it in one call.

## Usage

```bash
# One-shot scan across all four exchanges
python3 scripts/basis_scanner.py scan BTC ETH SOL

# JSON output for piping into another tool
python3 scripts/basis_scanner.py scan BTC --json

# Only check specific exchanges
python3 scripts/basis_scanner.py scan BTC --exchanges binance,okx

# Repeat every 30 seconds
python3 scripts/basis_scanner.py watch BTC ETH --interval 30
```

## Output columns

| Column | Meaning |
|---|---|
| spot | Spot last/index price |
| perp | Perpetual mark price |
| basis % | `(perp - spot) / spot * 100` |
| ann. % | Rough annualized basis (`basis_pct * 3 * 365`) — approximation only |
| fund 8h % | Current 8-hour funding rate reported by the exchange |

## Requirements

- Python 3.8+, standard library only (`urllib`, `json`, `argparse`) — no
  pip installs needed.
- Outbound HTTPS access to `api.binance.com`, `fapi.binance.com`,
  `api.bybit.com`, `www.okx.com`, `www.deribit.com`.

## Notes

This is a read-only market-data tool. It does not place trades, hold API
keys, or manage positions.
