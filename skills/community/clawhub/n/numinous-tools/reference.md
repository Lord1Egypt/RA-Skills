# Numinous API Reference

Full endpoint schemas and edge cases. Load when SKILL.md's tables don't have enough detail.

## Authentication

Three mutually exclusive paths. A given endpoint usually supports one or two of them.

| Method | Header / mechanism | Which endpoints accept it |
|---|---|---|
| **API key** | `X-API-Key: <key>` | forecast create, signals, `/me/*` |
| **x402 payment** | `PAYMENT-SIGNATURE: <proof>` (set by x402 client lib after reading 402 response) | forecast create only |
| **Browser session** | `access_token` JWT cookie (from eversight login) | `/credits/*`, `/api-keys/*`, chat, threads (not used from agents) |

Polling a forecast result (`GET /forecasters/prediction-jobs/{id}`) requires **no auth** — the UUID acts as the access token. Keep prediction IDs private.

Leaderboard, miner metadata, agent code, and `/credits/costs` are fully public.

## Forecast — `POST /api/v1/forecasters/prediction-jobs`

Base: `https://api.numinouslabs.io`

Creates an async prediction job. Returns `202` + `prediction_id`. Poll the GET endpoint for the result.

### Request body

Two mutually exclusive modes. Send fields for one mode only (the API accepts either shape).

**Query mode** — let Numinous parse a natural-language question:
```json
{
  "query": "Will Bitcoin exceed $150,000 before end of 2026?",
  "agent_version_id": null
}
```

**Structured mode** — supply the event spec directly (more precise, no parsing step):
```json
{
  "title": "Will Bitcoin exceed $150,000 before end of 2026?",
  "description": "Resolves YES if BTC spot price on any major exchange reaches $150,000 USD at any point before 2026-12-31T23:59:59Z.",
  "cutoff": "2026-12-31T23:59:59Z",
  "topics": ["crypto", "finance"],
  "agent_version_id": null
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `query` | string | query mode only | Natural language. Parsed server-side into title/description/cutoff/topics. |
| `title` | string | structured only | Yes/no question form. |
| `description` | string | structured only | Explicit resolution criteria. |
| `cutoff` | ISO 8601 datetime | structured only | After this time no more predictions are accepted. |
| `topics` | array[string] | no | e.g. `["crypto", "finance"]`. Improves routing. Default `[]`. |
| `agent_version_id` | UUID | no | Pin a specific miner version. Unset → pool-based default miner. |

### Response — `202 Accepted`

```json
{
  "prediction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "PENDING"
}
```

## Poll forecast — `GET /api/v1/forecasters/prediction-jobs/{prediction_id}`

No auth. Poll every ~5s; typical completion 25–120s.

### Response — `200 OK`

```json
{
  "prediction_id": "...",
  "status": "COMPLETED",
  "created_at": "2026-04-17T15:29:37Z",
  "result": {
    "prediction": 0.24,
    "forecaster_name": "pool_based_miner_forecaster",
    "forecasted_at": "2026-04-17T15:30:02Z",
    "metadata": {
      "pool": "global_brier",
      "miner_uid": 69,
      "miner_hotkey": "5GsATpa17oA7...",
      "agent_name": "lattice",
      "version_id": "7aee2ecc-...",
      "version_number": 2,
      "raw_prediction": 0.24,
      "event_title": "Will Bitcoin (BTC) exceed $150,000 before end of 2026?",
      "event_cutoff": "2026-12-31T23:59:59+00:00",
      "reasoning": "Markdown string with citations...",
      "total_cost_usd": "0.05762325",
      "gateway_call_stats": { "/api/gateway/openai/responses": { "count": 1, "cost_usd": "0.057" } }
    },
    "parsed_fields": {
      "title": "...",
      "description": "...",
      "cutoff": "2026-12-31T23:59:59Z",
      "topics": ["crypto", "economics", "finance"]
    }
  },
  "error": null
}
```

### Status values

| Status | Meaning |
|---|---|
| `PENDING` | Accepted, waiting for a miner slot. |
| `RUNNING` | Miner is computing. |
| `COMPLETED` | Done. `result` populated. |
| `FAILED` | Failed. `error` populated, `result` null. |

### Forecaster names

| Name | When |
|---|---|
| `pool_based_miner_forecaster` | Default (no `agent_version_id`) — network picks top miner in the active pool. |
| `miner_forecaster` | When `agent_version_id` is pinned. |
| `baseline` | Internal baseline fallback. |

### Notes

- `parsed_fields` is populated **only in query mode**. It's `null` in structured mode.
- `metadata.reasoning` is markdown with inline citations. Worth rendering verbatim to the user.
- `metadata.gateway_call_stats` exposes the miner's internal LLM spend (transparency — not a charge to the user).
- `metadata.pool` values: `global_brier` (default), `reasoning`, `geopolitics_brier`.

## Signals — `POST /api/v1/signals`

Base: `https://signals.numinouslabs.io`. API key only (no x402).

