---
name: kronos-signals-api
description: >
  Use this skill to call the Kronos Crypto Data API — a pay-per-call real-time
  crypto market data API that uses x402 USDC micropayments on Base mainnet.
  Activate when the user wants price data, perpetual futures intelligence
  (funding rates, OI, basis), ML directional forecasts (BTC/ETH/SOL), market
  regime alerts, Fear & Greed index, OHLC candles, realized volatility, a
  full-bundle snapshot, or a funding extremes screener across 16 assets.
  All paid endpoints cost $0.01–$0.08 USDC. Two endpoints are free.
---

# Kronos Crypto Data API — Agent Skill

> **Disclaimer:** All output from this API is informational only. This is NOT
> financial advice. Forecasts are probabilistic model outputs; signals are
> heuristics derived from public market data. Past signals do not guarantee
> future returns. Use at your own risk.

## Overview

| Property | Value |
|---|---|
| Base URL | `https://kronossignals.com` |
| Version | 1.0.0 |
| Payment | x402 USDC micropayments on Base mainnet (`eip155:8453`) |
| Payment scheme | EIP-3009 gasless (`exact`) |
| Free endpoints | `/api/stats`, `/api/health` |
| OpenAPI spec | `https://kronossignals.com/api/openapi.json` |

## Supported Assets (16)

`btc` `eth` `sol` `bnb` `xrp` `doge` `ada` `avax` `link` `dot` `ltc` `trx` `bch` `atom` `near` `apt`

---

## x402 Payment Flow (CRITICAL — read before any paid call)

All paid endpoints use the **x402 challenge-response protocol**:

1. **First call** (no `X-PAYMENT` header) → server returns **HTTP 402** with `X-PAYMENT-REQUIRED` header (Base64-encoded JSON payment requirements)
2. **Sign** the EIP-3009 transfer authorization using your wallet private key
3. **Second call** with `X-PAYMENT: <signed-payload>` header → server returns **HTTP 200** with data + `PAYMENT-RESPONSE` settlement receipt

**Never fabricate or cache payment tokens.** Each payment nonce is single-use (HTTP 409 on replay).

Use the `wallet-keeper` agent (or `x402-fetch` npm package) to handle steps 1-3 automatically.

---

## Endpoint Reference

### 🔓 FREE — Health Check
```
GET https://kronossignals.com/api/health
```
Returns API health status. No payment required.

---

### 🔓 FREE — Stats
```
GET https://kronossignals.com/api/stats
```
Returns API usage statistics. No payment required.

---

### 💰 Spot Price — $0.01 USDC
```
GET https://kronossignals.com/api/v1/price/{asset}
```
Real-time spot price from Binance for any of the 16 supported assets.

**Path params:**
- `asset` (required): lowercase asset slug, e.g. `btc`, `eth`, `sol`

**Query params:**
- `coins` (optional): comma-separated list (e.g. `BTC,ETH,SOL`) to batch up to 10 additional quotes in ONE paid call

**Response fields (200):**
```json
{
  "asset": "BTC-USD",
  "price": 107500,
  "source": "Binance",
  "as_of": "2026-07-02T10:00:00.000Z",
  "disclaimer": "...",
  "quotes": [...],        // only when ?coins= is used
  "unresolved": [...]     // unrecognized symbols from ?coins=
}
```

**Cost tip:** Use `?coins=ETH,SOL` on a BTC call to get 3 prices for the price of 1.

---

### 💰 Derivatives Signals — $0.02 USDC
```
GET https://kronossignals.com/api/v1/signals/{asset}
```
Perpetual swap intelligence from Bybit/OKX: funding rate, OI, basis, OI change, funding trend, and a human-readable heuristic read.

**Path params:**
- `asset` (required): any of 16 assets (lowercase)

**Response fields (200):**
```json
{
  "available": true,
  "asset": "BTC-USD",
  "as_of": "...",
  "data_source": "bybit",
  "samples": 12,
  "funding_rate": 0.0001,
  "funding_rate_annualized": 0.1095,
  "mark_price": 107510.5,
  "index_price": 107498.2,
  "basis": 0.0001144,
  "open_interest": 84320.15,
  "volume_24h": 2341089500,
  "next_funding_time": "...",
  "oi_change_1h": { "abs": 120.34, "pct": 0.1429 },
  "funding_trend": "flat",   // "rising" | "falling" | "flat" | "insufficient_data"
  "read": "Positive funding (10.9% ann.) — longs paying shorts...",
  "disclaimer": "..."
}
```

> Data lags by up to 5 minutes (cron cadence). `funding_rate_annualized` assumes current rate persists — it does not.

---

### 💰 BTC Market Regime Alerts — $0.02 USDC
```
GET https://kronossignals.com/api/v1/alerts/btc
```
BTC-only endpoint. Returns regime events from the last ~2 hours plus live state.

**Regime event types:**
- `squeeze` — volatility compression / squeeze setup
- `breakout` — significant price move detected
- `funding_extreme` — funding rate beyond normal bounds (annualized > threshold)
- `oi_surge` — rapid open interest change

