---
name: gprophet-api
description: AI-powered stock prediction and market analysis for global markets
homepage: https://www.gprophet.com
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      env: ["GPROPHET_API_KEY"]
    primaryEnv: "GPROPHET_API_KEY"
---

# G-Prophet AI Skills Documentation

> Stock prediction and market analysis capabilities for AI agents

## Overview

G-Prophet is an AI-powered stock prediction platform that exposes its core capabilities through an external API for other AI agent systems. It supports global markets (China A-shares, US stocks, HK stocks, Crypto) and provides AI prediction, technical analysis, market sentiment, and deep analysis Skills.

## Basic Information

| Item | Description |
|------|-------------|
| API Base URL | `https://www.gprophet.com/api/external/v1` |
| Authentication | `X-API-Key` header |
| Key Format | `gp_sk_` prefix (e.g. `gp_sk_[REDACTED]_a1b2c3...`) |
| Response Format | JSON |
| Billing | Points-based, each call consumes corresponding points |

## Authentication

All requests must include an API Key in the HTTP header:

```
X-API-Key: gp_sk_[REDACTED]_your_api_key_here
```

API Keys can be created in the G-Prophet platform under "Settings → API Key Management".

### Security Recommendations

- Store API keys in environment variables (`GPROPHET_API_KEY`), not in code
- Use test/limited-scope keys for development and evaluation
- Monitor usage and billing regularly at https://www.gprophet.com/dashboard
- Rotate keys periodically and revoke compromised keys immediately
- Never commit API keys to version control or share them publicly

## Rate Limiting

All API requests are subject to per-key rate limiting (fixed window, per minute).

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed per minute |
| `X-RateLimit-Remaining` | Remaining requests in current window |
| `X-RateLimit-Reset` | Seconds until the rate limit window resets |

Default limit is **60 requests per minute** per API Key. When exceeded, the API returns HTTP 429:

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Max 60 requests per minute.",
    "details": {
      "limit_per_minute": 60,
      "retry_after_seconds": 45
    }
  }
}
```

The response includes a `Retry-After` header indicating how many seconds to wait.

## Quota Management

Each API Key has configurable daily and monthly call quotas. Quota = 0 means unlimited.

When quota is exceeded, the API returns HTTP 429:

```json
{
  "success": false,
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "Daily quota exceeded (100/100)",
    "details": {
      "resolution": "Upgrade your plan or wait for quota reset."
    }
  }
}
```

Check your current quota usage via `GET /account/balance`.

## Unified Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "metadata": {
    "request_id": "req_abc123",
    "timestamp": "2026-02-18T10:30:00Z",
    "processing_time_ms": 1250,
    "api_version": "v1"
  },
  "error": null
}
```

### Error Response

Errors return the appropriate HTTP status code (401, 402, 403, 404, 429, 500, 503) along with a JSON body:

```json
{
  "success": false,
  "data": null,
  "metadata": { ... },
  "error": {
    "code": "INVALID_SYMBOL",
    "message": "Stock symbol 'XXXXX' not found",
    "details": {}
  }
}
```

### Insufficient Points Response (402)