### Request body

Send exactly one of `market` or `question`. Validator enforces this.

```json
{
  "market": "https://polymarket.com/event/some-slug",
  "question": null,
  "relevance_threshold": 0.25,
  "max_events_per_source": 25,
  "time_window_hours": 72
}
```

| Field | Type | Default | Notes |
|---|---|---|---|
| `market` | string | null | Polymarket URL / slug / condition_id. Compound event URLs auto-resolve if the event has exactly one sub-market; otherwise you'll get a `MarketNotFoundError` listing the available sub-market slugs. |
| `question` | string | null | Free-text question. Passthrough — no parsing. |
| `relevance_threshold` | float 0-1 | 0.25 | Signals below this are dropped from the response. |
| `max_events_per_source` | int 1-100 | 25 | Cap per source before dedup. |
| `time_window_hours` | int 1-720 | 72 | Lookback window. |

### Response — `200 OK`

```json
{
  "signals": [
    {
      "headline": "...",
      "source": "indicia_iran",
      "timestamp": "2026-04-17T15:30:49Z",
      "relevance_score": 0.92,
      "impact_score": 0.78,
      "impact_bucket": "S3",
      "direction": "supports_yes",
      "rationale": "One-sentence explanation.",
      "source_url": "https://..."
    }
  ],
  "source_weights": [
    { "source_name": "exa", "event_count": 12, "avg_relevance_score": 0.45, "avg_impact_score": 0.32 }
  ],
  "total_event_count": 87,
  "filtered_count": 34,
  "failed_sources": [],
  "question_context": "Resolved question text",
  "scenario_analysis": null,
  "processing_metadata": {
    "duration_seconds": 4.23,
    "llm_scored_count": 87,
    "total_ingested_events": 87,
    "question_text": "...",
    "market_yes_price": 0.18
  }
}
```

### Sources

Each `signal.source` is one of:

| Source | Fetches |
|---|---|
| `exa` | Web news via Exa Search |
| `perplexity` | AI-researched findings via Perplexity Sonar |
| `indicia_liveuamap` | Ukraine/conflict strike events |
| `indicia_gdelt` | Global news events from GDELT |
| `indicia_iran` | Iran geopolitical events |
| `indicia_polymarket` | Active Polymarket geopolitics markets |
| `indicia_geopolitical` | Generated geopolitical forecast questions |
| `indicia_unusual_whales` | Market/news feed |

### `impact_bucket` (scenario escalation ladder)

The ladder is generated per-question (scenario-specific), but buckets follow a consistent escalation shape:

| Bucket | Meaning |
|---|---|
| `S0` | Routine noise — no real program movement |
| `S1` | Peripheral / low-impact update |
| `S2` | Moderate escalation / meaningful program update |
| `S3` | Strong escalation / direct evidence of the scenario |
| `S4` | Near-resolution — structural change that makes the YES outcome highly probable |
| `S5` | Event has resolved (or functionally resolved) in favor of YES |

Most real-world responses cluster in S0–S3; S4/S5 appear when the scenario is imminent or realized.

### Error responses

| Status | Code | When |
|---|---|---|
| 404 | `MARKET_NOT_FOUND` | Slug / condition_id doesn't resolve. If it's a multi-market event, the error message lists sub-market slugs. |
| 422 | `VALIDATION_ERROR` | Both `market` and `question` sent, or neither. |
| 502 | `UPSTREAM_UNAVAILABLE` | Polymarket Gamma API unreachable. Transient; retry or use `--question`. |
| 500 | `INTERNAL_ERROR` | Unhandled. |

Shape: `{"detail": {"error_code": "...", "message": "..."}}`.

## `/me/balance` — current balance

`GET https://api-eversight.numinouslabs.io/api/v1/me/balance` — API-key authed.

```json
{ "balance": "1.5250", "currency": "credits" }
```

Multiply by `usd_per_credit` from `/credits/costs` to show USD equivalent.

## `/me/usage` — usage history

`GET https://api-eversight.numinouslabs.io/api/v1/me/usage?limit=50&since=2026-04-17T00:00:00Z` — API-key authed.

```json
{
  "transactions": [
    {
      "id": "uuid",
      "amount": "-0.0250",
      "type": "api_usage",
      "resource": "signal_compute",
      "description": "signal-compute",
      "reference_id": "uuid",
      "created_at": "2026-04-17T15:41:47Z"
    }
  ]
}
```

| Query param | Default | Limits |
|---|---|---|
| `limit` | 50 | 1–200 |
| `since` | none | ISO 8601 datetime |

