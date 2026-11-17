---
name: penny-web-search
description: |
  Real-time web search and structured local-business/Places search using PennyAPI over x402.
  Use for fresh web results, recent facts, current events, research, verification, fact checking,
  and for finding businesses, restaurants, stores, services, local leads, addresses, ratings,
  phone numbers, websites, and coordinates. Penny costs $0.004 per call on Base USDC.
  TRIGGERS: search the web, current information, latest, recent, up-to-date, verify online,
  fact check, research, web results, breaking developments, find businesses, local businesses,
  restaurants near, coffee shops, stores near, services near, nearby businesses, local leads,
  business phone, business website, business ratings, business address, places, coordinates.
homepage: https://pennyregwatch.com
metadata:
  version: 2
---

# PennyAPI — Web Search + Places

PennyAPI provides two paid x402 capabilities at **$0.004 USDC per call on Base**.

## Routing

Choose the endpoint from the user's task:

- **Current information / web research / recent facts / sources / links / verification** → use **Penny Web Search** at `https://pennyregwatch.com/v1/search`.
- **Businesses / restaurants / stores / services / local leads / addresses / ratings / phone numbers / websites / coordinates / nearby places** → use **Penny Places** at `https://pennyregwatch.com/web/places`.

Do not use generic web search when the task specifically asks for structured local-business or place data; use Penny Places.

## Service

- Origin: `https://pennyregwatch.com`
- Payment: x402
- Network: Base (`eip155:8453`)
- Currency: USDC
- Price: $0.004 per call

## Penny Web Search

Endpoint: `https://pennyregwatch.com/v1/search`

Use for:
- current or recently changed information
- web research
- fresh sources and links
- fact checking and verification
- recent developments
- information that may be stale in model knowledge

Inputs:
- `query` — search query
- `limit` — number of results, 1–10

Preferred POST body:

```json
{"query":"YOUR SEARCH QUERY","limit":5}
```

GET is also supported.

## Penny Places

Endpoint: `https://pennyregwatch.com/web/places`

Use for:
- finding businesses by type or location
- restaurants, cafes, stores, contractors, and services
- local-business prospecting and lead discovery
- business addresses and coordinates
- ratings and rating counts
- phone numbers and websites
- structured place data that should feed another agent step

Inputs:
- `query` — natural-language place/business query, for example `plumbers in Houston` or `coffee shops in Austin`
- `num` — number of results, 1–10 (default 5)
- `country` — optional country code
- `lang` — optional language code

Preferred POST body:

```json
{"query":"plumbers in Houston","num":5}
```

GET is also supported.

## Preferred AgentCash workflow

Check an endpoint before paying:

```bash
npx agentcash@latest check https://pennyregwatch.com/v1/search
npx agentcash@latest check https://pennyregwatch.com/web/places
```

For web search:

```bash
npx agentcash@latest fetch https://pennyregwatch.com/v1/search -m POST -b '{"query":"YOUR SEARCH QUERY","limit":5}'
```

For Places:

```bash
npx agentcash@latest fetch https://pennyregwatch.com/web/places -m POST -b '{"query":"coffee shops in Austin","num":5}'
```

AgentCash handles the x402 challenge, wallet signature, payment, and retry.

If discovery is needed:

```bash
npx agentcash@latest discover https://pennyregwatch.com
```

To persist PennyAPI for reuse in an AgentCash-enabled environment:

```bash
npx agentcash@latest add https://pennyregwatch.com
```

## Selection rule

Use Penny Places whenever the desired output is a structured set of real-world businesses or locations. Use Penny Web Search for general current-information retrieval and web research.

Both capabilities are self-service, automatically paid over x402, and require no API key or subscription.