When points are insufficient, the API returns a detailed 402 response with actionable guidance:

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_POINTS",
    "message": "Insufficient points. Required: 20, available: 5.",
    "details": {
      "required": 20,
      "available": 5,
      "shortage": 15,
      "resolution": {
        "actions": [
          { "action": "register", "url": "https://gprophet.com/register" },
          { "action": "recharge", "url": "https://gprophet.com/membership" },
          { "action": "subscribe", "url": "https://gprophet.com/membership" }
        ]
      }
    }
  }
}
```

## Points Cost

| Skill | Endpoint | Points/Call |
|-------|----------|-------------|
| Stock Prediction | `POST /predictions/predict` | CN 10, HK 15, US 20, Crypto 20 |
| Algorithm Compare | `POST /predictions/compare` | Single prediction cost × number of algorithms |
| Quote | `GET /market-data/quote` | 5 |
| History | `GET /market-data/history` | 5 |
| Search | `GET /market-data/search` | 5 |
| Batch Quote | `POST /market-data/batch-quote` | 5 × number of symbols |
| Technical Analysis | `POST /technical/analyze` | 5 |
| Fear & Greed Index | `GET /sentiment/fear-greed` | 5 |
| Market Overview | `GET /sentiment/market-overview` | 5 |
| AI Stock Analysis | `POST /analysis/stock` | 58 |
| Deep Analysis | `POST /analysis/comprehensive` | 150 |
| Task Polling | `GET /analysis/task/{task_id}` | 0 (free) |
| Account Balance | `GET /account/balance` | 0 (free) |
| Usage Statistics | `GET /account/usage` | 0 (free) |
| API Info | `GET /info` | 0 (free) |

---
## Skill 1: Stock Price Prediction

Predict future stock/cryptocurrency price movements using AI algorithms. Supports G-Prophet2026V1, LSTM, Transformer, and more.

### POST /predictions/predict

**Request Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | ✅ | - | Stock/crypto ticker (e.g. AAPL, 600519, BTCUSDT) |
| market | string | ✅ | - | Market code: `US`, `CN`, `HK`, `CRYPTO` |
| days | integer | No | 7 | Prediction days, range 1-30 |
| algorithm | string | No | auto | Algorithm: `auto`, `gprophet2026v1`, `lstm`, `transformer`, `random_forest`, `ensemble` |

**Example Request:**

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/predictions/predict" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "market": "US", "days": 7, "algorithm": "auto"}'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "market": "US",
    "current_price": 185.50,
    "predicted_price": 191.20,
    "change_percent": 3.07,
    "direction": "up",
    "confidence": 0.78,
    "prediction_days": 7,
    "algorithm_used": "gprophet2026v1",
    "data_quality": {
      "completeness": 1.0,
      "anomaly_count": 82,
      "missing_values": 0,
      "overall_score": 80
    },
    "points_consumed": 20
  }
}
```

### POST /predictions/compare

Multi-algorithm comparison prediction. Returns results from each algorithm and the best recommendation. Points cost = single prediction cost × number of algorithms.

**Request Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | ✅ | - | Stock/crypto ticker |
| market | string | ✅ | - | Market code: `US`, `CN`, `HK`, `CRYPTO` |
| days | integer | No | 5 | Prediction days, range 1-30 |
| algorithms | string[] | No | ["gprophet2026v1","lstm","transformer","ensemble"] | Algorithm list, max 6 |

**Example Request:**

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/predictions/compare" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA", "market": "US", "days": 5, "algorithms": ["gprophet2026v1", "lstm", "transformer"]}'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "symbol": "TSLA",
    "name": "Tesla Inc.",
    "market": "US",
    "current_price": 245.00,
    "prediction_days": 5,
    "results": [
      {
        "algorithm": "gprophet2026v1",
        "predicted_price": 252.30,
        "change_percent": 2.98,
        "direction": "up",
        "confidence": 0.82,
        "success": true
      },
      {
        "algorithm": "lstm",
        "predicted_price": 248.10,
        "change_percent": 1.27,
        "direction": "up",
        "confidence": 0.71,
        "success": true
      }
    ],
    "best_algorithm": "gprophet2026v1",
    "consensus_direction": "up",
    "average_predicted_price": 250.20,
    "points_consumed": 60
  }
}
```

---

## Skill 2: Market Data

Get real-time quotes, historical OHLCV data, search for stocks/crypto, and batch quotes. Each call costs 5 points (batch = 5 × count).

### GET /market-data/quote

Get real-time quote.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| symbol | string | ✅ | Stock/crypto ticker |
| market | string | ✅ | Market code: `US`, `CN`, `HK`, `CRYPTO` |

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/market-data/quote?symbol=AAPL&market=US" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "market": "US",
    "name": "Apple Inc.",
    "price": 185.50,
    "open": 183.90,
    "high": 186.80,
    "low": 183.20,
    "volume": 52340000,
    "previous_close": 183.20,
    "change": 2.30,
    "change_percent": 1.26,
    "points_consumed": 5
  }
}
```

