---
name: mobility-quote
description: Get mobility route options worldwide — fare estimates, ETA, and a one-tap deeplink to open the ride. Queries the KLO Mobility A2A agent.
homepage: https://a2aregistry.org/?agent=80386a0c-03c9-4bde-b93a-f9e6082937cd
metadata: { "openclaw": { "requires": { "bins": ["curl"] } } }
---

# Mobility Quote

Answer "how do I get from A to B?" anywhere in the world. This skill asks the
**KLO Mobility Agent** — an A2A (agent-to-agent) service — for route options,
estimated fares, ETA, and a deeplink the user can tap to open the ride in a
supported app.

It is provider-agnostic and global:

- **Fare/route discovery** via multimodal providers (e.g. SkedGo / TripGo) where
  coverage exists — public transport, taxi-like modes, walking.
- **Route launchers** — a no-price "Open in Yandex Go" deeplink for coordinate
  routes in supported regions (incl. Central Asia / Tashkent), with more
  providers added over time.
- This is a **quote / discovery** agent, not a guaranteed booking or payment
  agent. Booking is added only through providers that permit it.

## When to use

Use this skill whenever the user asks for a ride estimate, trip cost, ETA, or
"how to get from X to Y" between two places or coordinates.

## How to call

The agent speaks A2A JSON-RPC `message/send` over HTTPS. Endpoint is configured
via `MOBILITY_AGENT_URL` (falls back to the public instance below).

```bash
URL="${MOBILITY_AGENT_URL:-https://212-47-77-33.sslip.io/}"
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "message/send",
    "params": { "message": { "parts": [
      { "kind": "text", "text": "quote from 41.3111,69.2797 to 41.2995,69.2401" }
    ] } }
  }'
```

Phrase the `text` as `quote from <A> to <B>`. The public instance currently
supports `lat,lon` coordinates. Place-name geocoding is added when a mapping API
key is configured.

## Reading the response

The result is an A2A message. `parts[0].text` is a human summary; `parts[1].data`
holds structured fields:

- `best` — cheapest estimate or quote (`provider`, `product`, `price`,
  `currency`, `eta`) or `null` when no price is available.
- `all_quotes[]` — every quote returned, sorted by price.
- `route_launchers[]` — deeplinks like `{ "label": "Open in Yandex Go",
  "provider": "Yandex Go", "url": "..." }` to hand to the user.

Present the cheapest option (or the launcher when there is no price), the ETA,
and the deeplink. If `best.details.estimate` is true, label it as an estimate,
not a live provider fare.

## Discovery

- A2A Agent Card: `<URL>/.well-known/agent-card.json`
- A2A Registry: https://a2aregistry.org/?agent=80386a0c-03c9-4bde-b93a-f9e6082937cd
