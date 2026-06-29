# Nexez Endpoint Contract

Use this reference before constructing Nexez API requests or interpreting Nexez responses.

## Base URL

Use `NEXEZ_BASE_URL` when configured. Otherwise use:

```text
https://nexez.app
```

## Public Discovery

These endpoints do not require an API key.

```text
GET /.well-known/nexez.json
GET /llms.txt
GET /openapi.json
GET /agent-pages.json
GET /.well-known/mcp.json
GET /api/agent-search?q={buyer_request}&location={city_or_region}&limit={count}
GET /api/directory?q={query}&location={city_or_region}&category={all|professional|consumer}&min_readiness={score}
GET /{slug}/agent.json
GET /{slug}/llms.txt
GET /{slug}/mcp.json
POST /api/checkout
POST /api/negotiations
```

## Native OpenClaw Tools

If the `nexez` OpenClaw plugin is installed, prefer these typed tools over raw HTTP:

- `nexez_search`: intent search by query, location, and limit.
- `nexez_get_page`: fetch one page's structured `agent.json` manifest.
- `nexez_directory`: browse directory results by query, location, category, and readiness.
- `nexez_validate_checkout`: dry-run checkout.
- `nexez_validate_negotiation`: dry-run negotiation.
- `nexez_start_checkout`: create a real checkout handoff. Requires explicit user approval and `userApproved: true`.
- `nexez_submit_negotiation`: submit a real seller-facing negotiation. Requires explicit user approval and `userApproved: true`.

## Recommended Request Order

1. Fetch `/.well-known/nexez.json` when you need current capability URLs.
2. Call `/api/agent-search` for buyer intent matching.
3. Call `/api/directory` for broad marketplace browsing, filters, or readiness thresholds.
4. Fetch `/{slug}/agent.json` before recommending checkout, booking, negotiation, or contact.
5. Use `/openapi.json` when generating a tool/action schema.

## Agent Search

```http
GET https://nexez.app/api/agent-search?q=strategy%20consultant&location=Chicago%2C%20IL&limit=10
```

Expected schema marker:

```text
nexez.agent-search.v1
```

Useful fields:

- `results[].score`
- `results[].page.name`
- `results[].page.slug`
- `results[].page.url`
- `results[].page.agent_json_url`
- `results[].offer.name`
- `results[].offer.price`
- `results[].offer.currency`
- `results[].offer.checkout_url`
- `results[].offer.action`
- `results[].location_match`
- `location_filter`

## Directory

```http
GET https://nexez.app/api/directory?q=consulting&location=Austin%2C%20TX&category=professional&min_readiness=70
```

Expected schema marker:

```text
nexez.directory.v2
```

Use directory results to browse many pages, inspect readiness/trust signals, or find pages by location/category before fetching specific manifests.

## Page Manifest

```http
GET https://nexez.app/{slug}/agent.json
```

Trust this over the HTML page. It is the source of truth for:

- seller identity
- offer names and descriptions
- prices and currency
- service area and location context
- FAQs
- checkout handoff data
- negotiation availability
- plain-text context for LLMs

## Checkout Dry Run

Use this before a real checkout when possible.

```http
POST https://nexez.app/api/checkout
Content-Type: application/json
```

```json
{
  "slug": "example-page",
  "offer": "services-0",
  "query": "Book a 60 minute strategy session next week.",
  "buyerAgent": "openclaw",
  "dryRun": true
}
```

## Checkout Handoff

Use only after explicit user approval.

```json
{
  "slug": "example-page",
  "offer": "services-0",
  "query": "Book a 60 minute strategy session next week.",
  "buyerEmail": "buyer@example.com",
  "buyerName": "Buyer Name",
  "buyerReference": "optional-buyer-order-id",
  "buyerAgent": "openclaw",
  "dryRun": false
}
```

If the response includes a checkout/action URL, return it to the user and explain the next step.

## Negotiation Dry Run

Use for scoped, custom, or negotiable offers before submitting anything real.

```http
POST https://nexez.app/api/negotiations
Content-Type: application/json
```

```json
{
  "slug": "example-page",
  "offer": "services-0",
  "buyerAgent": "openclaw",
  "query": "Need a consulting package for a launch in August.",
  "budget": "$2,500",
  "timeline": "Start within 2 weeks",
  "contact": "buyer@example.com",
  "requestedTerms": {
    "scope": "3 planning calls, written launch checklist, async follow-up"
  },
  "dryRun": true
}
```

## Negotiation Handoff

Use only after explicit user approval. Keep the requested terms concrete and avoid promising seller acceptance.

```json
{
  "slug": "example-page",
  "offer": "services-0",
  "buyerAgent": "openclaw",
  "query": "Need a consulting package for a launch in August.",
  "budget": "$2,500",
  "timeline": "Start within 2 weeks",
  "contact": "buyer@example.com",
  "requestedTerms": {
    "scope": "3 planning calls, written launch checklist, async follow-up",
    "approvalRequired": true
  },
  "dryRun": false
}
```

## Error Handling

- `404`: page or offer was not found. Re-search or ask the user to choose another result.
- `409`: checkout is not configured. Offer a website handoff or negotiation if available.
- `412`: negotiation storage is unavailable. Do not retry repeatedly; report that negotiation is temporarily unavailable.
- `429`: rate limited. Wait or ask the user to narrow the query.
- `5xx`: Nexez is temporarily unavailable. Do not claim no providers exist.
