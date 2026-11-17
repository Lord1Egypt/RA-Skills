---
name: perp-basis-scanner
description: Scans the spot-vs-perpetual futures basis (contango/backwardation) across Binance, Bybit, OKX, and Deribit for any symbol they list, using free public REST market-data endpoints with no API key required. Useful for crypto trading, basis trade, cash-and-carry arbitrage, funding rate arbitrage, perpetual futures, options and derivatives research, whale-style institutional strategies, and passive income via delta-neutral spot-perp spreads. Reports live spot price, perp mark price, basis percentage, a rough annualized basis estimate, and the current 8-hour funding rate side by side across exchanges so you can spot the widest, most tradeable dislocations. Supports one-shot scans and a repeating watch mode for monitoring basis drift over time. Built for python developers, ai agent operators, and defi/crypto researchers who want a quick cross-exchange basis check before sizing a cash-and-carry or funding-rate-arbitrage position.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Perp Basis Scanner

Compares spot and perpetual futures prices across Binance, Bybit, OKX, and
Deribit for a given symbol, reporting the basis (spread between spot and
perp) and an approximate annualized rate. This is a research/monitoring
tool, not an execution engine — it does not place orders.

## When to use this skill

- The user wants to check whether a spot-vs-perp basis trade (cash-and-carry)
  looks attractive right now for a given coin.
- The user asks "what's the basis on BTC/ETH/SOL across exchanges" or wants
  to compare funding rates and mark-price spreads side by side.
- The user wants a lightweight, repeatable way to watch basis drift over a
  session (`watch` mode).

## How to run it

```bash
python3 scripts/basis_scanner.py scan BTC ETH SOL
python3 scripts/basis_scanner.py scan BTC --json
python3 scripts/basis_scanner.py scan BTC --exchanges binance,deribit
python3 scripts/basis_scanner.py watch BTC ETH --interval 30
```

`scan` runs once and prints a table (or JSON with `--json`). `watch` repeats
the scan on an interval (seconds) until interrupted with Ctrl+C.

## What it covers

- **Binance**: spot `/api/v3/ticker/price` + futures `/fapi/v1/premiumIndex`
  (mark price + last funding rate).
- **Bybit**: v5 `/market/tickers` for both `spot` and `linear` categories.
- **OKX**: `/market/ticker` for spot and `-SWAP` instruments, plus
  `/public/funding-rate`.
- **Deribit**: `/public/get_index_price` (spot index) + `/public/ticker`
  for the `-PERPETUAL` instrument (BTC/ETH/SOL only — Deribit doesn't list
  perpetuals for every coin).

## Limitations

- The "annualized basis" figure is a rough extrapolation
  (`basis_pct * 3 * 365`), not a real funding-payment forecast — actual
  funding rates float and can flip sign.
- No order-book depth is used, so this does not account for slippage on
  entry/exit.
- Deribit only supports BTC, ETH, and SOL perpetuals; other symbols will
  return an error row for that exchange and can be excluded with
  `--exchanges`.
- All endpoints are public and unauthenticated; if an exchange rate-limits
  or blocks the request, that row will show an `error` field instead of
  failing the whole scan.
