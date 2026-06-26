---
name: over-computer
description: >-
  Trade on prediction markets through over.computer.
  Browse markets, approve funds, place buy/sell orders, and check positions
  on Myriad. Use when the operator mentions trading, markets, predictions,
  placing orders, checking positions, or approving funds.
homepage: https://over.computer
credentials:
  - name: OVER_API_KEY
    description: Bearer token API key for authenticating with over-computer-validator-1002664526717.europe-north2.run.app
    required: true
    sensitive: true
---

# over.computer

Trade on prediction markets through the over.computer API.

Use this when the operator says things like:
- check markets
- place an order / buy / sell
- approve funds
- show my positions
- list my orders

## Getting started

If `OVER_API_KEY` is not set, help the operator register:

**Option A — agent-initiated:**

1. Call the link endpoint (no auth required) to obtain a registration URL:

```bash
curl -s --request GET \
  --url https://over-computer-validator-1002664526717.europe-north2.run.app/config/link
```

This returns `{ "configId": "<uuid>", "url": "<registration_url>" }`.

2. Give the operator the `url` and ask them to open it, connect their wallet on over.computer, and copy the API key shown after setup.
3. Once the operator provides the key, store it as `OVER_API_KEY`.

**Option B — operator-initiated:**

1. The operator goes to https://over.computer directly, registers, and obtains an API key.
2. The operator gives the key to you.

## Authentication

All endpoints under `/myriad/*` and `/agent/*` require the header:

```
Authorization: Bearer $OVER_API_KEY
```

## Get your config

Retrieve your agent’s configuration from the operator (same auth as Myriad routes):

```bash
curl -s --request GET \
  --url https://over-computer-validator-1002664526717.europe-north2.run.app/agent/config \
  --header "Authorization: Bearer $OVER_API_KEY"
```

Returns: `{ "prompt": "...", "label": "..." }` (either field may be `null` if unset).

- **`prompt`** — trading instructions from the operator; follow them as your directive.
- **`label`** — your agent’s display name.

Guardrails (position limits, trade limits, allowed markets, etc.) are enforced server-side and are **not** exposed on this endpoint. If an order violates a guardrail, the execute endpoint will reject it with a clear reason.

## Browse markets

List open markets:

```bash
curl -s --request GET \
  --url "https://over-computer-validator-1002664526717.europe-north2.run.app/myriad/markets?state=open&limit=10&page=1" \
  --header "Authorization: Bearer $OVER_API_KEY"
```

Query parameters: `limit` (number), `page` (number), `state` (string, default `open`).

Get details for a specific market:

```bash
curl -s --request GET \
  --url "https://over-computer-validator-1002664526717.europe-north2.run.app/myriad/markets/{slug}" \
  --header "Authorization: Bearer $OVER_API_KEY"
```

## Place an order

```bash
curl -s --request POST \
  --url https://over-computer-validator-1002664526717.europe-north2.run.app/myriad/order/execute \
  --header "Authorization: Bearer $OVER_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
  "idempotency_key": "unique-key-per-order",
  "order": {
    "market_id": 123,
    "outcome_id": 0,
    "side": "BUY",
    "size": 50,
    "slippage": 0.05
  }
}'
```

Body fields:
- `idempotency_key` (string, required) — unique key to prevent duplicate orders
- `order.market_id` (number, required)
- `order.outcome_id` (number, required)
- `order.side` (`"BUY"` | `"SELL"`, required)
- `order.size` (number, required) — order size in token units
- `order.slippage` (number, optional)

A duplicate `idempotency_key` returns HTTP 400 with the existing order.

## Check positions

```bash
curl -s --request GET \
  --url https://over-computer-validator-1002664526717.europe-north2.run.app/myriad/order/positions \
  --header "Authorization: Bearer $OVER_API_KEY"
```

## Order history

```bash
curl -s --request GET \
  --url https://over-computer-validator-1002664526717.europe-north2.run.app/myriad/order/list \
  --header "Authorization: Bearer $OVER_API_KEY"
```

## Config guardrails

The operator's config may restrict what the agent can do:
- **allowed_markets** — whitelist of permitted market IDs
- **max_order_size** — maximum USD value per order
- **max_trades_per_day** — daily trade limit

When a request violates a guardrail the API returns an error with a clear reason, for example:
- `"Market 456 is not in the allowed markets list"`
- `"Order size 200 * price 1 exceeds max allowed 100"`
- `"Trades per day 10 exceeds max allowed 5"`

When this happens:
1. Do **not** retry the request.
2. Tell the operator the exact rejection reason.
3. Ask the operator to update their config at https://over.computer — only humans can change config settings.

## Error reference

- `400` — Bad request or duplicate `idempotency_key`
- `401` — Missing or invalid API key
- `403` — Agent has no associated user or no config found
- `404` — Resource not found
- `500` — Server error (includes guardrail rejections wrapped in order execution)

If execution cannot proceed due to missing credentials or API errors, inform the operator and stop. Do not retry failed requests without operator confirmation.
