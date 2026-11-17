# Hyperliquid Perp Signals

Signal scanner for Hyperliquid L1 perpetual futures. Funding rates, open interest shifts, liquidation events, and cross-venue basis — all in one CLI built for the on-chain perp trader.

## What it does

- `funding` — current funding rate per coin, annualized %, with directional bias signal
- `oi` — open interest ranked by 24h change; flags crowded longs/shorts
- `liqs` — recent liquidation feed, tallies long vs short liq size, flags cascade risk
- `basis` — Hyperliquid vs Binance funding basis, surfaces cross-venue arb
- `squeeze` — short-squeeze risk score (negative funding + OI build + mark premium)

## Why it matters

Hyperliquid is the only major L1 with a real order-book perpetual futures DEX. Binance and Bybit dominate CEX perp flow but have custody and KYC overhead. This skill gives you a CLI to compare the two venues in one place without writing a custom script.

## Install

```bash
python3 scripts/hl_signals.py funding
python3 scripts/hl_signals.py squeeze ETH
```

Zero dependencies. Python 3.9+.

## Configuration

- `HL_API_URL` — Hyperliquid info endpoint (default `https://api.hyperliquid.xyz/info`)
- `HL_BINANCE_FUNDING_COMPARE` — set `false` to skip Binance basis comparison

## Notes

The bundled script ships with deterministic mock data. In production, replace `fetch_meta_mock` with a `POST` to `{type: "metaAndAssetCtxs"}` on the Hyperliquid info endpoint, and replace the Binance funding mock with the Binance public `fapi/v1/fundingRate` endpoint. The output schema and CLI do not change.
