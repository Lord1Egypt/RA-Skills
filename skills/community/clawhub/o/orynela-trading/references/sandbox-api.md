# Sandbox API Reference

Complete reference for the Orynela Sandbox API.

## Base URL

```
https://orynela.ai/api/sandbox
```

## Authentication

All endpoints except `/status` require a valid sandbox API key.

- `Authorization: Bearer olab_xxxx`
- or `X-Orynela-Key: olab_xxxx`

## Scopes

| Scope | Description |
|-------|-------------|
| `heartbeat:write` | Send heartbeats |
| `logs:write` | Push logs |
| `signal:write` | Publish signals |
| `order:simulate` | Request simulated orders |
| `portfolio:read` | Read sandbox portfolio |
| `market:read` | Read OHLCV market data (granted by default) |

## Endpoints

### GET /status
Health check. No auth required.

### POST /heartbeat
Scope: `heartbeat:write`

```json
{"status": "online", "latency_ms": 120, "version": "0.1.0"}
```

### POST /logs
Scope: `logs:write`

```json
{"level": "info", "message": "Decision: BUY AAPL", "context": {"reason": "RSI oversold"}}
```

### POST /signals
Scope: `signal:write`

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "side": "buy",
  "confidence": 0.72,
  "signal_type": "trend_observation",
  "reasoning": "EMA alignment, volume confirmation"
}
```

Response:
```json
{
  "ok": true,
  "signal_id": 123,
  "risk_status": "accepted",
  "environment": "sandbox",
  "real_execution": false
}
```

### POST /orders/simulate
Scope: `order:simulate`

```json
{
  "signal_id": 123,
  "symbol": "BTCUSDT",
  "side": "buy",
  "order_type": "market",
  "quantity": 0.01
}
```

Response includes `simulated_fill_price`, `fee`, `slippage`.

### GET /portfolio
Returns sandbox portfolio ($100K fictive initial balance), positions, P&L.

### GET /orders
Simulated order history.

### GET /signals
Signal history.

### GET /market/candles

Query params:
- `symbol` (required) — equity/ETF as-is, crypto as `XXXUSDT`, forex as 6-letter
- `timeframe` — `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- `limit` — up to 500 (default 100)

Response:
```json
{
  "environment": "sandbox",
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "count": 200,
  "source": "yahoo",
  "candles": [
    {"t": 1733400000000, "o": 68250.1, "h": 68420.0, "l": 68110.5, "c": 68390.2, "v": 1234.5}
  ]
}
```

## Rate Limits

10 requests per IP per minute per endpoint. 11th+ → 429.

## Error Responses

| HTTP | Error | Cause |
|------|-------|-------|
| 401 | `invalid_credentials` | Key missing/invalid/revoked |
| 403 | `forbidden_scope` | Missing required scope |
| 403 | `bot_not_active` | Bot not yet approved |
| 422 | `validation_failed` | Invalid payload field |
| 422 | `risk_rejected` | Risk Guard rejected |
| 429 | `rate_limit_exceeded` | Too many requests |
| 503 | `kill_switch_engaged` | Lab kill switch active |