**Severity levels:** `high` | `notable` | `info`

**Response fields (200):**
```json
{
  "available": true,
  "asset": "BTC-USD",
  "active_alerts": [
    {
      "event_type": "funding_extreme",
      "severity": "high",
      "detected_at": "...",
      "details": { "annualized_pct": 42.1, "sign": "longs_paying", "funding_rate_8h": 0.00096 }
    }
  ],
  "current_state": {
    "as_of": "...",
    "funding_rate": 0.0001,
    "funding_annualized": 0.1095,
    "open_interest": 84320.15,
    "read": "BTC: elevated positive funding ..."
  },
  "as_of": "...",
  "disclaimer": "..."
}
```

---

### 💰 Overview — All 16 Assets Derivatives Snapshot — $0.02 USDC
```
GET https://kronossignals.com/api/v1/overview
```
Market-wide derivatives snapshot across all 16 assets in one call. Good for cross-asset scanning.

---

### 💰 Funding Extremes Screener — $0.01 USDC
```
GET https://kronossignals.com/api/v1/funding-extremes
```
Ranks all 16 assets by absolute funding rate. Identifies crowded positions and squeeze risk across the full market.

**Response fields (200):**
```json
{
  "as_of": "...",
  "ranked": [
    {
      "rank": 1,
      "asset": "DOGE-USD",
      "short": "DOGE",
      "funding_rate": 0.0005,
      "funding_rate_annualized": 0.5475,
      "mark_price": 0.32,
      "open_interest": 98000000,
      "next_funding_time": "...",
      "funding_interval_hours": 8,
      "captured_at": "..."
    }
  ],
  "disclaimer": "..."
}
```

---

### 💰 Fear & Greed Index — $0.01 USDC
```
GET https://kronossignals.com/api/v1/fear-greed
```
Crypto Fear & Greed Index from alternative.me. Scale 0 (Extreme Fear) to 100 (Extreme Greed).

---

### 💰 OHLC Candlestick Data — $0.01 USDC
```
GET https://kronossignals.com/api/v1/ohlc/{asset}
```
Candlestick data from Binance.

**Path params:**
- `asset` (required): lowercase asset slug

**Common query params:**
- `interval` (optional): candle interval, e.g. `1h`, `4h`, `1d`
- `limit` (optional): number of candles

---

### 💰 Realized Volatility — $0.01 USDC
```
GET https://kronossignals.com/api/v1/volatility/{asset}
```
7-day and 30-day realized volatility for any of the 16 supported assets.

**Path params:**
- `asset` (required): lowercase asset slug

---

### 💰 Full Bundle Snapshot — $0.08 USDC ⭐ Best Value
```
GET https://kronossignals.com/api/v1/snapshot/{asset}
```
Everything for an asset in one call: spot price, derivatives, regime alerts (BTC only), ML forecast (BTC/ETH/SOL only), options IV (BTC/ETH only), squeeze bias, Coinbase CEX premium.

**Path params:**
- `asset` (required): any of 16 assets (lowercase)

**Response fields (200):**
```json
{
  "asset": "BTC-USD",
  "price": 107500,
  "derivatives": {
    "available": true,
    "funding_rate": 0.0001,
    "funding_rate_annualized": 0.1095,
    "open_interest": 84320.15,
    "basis": 0.000186,
    "funding_trend": "flat",
    "read": "..."
  },
  "regime": {
    "available": true,
    "active_alerts": [],
    "current_state": { "funding_rate": 0.0001, "open_interest": 84320.15, "read": "..." }
  },
  "forecast": {
    "available": true,
    "horizon": "1h",
    "up_prob": 0.62,
    "expected_close": 107620.5,
    "range_low": 106300,
    "range_high": 108700,
    "model": "kronos-base-60path-t1-v2",
    "cached": true,
    "cache_age_seconds": 180
  },
  "options_iv": {
    "available": true,
    "atm_iv": 52.4,
    "term_structure_shape": "contango",
    "data_source": "deribit",
    "as_of": "..."
  },
  "liquidations": {
    "available": true,
    "squeeze_bias": "long_squeeze_risk"   // "long_squeeze_risk" | "short_squeeze_risk" | "balanced"
  },
  "cex_premium": {
    "available": true,
    "coinbase_price": 107512.34,
    "composite_median": 107498,
    "premium_pct": 0.0133,
    "interpretation": "Coinbase +0.013% premium..."
  },
  "as_of": "...",
  "disclaimer": "..."
}
```

> Use snapshot when you need 3+ data dimensions for one asset. Cheaper than calling price + signals + alerts separately ($0.05).

---

### 💰 ML Directional Forecast — $0.05 USDC (Premium)
```
GET https://kronossignals.com/api/v1/forecast/btc    # BTC
GET https://kronossignals.com/api/v1/forecast/eth    # ETH
GET https://kronossignals.com/api/v1/forecast/sol    # SOL
```
Or via the generic endpoint:
```
GET https://kronossignals.com/api/v1/forecast/btc?asset=BTC-USD&horizon=1h
```

ML directional price forecast from **Kronos-small** model (falls back to EMA/RSI/MACD/ATR composite heuristic if ML service is unavailable).

