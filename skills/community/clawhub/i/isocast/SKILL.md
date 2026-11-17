---
name: isocast
version: 1.1.0
description: >-
  Polymarket weather-signal API for AI agents. When a city's observed daily-high
  temperature crosses into a new Polymarket temperature bucket, Isocast fires one signal
  carrying the market URL, the old and new reading, and live odds for every bucket. 37
  cities, with optional Telegram push delivery. Free to browse — cities, sample signal,
  pricing, and terms need no auth; deeper per-city signal bundles are pay-per-call via x402.
homepage: https://isocast.dev
metadata:
  openclaw:
    emoji: "🌦️"
    requires:
      bins: ["node"]
---

# Isocast — Polymarket Weather-Signal API for AI Agents

API at `https://api.isocast.dev`. Isocast watches 37 cities and, when a city's observed
daily-high temperature crosses out of one Polymarket temperature bucket and into another,
emits exactly one signal for that (city, day, transition). Every signal carries the
Polymarket market URL, the old and new `{reading, unit, bucket}`, and live YES/NO/midpoint
odds for every bucket (with `dead: true` on buckets the day can no longer reach). Browsing is
free and needs no auth; deeper signals are per-city bundles bought pay-per-call.

Full API docs: [api.isocast.dev/llms.txt](https://api.isocast.dev/llms.txt) | OpenAPI spec: [api.isocast.dev/openapi.json](https://api.isocast.dev/openapi.json)

## What a signal is

A signal fires when a city's daily-high reading moves into a new Polymarket bucket. It
includes the market URL, the old/new bucket readings, and current odds for every bucket, plus
`bucketsAsOf` (odds freshness, ~10s) and `observedAt`. Delivery is at-most-once per (city,
day, bucket), and `seq` is a monotonic per-city counter so you can track what you've seen.

## Free endpoints (no auth, no payment)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness + configured payment mode (`live`\|`mock`) |
| GET | `/v1/cities` | All active cities (slug, unit, bucketWidth, timezone, latestSeq). 30s cache |
| GET | `/v1/cities/:slug` | One city + today's target date + Polymarket market URL |
| GET | `/v1/sample?city=SLUG` | A promo signal (fixed, never the latest) so you can see the shape before paying. `sample: true` |
| GET | `/v1/signals/meta?city=SLUG` | Pricing + bundle tiers for a city (never returns signal rows) |
| GET | `/terms.txt` · `/terms.json` | Terms of Service (also sets `X-Terms-URL`) |

Every JSON response also carries a `disclaimer` string.

## Quick Start — Browse a City (free)

```typescript
// All free, no auth, no setup
const BASE = "https://api.isocast.dev";

// 1. List active cities
const cities = await (await fetch(`${BASE}/v1/cities`)).json();
// cities: [{ slug, unit, bucketWidth, timezone, latestSeq }, ...]

// 2. Inspect today's market for one city
const city = await (await fetch(`${BASE}/v1/cities/istanbul`)).json();
// city: { slug, targetDate, marketUrl, ... }

// 3. See a sample signal shape before paying
const sample = await (await fetch(`${BASE}/v1/sample?city=istanbul`)).json();
// sample.signal: { marketUrl, old, new, buckets, observedAt, ... }, sample: true
```

## Paid signals

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | `/v1/spot?city=SLUG` | $0.01 | Snapshot of a city's LATEST signal — stock x402 (no binding nonce). Exactly one signal, never history. Uncharged on unknown-city / no-data. |
| POST | `/v1/subscribe?city=SLUG&count=N` | $0.01–$7.00 | Buy the next N signals for a city (bundle prepay, count ≥ 2; volume tiers). |
| GET | `/v1/signals?city=SLUG&since=S` | Bearer receipt or x402 | Read signals you're entitled to (402 on exhaustion). |

The cheapest read is `GET /v1/spot?city=SLUG` — a $0.01 snapshot of the city's latest signal,
payable by a STOCK x402 client (plain `@x402/fetch` `wrapFetchWithPayment`, no custom nonce).
For a running feed, buy a prepaid per-city bundle via `/v1/subscribe` (pay-per-call via x402;
the effective unit price drops with bundle size), then read `/v1/signals`. Agents can use the
`isocast-mcp` npm package (an MCP server) which handles payment for you, or read the full flow at
[api.isocast.dev/llms.txt](https://api.isocast.dev/llms.txt). Entitled signals can also be pushed
to a Telegram chat (free — the delivery registration route never charges).

## Error Handling

- **402** — Payment required for a paid signal route. See the docs above for the payment flow.
- **429** — Rate limited. Respect the `Retry-After` header (seconds to wait).
- **404** — Unknown or inactive city.

## Machine discovery

| Path | What |
|------|------|
| `/llms.txt` | This doc (concise) |
| `/openapi.json` | OpenAPI 3.1 spec |
| `/discovery` | Discovery JSON (free/paid endpoint listing) |

## Disclaimer

Informational data only — not financial or betting advice. No guarantee of accuracy or
outcome; prediction markets are restricted in some jurisdictions. Terms: https://isocast.dev/terms