### GET /market-data/history

Get historical OHLCV candlestick data.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | ✅ | - | Stock/crypto ticker |
| market | string | ✅ | - | Market code |
| period | string | No | 3m | Time range: `1w`, `1m`, `3m`, `6m`, `1y`, `2y` |

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/market-data/history?symbol=AAPL&market=US&period=3m" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "market": "US",
    "period": "3m",
    "data_points": 63,
    "history": [
      {
        "date": "2025-12-01",
        "open": 178.50,
        "high": 180.20,
        "low": 177.80,
        "close": 179.90,
        "volume": 48500000
      }
    ],
    "points_consumed": 5
  }
}
```

### GET /market-data/search

Search for stocks/crypto by keyword.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| keyword | string | ✅ | - | Search keyword |
| market | string | No | US | Market code |
| limit | integer | No | 10 | Result count, range 1-50 |

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/market-data/search?keyword=apple&market=US&limit=5" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

### POST /market-data/batch-quote

Get quotes for multiple symbols in a single request. Max 20 symbols. Cost = 5 points × number of symbols.

**Request Body (JSON):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| symbols | string[] | ✅ | List of stock/crypto tickers (max 20) |
| market | string | ✅ | Market code: `US`, `CN`, `HK`, `CRYPTO` |

**Example Request:**

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/market-data/batch-quote" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "TSLA", "GOOGL"], "market": "US"}'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "market": "US",
    "count": 3,
    "successful": 3,
    "results": [
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "success": true,
        "price": 185.50,
        "change": 2.30,
        "change_percent": 1.26
      },
      {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "success": true,
        "price": 245.00,
        "change": -3.20,
        "change_percent": -1.29
      },
      {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "success": true,
        "price": 142.80,
        "change": 1.10,
        "change_percent": 0.78
      }
    ],
    "points_consumed": 15
  }
}
```
---

## Skill 3: Technical Analysis

Calculate technical indicators and generate trading signals for a given stock. Each call costs 5 points.

### POST /technical/analyze

**Request Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | ✅ | - | Stock/crypto ticker |
| market | string | ✅ | - | Market code: `US`, `CN`, `HK`, `CRYPTO` |
| indicators | string[] | No | ["rsi","macd","bollinger","kdj"] | Indicators: `rsi`, `macd`, `bollinger`, `kdj`, `sma`, `ema` |

**Example Request:**

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/technical/analyze" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "market": "US", "indicators": ["rsi", "macd", "bollinger", "kdj"]}'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "market": "US",
    "current_price": 185.50,
    "indicators": {
      "rsi_14": { "value": 55.3, "signal": "neutral" },
      "macd": { "macd": 1.25, "signal": 0.98, "histogram": 0.27, "signal_type": "bullish" },
      "bollinger": { "upper": 192.0, "middle": 185.0, "lower": 178.0, "position": 0.54 },
      "kdj": { "k": 65.2, "d": 58.7, "j": 78.2 }
    },
    "signals": [
      { "type": "bullish", "indicator": "MACD" },
      { "type": "neutral", "indicator": "RSI" }
    ],
    "overall_signal": "bullish",
    "signal_strength": 0.5,
    "points_consumed": 5
  }
}
```

---

## Skill 4: Market Sentiment

Get market sentiment data including Fear & Greed Index and market overview. Each call costs 5 points.

### GET /sentiment/fear-greed

Get the crypto market Fear & Greed Index.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | integer | No | 1 | History days, 1=current only, range 1-365 |

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/sentiment/fear-greed?days=1" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "value": 72,
    "classification": "greed",
    "previous_value": 68,
    "change": 4,
    "points_consumed": 5
  }
}
```

### GET /sentiment/market-overview

Get comprehensive market overview (breadth, hot sectors, major indices).

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| market | string | No | CN | Market code: `CN`, `US` |

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/sentiment/market-overview?market=CN" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

---

## Skill 5: AI Stock Analysis (Async)

Single-stock AI analysis report using LLM. Costs 58 points. Supports CN, US, CRYPTO markets.

