---
name: millimetric-track
description: Emit analytics events to Millimetric (track, identify, batch, forget). Use when the user wants to send a custom event, log a signup/purchase/pageview, link an anonymous visitor to a user_id, bulk-import events, or process a GDPR delete request.
metadata: { "openclaw": { "requires": { "env": ["MILLIMETRIC_KEY"], "bins": ["curl"] }, "primaryEnv": "MILLIMETRIC_KEY", "emoji": "📡", "homepage": "https://api.millimetric.ai" } }
---

# Millimetric Track

Send analytics events to Millimetric's API. Server-side keys only (`sk_live_…`). The classifier auto-derives `source`/`medium`/`campaign` from `url` + `referrer` + click IDs — don't try to set those yourself.

## When to Use

- User asks to log/track/emit/send/record an event
- Linking an anonymous visitor to a known user (`identify`)
- Bulk-uploading events from a backfill or webhook
- Processing a "forget me" / GDPR erasure request
- Wiring server-side instrumentation (Express, Fastify, Hono, Next.js route handler, cron job, queue worker)

## When NOT to Use

- Reading data → use `millimetric-query`
- Connecting an AI agent to Millimetric → use `millimetric-mcp-setup`
- Browser instrumentation → tell the user to drop in the `<script src="https://cdn.millimetric.ai/v1/a.js" data-key="pk_live_…">` snippet instead — `pk_*` keys must never appear in shell or server code

## Setup

```bash
export MILLIMETRIC_KEY=sk_live_...     # server key, scope: ingest
export MILLIMETRIC_HOST=https://api.millimetric.ai
```

For local dev against the Worker: `MILLIMETRIC_HOST=http://localhost:8787`.

## Quick start

### Track a single event

```bash
curl -X POST "$MILLIMETRIC_HOST/v1/track" \
  -H "Authorization: Bearer $MILLIMETRIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "signup",
    "anonymous_id": "u_abc",
    "user_id": "user_42",
    "url": "https://yoursite.com/?utm_source=facebook&utm_medium=cpc&fbclid=abc",
    "properties": { "plan": "free" }
  }'
```

Response: `202 Accepted`, body `{ "ok": true, "event_id": "..." }`.

### Identify (link anonymous → user)

```bash
curl -X POST "$MILLIMETRIC_HOST/v1/identify" \
  -H "Authorization: Bearer $MILLIMETRIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "anonymous_id": "u_abc",
    "user_id": "user_42",
    "traits": { "email": "matt@example.com", "plan": "pro" }
  }'
```

After this, include `user_id` on every subsequent `track` call for that visitor.

### Batch (up to 500 events per request, ≤256 KB body)

```bash
curl -X POST "$MILLIMETRIC_HOST/v1/batch" \
  -H "Authorization: Bearer $MILLIMETRIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      { "event": "purchase", "anonymous_id": "u_1", "user_id": "user_1", "properties": { "amount_cents": 4900 } },
      { "event": "purchase", "anonymous_id": "u_2", "user_id": "user_2", "properties": { "amount_cents": 1900 } }
    ]
  }'
```

Each event in the batch supports the same fields as `/v1/track`. Batch is rate-limited at 5/sec, burst 20.

### Forget (GDPR delete)

```bash
curl -X POST "$MILLIMETRIC_HOST/v1/forget" \
  -H "Authorization: Bearer $MILLIMETRIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "user_id": "user_42" }'
```

Requires an `sk_*` key — `pk_*` is rejected with `403 forget_requires_secret_key`.

## Field reference (track / batch event)

| Field | Required | Notes |
|-------|----------|-------|
| `event` | yes | 1–128 chars. System events start with `$` (`$pageview`, `$identify`). |
| `event_id` | no | Idempotency key, 1–128 chars. |
| `timestamp` | no | ISO 8601. Defaults to server time. |
| `anonymous_id` | no | Caller-supplied UUID. Server generates one if omitted. |
| `user_id` | no | Stable internal user id. |
| `session_id` | no | Defaults to `${anonymous_id}-${30min_bucket}`. |
| `url` | no | Landing URL with `utm_*`, `fbclid`, `gclid`. **Classifier reads this.** |
| `path` | no | Path only. |
| `referrer` | no | `document.referrer` or server `Referer`. **Classifier reads this.** |
| `properties` | no | Free-form JSON, capped at 8 KB after `JSON.stringify`. |

The Worker enriches every event with `source`, `medium`, `campaign`, `source_confidence`, `source_rule_id`, `country`, `device_type`, `browser`, `os`, `ip_hash`. Don't send these — they're ignored.

## Node SDK alternative

```bash
npm i @millimetric/track-node
```

```ts
import { init, track, identify, flush } from "@millimetric/track-node";

init({ key: process.env.MILLIMETRIC_KEY!, host: "https://api.millimetric.ai" });

track({
  event: "purchase",
  anonymous_id: req.cookies.aid,
  user_id: user.id,
  properties: { amount_cents: 4900, currency: "usd" }
});

await flush();   // important in serverless handlers
```

## Common errors

| Status | `error` | Fix |
|--------|---------|-----|
| 400 | `invalid_payload` | `event` missing or `properties` > 8 KB. |
| 401 | `malformed_api_key` | Key doesn't match `(pk\|sk\|rk)_*_*_*`. |
| 401 | `invalid_api_key` | Key not found in DB. |
| 403 | `origin_not_allowed` | Using `pk_*` from a non-allowlisted origin — switch to `sk_*` for server-side. |
| 403 | `forget_requires_secret_key` | `/v1/forget` called with `pk_*`. |
| 429 | `rate_limited` | Back off using the `Retry-After` header. Track: 50/s, burst 200. Batch: 5/s, burst 20. |

## Key hygiene

- `pk_live_…` → browser snippet only. Never paste into shell, server code, or this skill.
- `sk_live_…` → server-side ingest. Use here.
- `rk_live_…` → read-only — for the query skill, not this one.

## See also

- Query/analytics → `millimetric-query`
- AI agent / MCP setup → `millimetric-mcp-setup`
- Attribution rules: https://api.millimetric.ai (docs/concepts/attribution.md)