**Query params:**
- `asset`: `BTC-USD` | `ETH-USD` | `SOL-USD` (default: `BTC-USD`)
- `horizon`: `1h` | `4h` | `24h` (default: `1h`)

**Response fields (200):**
```json
{
  "asset": "BTC-USD",
  "horizon": "1h",
  "source": "Kronos-small",
  "generated_at": "...",
  "price": { "close": 107500, "atr": 850.42 },
  "forecast": {
    "up_prob": 0.62,
    "range_low": 106224.37,
    "range_high": 108775.63,
    "horizon_bars": 20,
    "confidence": 0.75,
    "expected_close": 107620.5,
    "pred_high": 108900,
    "pred_low": 106200,
    "pred_volatility": 0.0079,
    "prob_up": 0.62,
    "mean_path_closes": [...],   // optional
    "quantiles": { "p10": 106350, "p25": 107100, "p50": 107620.5, "p75": 108150, "p90": 108900 }
  },
  "model": "Kronos-small",
  "inference_seconds": 0.23,
  "disclaimer": "..."
}
```

**Composite fallback additions** (when ML unavailable):
- `indicators`: `{ ema20, ema50, rsi14, macd, macd_signal, macd_hist, atr14 }`
- `signal.votes`: 6-element array `[close>EMA20, close>EMA50, EMA20>EMA50, RSI, MACD, MACDhist]`
- `risk_state`: `"elevated"` | `"normal"` (elevated when ATR/close > 2%)
- `directional_context.direction`: `"positive"` | `"negative"` | `"neutral"`

---

## Cost Reference Table

| Endpoint | Cost | Best for |
|---|---|---|
| `/api/health` | **FREE** | Connectivity check |
| `/api/stats` | **FREE** | API health overview |
| `/api/v1/price/{asset}` | $0.01 | Quick price lookup; use `?coins=` for batching |
| `/api/v1/signals/{asset}` | $0.02 | Derivatives intelligence (funding, OI, basis) |
| `/api/v1/alerts/btc` | $0.02 | BTC regime alerts only |
| `/api/v1/overview` | $0.02 | Cross-asset derivatives scan |
| `/api/v1/funding-extremes` | $0.01 | Full-market funding extremes screener |
| `/api/v1/fear-greed` | $0.01 | Market sentiment index |
| `/api/v1/ohlc/{asset}` | $0.01 | OHLC candlestick data |
| `/api/v1/volatility/{asset}` | $0.01 | 7d/30d realized volatility |
| `/api/v1/snapshot/{asset}` | **$0.08** | **Everything for one asset in one call** |
| `/api/v1/forecast/{asset}` | **$0.05** | ML directional forecast (BTC/ETH/SOL only) |

---

## Error Codes

| HTTP | Meaning | Action |
|---|---|---|
| 200 | Success (payment accepted) | Parse response body |
| 402 | Payment required | Read `X-PAYMENT-REQUIRED` header, sign, retry |
| 409 | Nonce already used (replay) | Generate a new payment nonce |
| 503 | Upstream data unavailable | Retry after 30s; use cached data if available |

---

## Decision Guide: Which Endpoint to Use?

```
Need spot price only?
  → /api/v1/price/{asset}?coins=ETH,SOL   ($0.01, batch 3 prices)

Need funding/OI for one asset?
  → /api/v1/signals/{asset}   ($0.02)

Need BTC regime alerts?
  → /api/v1/alerts/btc   ($0.02)

Need price + derivatives + forecast for one asset?
  → /api/v1/snapshot/{asset}   ($0.08 — cheaper than buying separately)

Need ML forecast probability + price range?
  → /api/v1/forecast/btc|eth|sol   ($0.05, BTC/ETH/SOL only)

Need to scan which asset has the most extreme funding?
  → /api/v1/funding-extremes   ($0.01)

Need overall market sentiment?
  → /api/v1/fear-greed   ($0.01)

Need candles for TA?
  → /api/v1/ohlc/{asset}   ($0.01)

Need to check if API is up before spending USDC?
  → /api/health   (FREE)
```

---

## Integration with crypto-signals-plugin

This skill is the primary data source for the `market-scout` agent in the crypto-signals-plugin. The recommended call sequence per 30-minute cycle:

1. **`/api/health`** (FREE) — verify API is reachable before spending USDC
2. **`/api/v1/snapshot/{asset}`** ($0.08) — for BTC/ETH/SOL (most data for the money)
3. **`/api/v1/price/{btc}?coins=BNB,XRP,DOGE`** ($0.01) — altcoin prices in batch
4. **`/api/v1/funding-extremes`** ($0.01) — market-wide squeeze screener
5. **`/api/v1/fear-greed`** ($0.01) — sentiment context

**Estimated per-cycle cost** for BTC+ETH+SOL snapshots + screener + sentiment:
- 3 × $0.08 + $0.01 + $0.01 = **$0.26 USDC/cycle**
- At 48 cycles/day = **$12.48/day max** (within `DAILY_SPEND_CAP_USDC=15.0`)
