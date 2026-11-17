# Polymarket Edge Detector

Find mispriced binary contracts on Polymarket. Compares market price to an external reference probability and surfaces +EV setups with confidence and liquidity scoring.

## What it does

- `scan` — ranks all open markets by edge (reference vs market price), with edge-decay adjustment based on time-to-resolution
- `scan --category crypto` — filter to a category (crypto, politics, sports, economics, tech)
- `market <slug>` — single-market deep-dive with full edge math
- `watch` — stream price changes, alert when any market crosses the configured edge threshold

## Why it matters

Polymarket has thousands of binary contracts, but most are efficiently priced near resolution. The edge sits in the long tail: low-liquidity markets, distant resolutions, and contracts where the market is misanchored to recent news. This skill gives you a CLI to surface them without hand-rolling a screener.

## Install

```bash
python3 scripts/edge_detector.py scan
python3 scripts/edge_detector.py market btc-100k-2026
```

Zero dependencies. Python 3.9+.

## Configuration

- `POLY_API_URL` — Polymarket CLOB endpoint (default `https://clob.polymarket.com`)
- `EDGE_THRESHOLD_PCT` — minimum edge to surface (default 3.0)
- `REFERENCE_SOURCE` — `poll`, `model`, or `market_implied` (default `market_implied`)

## Notes

The bundled script ships with a mock market universe of 12 contracts across 5 categories. In production, replace `MARKETS` with results from `GET /markets` on the Polymarket CLOB API and replace the mock price fetcher with `GET /book` for each market. The CLI does not change.