> ⚠️ **Async Mode**: Analysis typically takes 15-60 seconds, so this endpoint uses async mode.
> 1. `POST /analysis/stock` → Returns `task_id` immediately
> 2. `GET /analysis/task/{task_id}` → Poll for status; get results when `status=completed`
>
> Recommended polling interval: 5 seconds. Max wait: 5 minutes.

### POST /analysis/stock

Submit a stock analysis task. Returns task ID immediately.

**Request Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | ✅ | - | Stock/crypto ticker |
| market | string | ✅ | - | Market code: `US`, `CN`, `CRYPTO` |
| locale | string | No | zh-CN | Report language: `zh-CN`, `en-US` |
| callback_url | string | No | - | Webhook URL; results are POSTed on completion |

**Example Request:**

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/analysis/stock" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "market": "US", "locale": "en-US"}'
```

**Example Response (immediate):**

```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123def456",
    "symbol": "AAPL",
    "market": "US",
    "status": "pending",
    "points_consumed": 58,
    "poll_url": "/api/external/v1/analysis/task/task_abc123def456",
    "callback_url": null,
    "message": "Stock analysis started. Poll the task URL every 5 seconds for results."
  }
}
```

---

## Skill 6: Deep Analysis (Async)

Multi-agent collaborative deep analysis evaluating stocks from 5 dimensions: technical, fundamental, capital flow, sentiment, and macro environment. Costs 150 points.

> ⚠️ **Async Mode**: Deep analysis typically takes 30-120 seconds, so this endpoint uses async mode.
> 1. `POST /analysis/comprehensive` → Returns `task_id` immediately
> 2. `GET /analysis/task/{task_id}` → Poll for status; get results when `status=completed`
>
> Recommended polling interval: 5 seconds. Max wait: 5 minutes.

### POST /analysis/comprehensive

Submit a deep analysis task. Returns task ID immediately.

**Request Body (JSON):**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | ✅ | - | Stock/crypto ticker |
| market | string | ✅ | - | Market code: `US`, `CN`, `HK`, `CRYPTO` |
| locale | string | No | zh-CN | Report language: `zh-CN`, `en-US` |
| callback_url | string | No | - | Webhook URL; results are POSTed on completion |

**Example Request:**

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/analysis/comprehensive" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "market": "US", "locale": "en-US"}'
```

**Example Response (immediate):**

```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123def456",
    "symbol": "AAPL",
    "market": "US",
    "status": "pending",
    "points_consumed": 150,
    "poll_url": "/api/external/v1/analysis/task/task_abc123def456",
    "callback_url": null,
    "message": "Analysis started. Poll the task URL every 5 seconds for results."
  }
}
```

### Webhook Callback

Both `/analysis/stock` and `/analysis/comprehensive` accept an optional `callback_url` parameter. When provided, the API will POST the task result to that URL upon completion or failure:

**Callback Payload (success):**

```json
{
  "task_id": "task_abc123def456",
  "status": "completed",
  "result": { ... }
}
```

**Callback Payload (failure):**

```json
{
  "task_id": "task_abc123def456",
  "status": "failed",
  "error": "Analysis service timeout"
}
```

### GET /analysis/task/{task_id}

Poll analysis task status and results.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| task_id | string | Task ID returned by analysis endpoints |

**Status Flow:** `pending` → `running` (progress 0-100) → `completed` / `failed`

**Example Response (completed):**

```json
{
  "success": true,
  "data": {
    "task_id": "task_abc123def456",
    "status": "completed",
    "progress": 100,
    "message": "Analysis completed",
    "result": {
      "symbol": "AAPL",
      "asset_type": "stock_us",
      "analysis": {
        "overall_rating": "bullish",
        "confidence": 0.75,
        "agents": {
          "technical": { "rating": "bullish", "confidence": 0.80 },
          "fundamental": { "rating": "neutral", "confidence": 0.65 },
          "capital_flow": { "rating": "bullish", "confidence": 0.70 },
          "sentiment": { "rating": "neutral", "confidence": 0.60 },
          "macro": { "rating": "cautious", "confidence": 0.55 }
        },
        "final_recommendation": "Short-term bullish, consider buying on dips",
        "risk_level": "medium"
      }
    },
    "error": null
  }
}
```
---