Transactions are filtered to `api_usage` and `refund` types only — chat usage, bonuses, and Stripe top-ups are excluded (they're eversight-UI-only flows).

`resource` enum values: `signal_compute`, `prediction_job`. Use this to group spend by product.

## `/credits/costs` — current pricing (public)

`GET https://api-eversight.numinouslabs.io/api/v1/credits/costs` — no auth.

```json
{
  "usd_per_credit": "1.00",
  "min_purchase_usd": "1.00",
  "api_prediction_job": "0.1",
  "signal_compute": "0.025",
  "eversight_prediction_job": "0.1",
  "eversight_chat_message": "0",
  "eversight_signal_refresh": "0.2"
}
```

Only `api_prediction_job` and `signal_compute` are relevant for API users — the `eversight_*` costs are for the eversight web chat app.

## x402 payment flow (forecasts only)

### 402 response shape

When the forecast endpoint is hit without auth:

- HTTP status: `402`
- Body: `{}`
- Header: `payment-required` — base64-encoded JSON (x402 v2 schema)

Decoded header:
```json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "http://api.numinouslabs.io/api/v1/forecasters/prediction-jobs",
    "description": "Create a prediction job (paid via x402)",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "amount": "100000",
      "payTo": "0x5adB99dcABbecC69b88A210B20C5EcaD696E1D73",
      "maxTimeoutSeconds": 300,
      "extra": { "name": "USD Coin", "version": "2" }
    },
    {
      "scheme": "exact",
      "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
      "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "amount": "100000",
      "payTo": "Dt4uWE5AbLQ7NZFF9LqMLv9XBf45A1jDFxyYcWcVDZtb",
      "maxTimeoutSeconds": 300,
      "extra": { "feePayer": "D6ZhtNQ5nT9ZnTHUbqXZsTx5MH2rPFiBBggX4hY1WePM" }
    }
  ]
}
```

`amount` is in the asset's smallest unit — USDC has 6 decimals, so `100000` = $0.10.

### Python client (used by `scripts/forecast_x402.py`)

```python
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

account = Account.from_key(private_key_hex)
client = x402Client()
register_exact_evm_client(client, EthAccountSigner(account))

async with x402HttpxClient(client, timeout=60) as http:
    resp = await http.post(URL, json=PAYLOAD)
    # The lib handles 402 → sign → retry automatically
```

Install: `pip install 'x402[client]' eth-account httpx`.

Solana path: use `register_exact_svm_client` with an SVM signer — pattern identical.

## Miner & leaderboard endpoints (public)

All under `https://api.numinouslabs.io/api/v1/`.

| Path | Returns |
|---|---|
| `GET /leaderboard` | Top miners sorted by pool (default `global_brier`). |
| `GET /aggregated-scores` | Per-miner aggregated scores across pools. |
| `GET /miners/{uid}/{hotkey}/agents` | All agent versions a miner has submitted. |
| `GET /miners/{uid}/{hotkey}/agents/{version_id}/code` | Source code of a specific agent version. |
| `GET /agents/{version_id}/code` | Same as above but without requiring uid/hotkey. |
| `GET /miners/{uid}/{hotkey}/historical-ranking` | Rank over time. |
| `GET /miners/{uid}/{hotkey}/predictions/active` | Active predictions. |
| `GET /miners/{uid}/{hotkey}/runs/{event_id}` | What this miner predicted on a specific event. |
| `GET /miners/{uid}/{hotkey}/runs/{run_id}/logs` | Execution logs for a run. |
| `GET /miner-reasonings` | Recent reasoning snippets. |
| `GET /benchmarks/baseline` | Baseline forecaster benchmark. |
| `GET /causal-drivers/` | Causal-drivers endpoint. |
| `GET /deep-research/` | Deep-research endpoint. |

## Environment variables

| Var | Required | Used by |
|---|---|---|
| `NUMINOUS_API_KEY` | For API-key auth | `forecast.py`, `signals.py`, balance/usage curls |
| `NUMINOUS_X402_EVM_PRIVATE_KEY` | For x402 Base USDC | `forecast_x402.py` (EVM path) |
| `NUMINOUS_X402_SVM_PRIVATE_KEY` | For x402 Solana USDC | `forecast_x402.py` (SVM path, if extended) |
| `NUMINOUS_BASE_URL` | no | Override forecast API base (default `https://api.numinouslabs.io`). For testing. |
| `NUMINOUS_SIGNALS_URL` | no | Override signals base (default `https://signals.numinouslabs.io`). |
| `NUMINOUS_EVERSIGHT_URL` | no | Override eversight base (default `https://api-eversight.numinouslabs.io`). |

Never commit private keys or API keys. `.env` files should be gitignored.