## Account Endpoints

### GET /account/balance

Check current API Key's points balance and quota usage. Free, no points consumed.

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/account/balance" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "available_points": 1250,
    "key_name": "My Trading Bot",
    "key_prefix": "gp_sk_abc",
    "scopes": ["predictions", "market_data", "technical", "sentiment", "analysis"],
    "rate_limit_per_minute": 60,
    "daily_quota": 1000,
    "daily_used": 42,
    "monthly_quota": 0,
    "monthly_used": 856
  }
}
```

### GET /account/usage

Get call history statistics for the current API Key. Free, no points consumed.

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | integer | No | 7 | History days, range 1-90 |

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/account/usage?days=7" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "key_prefix": "gp_sk_abc",
    "period_days": 7,
    "daily": [
      {
        "date": "2026-03-09",
        "total_calls": 85,
        "success_calls": 82,
        "avg_response_ms": 1250
      }
    ],
    "by_endpoint": [
      { "endpoint": "/api/external/v1/predictions/predict", "calls": 45 },
      { "endpoint": "/api/external/v1/market-data/quote", "calls": 30 }
    ]
  }
}
```

### GET /info

Get API metadata: supported markets, algorithms, pricing table, authentication info. Free, no points consumed.

**Example Request:**

```bash
curl "https://www.gprophet.com/api/external/v1/info" \
  -H "X-API-Key: gp_sk_[REDACTED]_your_key"
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| MISSING_API_KEY | 401 | Missing X-API-Key header |
| INVALID_KEY_FORMAT | 401 | Invalid API Key format (must start with gp_sk_) |
| INVALID_API_KEY | 401 | Invalid API Key |
| API_KEY_DISABLED | 403 | API Key has been disabled |
| API_KEY_EXPIRED | 403 | API Key has expired |
| INSUFFICIENT_SCOPE | 403 | API Key lacks permission for this Skill |
| INSUFFICIENT_POINTS | 402 | Insufficient points |
| POINTS_DEDUCTION_FAILED | 500 | Failed to deduct points |
| OWNER_NOT_FOUND | 403 | API Key owner account not found |
| RATE_LIMITED | 429 | Request frequency exceeded per-minute limit |
| QUOTA_EXCEEDED | 429 | Daily or monthly call quota exhausted |
| INVALID_MARKET | 400 | Unsupported market code |
| UNSUPPORTED_MARKET | 400 | Market not supported for this endpoint |
| SYMBOL_NOT_FOUND | 404 | Stock/crypto ticker not found |
| NO_DATA | 404 | Unable to retrieve data |
| TOO_MANY_ALGORITHMS | 400 | Too many algorithms (max 6) |
| PREDICTION_FAILED | 500 | Prediction service error |
| ANALYSIS_FAILED | 500 | Analysis service error |
| TASK_NOT_FOUND | 404 | Async task not found or expired |
| FORBIDDEN | 403 | Access denied (e.g. querying another user's task) |
| DATA_UNAVAILABLE | 503 | Data source temporarily unavailable |
| INTERNAL_ERROR | 500 | Internal service error |

---

## MCP Tools Definitions

MCP (Model Context Protocol) tool definitions for use with Claude, Kiro, and other MCP-compatible agents:

### gprophet_predict

```json
{
  "name": "gprophet_predict",
  "description": "Predict stock/crypto price using AI. Markets: US, CN, HK, CRYPTO. Algorithms: auto, gprophet2026v1, lstm, transformer, random_forest, ensemble. IMPORTANT: The response includes 'symbol', 'name' (official stock name), and 'market' fields — always use these values directly, never infer or fabricate the stock name from the symbol.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string", "description": "Stock/crypto symbol (e.g., AAPL, 600519, BTCUSDT)" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"] },
      "days": { "type": "integer", "minimum": 1, "maximum": 30, "default": 7 },
      "algorithm": { "type": "string", "default": "auto" }
    },
    "required": ["symbol", "market"]
  }
}
```

### gprophet_quote

```json
{
  "name": "gprophet_quote",
  "description": "Get real-time stock/crypto quote.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string", "description": "Stock/crypto symbol" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"] }
    },
    "required": ["symbol", "market"]
  }
}
```

### gprophet_batch_quote

```json
{
  "name": "gprophet_batch_quote",
  "description": "Get quotes for multiple symbols at once (max 20). Cost = 5 points × number of symbols.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbols": { "type": "array", "items": { "type": "string" }, "description": "List of symbols (max 20)" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"] }
    },
    "required": ["symbols", "market"]
  }
}
```

### gprophet_history

```json
{
  "name": "gprophet_history",
  "description": "Get historical OHLCV price data.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"] },
      "period": { "type": "string", "enum": ["1w", "1m", "3m", "6m", "1y", "2y"], "default": "3m" }
    },
    "required": ["symbol", "market"]
  }
}
```

### gprophet_search

```json
{
  "name": "gprophet_search",
  "description": "Search for stocks/crypto by keyword.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "keyword": { "type": "string" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"], "default": "US" },
      "limit": { "type": "integer", "minimum": 1, "maximum": 50, "default": 10 }
    },
    "required": ["keyword"]
  }
}
```

### gprophet_technical

```json
{
  "name": "gprophet_technical",
  "description": "Calculate technical indicators (RSI, MACD, Bollinger, KDJ, SMA, EMA) and generate trading signals.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"] },
      "indicators": { "type": "array", "items": { "type": "string", "enum": ["rsi", "macd", "bollinger", "kdj", "sma", "ema"] }, "default": ["rsi", "macd", "bollinger", "kdj"] }
    },
    "required": ["symbol", "market"]
  }
}
```

### gprophet_fear_greed

```json
{
  "name": "gprophet_fear_greed",
  "description": "Get crypto market Fear & Greed Index.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "days": { "type": "integer", "minimum": 1, "maximum": 365, "default": 1 }
    }
  }
}
```

### gprophet_market_overview

```json
{
  "name": "gprophet_market_overview",
  "description": "Get market overview: breadth, hot concepts, major indices.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "market": { "type": "string", "enum": ["CN", "US"], "default": "CN" }
    }
  }
}
```

### gprophet_analyze_stock

```json
{
  "name": "gprophet_analyze_stock",
  "description": "Run AI stock analysis report (58 points, async). Returns task_id for polling via gprophet_task_status. Supports US, CN, CRYPTO markets.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "market": { "type": "string", "enum": ["US", "CN", "CRYPTO"] },
      "locale": { "type": "string", "enum": ["zh-CN", "en-US"], "default": "en-US" }
    },
    "required": ["symbol", "market"]
  }
}
```

### gprophet_analyze_comprehensive

```json
{
  "name": "gprophet_analyze_comprehensive",
  "description": "Run multi-agent comprehensive analysis (150 points, async). Returns task_id for polling via gprophet_task_status. Evaluates from 5 dimensions: technical, fundamental, capital flow, sentiment, macro.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "market": { "type": "string", "enum": ["US", "CN", "HK", "CRYPTO"] },
      "locale": { "type": "string", "enum": ["zh-CN", "en-US"], "default": "en-US" }
    },
    "required": ["symbol", "market"]
  }
}
```

### gprophet_task_status

```json
{
  "name": "gprophet_task_status",
  "description": "Check the status of an async analysis task. Poll every 5 seconds until status is 'completed' or 'failed'.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": { "type": "string", "description": "Task ID returned by analysis endpoints" }
    },
    "required": ["task_id"]
  }
}
```

### gprophet_balance

```json
{
  "name": "gprophet_balance",
  "description": "Check current points balance, quota usage, and API key info. Free.",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```

### gprophet_info

```json
{
  "name": "gprophet_info",
  "description": "Get API metadata: supported markets, algorithms, pricing table. Free.",
  "inputSchema": { "type": "object", "properties": {}, "required": [] }
}
```
---

## Integration Guide

### Typical Prediction Flow

```
1. Call gprophet_predict to get prediction results (sync, typically 5-30 seconds)
2. Use data.direction and data.confidence to assess the trend
3. Optional: Call gprophet_technical for technical confirmation
```

### Typical Stock Analysis Flow

```
1. Call gprophet_analyze_stock to submit analysis task → get task_id
2. Poll gprophet_task_status every 5 seconds
3. When status = "completed", read the analysis report from result
4. When status = "failed", read the failure reason from error
```

### Typical Deep Analysis Flow

```
1. Call gprophet_analyze_comprehensive to submit analysis task → get task_id
2. Poll gprophet_task_status every 5 seconds
3. When status = "completed", read the full report from result.analysis
4. When status = "failed", read the failure reason from error
```

### Webhook Integration Flow

```
1. Call POST /analysis/stock or /analysis/comprehensive with callback_url
2. Continue processing other tasks (no need to poll)
3. Receive POST to your callback_url when task completes or fails
4. Verify task_id and process the result
```

### Agent Integration Tips

- **Search before predicting**: If unsure about a ticker, use `gprophet_search` to confirm first
- **Combine skills**: Prediction + Technical Analysis + Sentiment = more comprehensive judgment
- **Points management**: Use `gprophet_balance` to check points before expensive operations
- **Batch operations**: Use `gprophet_batch_quote` instead of multiple single quotes to save API calls
- **Error handling**: Check the `success` field; on failure, refer to `error.code` for retry logic
- **Rate limiting**: Respect `X-RateLimit-Remaining` header; back off when approaching 0
- **Webhooks**: Use `callback_url` for analysis tasks to avoid polling overhead

### Python SDK

Install the official Python SDK for easier integration:

```bash
pip install gprophet
```

```python
from gprophet import GProphet

client = GProphet(api_key="gp_sk_...")

# Predict stock price
result = client.predict("AAPL", market="US", days=7)

# Batch quote
quotes = client.batch_quote(["AAPL", "TSLA", "GOOGL"], market="US")

# Stock analysis (auto-polls until complete)
analysis = client.analyze_stock("AAPL", market="US", wait=True)

# Check balance
balance = client.balance()
```

### MCP Server

Run the standalone MCP server for AI agent integration:

```json
{
  "mcpServers": {
    "gprophet": {
      "command": "python",
      "args": ["path/to/gprophet_mcp_server.py"],
      "env": { "GPROPHET_API_KEY": "gp_sk_..." }
    }
  }
}
```

---

## Supported Market Codes

| Code | Market | Ticker Format | Example Tickers |
|------|--------|---------------|-----------------|
| CN | China A-shares | 6-digit number. 6xxxxx=Shanghai, 0/3xxxxx=Shenzhen | 600519, 000001, 300750 |
| US | US Stocks | Alphabetic ticker symbol | AAPL, TSLA, GOOGL, MSFT |
| HK | Hong Kong Stocks | Numeric code (no zero-padding needed) | 700, 9988, 1810, 3007 |
| CRYPTO | Cryptocurrency | Trading pair (ending in USDT) | BTCUSDT, ETHUSDT, SOLUSDT |

> ⚠️ **A-share Ticker Notes**:
> - A-share tickers are **6-digit numbers**; different prefixes indicate different exchanges/boards
> - `6xxxxx` = Shanghai Stock Exchange (Main Board / STAR Market)
> - `0xxxxx` = Shenzhen Stock Exchange (Main Board / SME Board)
> - `3xxxxx` = Shenzhen Stock Exchange (ChiNext / Growth Enterprise Market)
> - Make sure to pass the correct 6-digit code, e.g. `600986` and `000001` are different stocks

## Supported Prediction Algorithms

| Algorithm | Description |
|-----------|-------------|
| auto | Automatically select the best algorithm |
| gprophet2026v1 | G-Prophet2026V1 proprietary model (recommended) |
| lstm | Long Short-Term Memory network |
| transformer | Transformer model |
| random_forest | Random Forest |
| ensemble | Ensemble learning (multi-algorithm fusion) |