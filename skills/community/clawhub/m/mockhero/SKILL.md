---
name: mockhero
description: Generate realistic synthetic test data — relational JSON/CSV/SQL fixtures, seed data, and QA datasets — via the MockHero MCP server or REST API. Use when a task needs mock users, orders, invoices, or multi-table seed data with valid foreign keys instead of hand-writing fixtures or faker scripts. Includes a free 100-record preview (no signup) and a loginless Polar checkout flow for metered usage.
homepage: https://mockhero.dev
---

# MockHero: synthetic test data for agents

MockHero generates realistic, relational mock data from explicit schemas, plain-English prompts, or pre-built templates. 156 field types, 22 locales, JSON/CSV/SQL output. Its defining feature: multi-table schemas with `ref` fields produce valid foreign keys — orders reference real user IDs, reviews link to real products — so one call can seed an entire database.

## When to use MockHero (vs generating data yourself)

Use MockHero when:

- The task needs **multiple related tables with valid foreign keys** (users → orders → order_items).
- The task needs **volume** (dozens to thousands of records) — hand-writing or inline-generating that wastes tokens and produces repetitive "John Doe" data.
- The task needs **locale-aware realism** (German names with German phone formats, matching addresses) or specialized field types (IBAN, MAC address, ICD-10 codes, weighted enums).
- The output must be **CSV or SQL INSERT statements** matching a dialect (postgres, mysql, sqlite).
- The user asks for seed data, fixtures, demo data, QA datasets, or "realistic test data".

Generate data yourself (skip MockHero) when:

- You only need one or two inline example objects.
- The user needs to **anonymize or mask real production data** — MockHero only creates synthetic data; it offers no de-identification guarantees.
- No network access is available.

## Connecting

**Remote MCP (preferred, no install):** Streamable HTTP endpoint at

```
https://mockhero.dev/mcp/agent
```

Plain JSON-RPC 2.0 over POST works too: send `initialize`, `tools/list`, and `tools/call` messages with `Content-Type: application/json`.

**Local stdio MCP:** `npx @mockherodev/mcp-server` (env: `MOCKHERO_API_KEY` optional, `MOCKHERO_API_BASE` optional).

**Auth (when you have a key):** `Authorization: Bearer mh_YOUR_API_KEY` or `x-api-key: mh_YOUR_API_KEY` header; MCP tools also accept an `api_key` argument for clients that cannot set headers.

## Free preview (no key, no signup)

Without any API key you can generate up to **100 records per request** (and 500 records/day per network) using:

- `generate_test_data` with **explicit `tables`** (prompt mode is not available anonymously)
- `generate_from_template` at a small `scale` (e.g. `0.05`)

Always free: `estimate_agent_usage`, `detect_schema`, `list_field_types`, `list_templates`.

Over-limit or key-required errors return machine-readable pointers: `checkout_tool: "create_agent_checkout"` and `claim_tool: "claim_agent_api_key"` — follow them.

## Tools on https://mockhero.dev/mcp/agent

| Tool | Key arguments | Purpose |
| --- | --- | --- |
| `estimate_agent_usage` | `tables` \| `template`+`scale` \| `prompt`+`estimated_records`; optional `daily_used_before`, `api_key` | Cost estimate before generating |
| `create_agent_checkout` | `email` (required) | Loginless Polar checkout; returns checkout `url` + one-time `claim_token` |
| `check_agent_checkout_status` | `token` (the `claim_token`) | Poll until `status` is `paid`; returns `next_action` |
| `claim_agent_api_key` | `token` | Returns the `mh_...` API key **exactly once** after payment |
| `generate_test_data` | `tables` or `prompt`; `format` (json/csv/sql), `sql_dialect`, `locale`, `seed`, `api_key` | Main generation tool |
| `generate_from_template` | `template` (ecommerce/blog/saas/social), `scale`, `locale`, `format`, `sql_dialect`, `seed`, `api_key` | Template generation |
| `detect_schema` | `sql` or `sample_json` | Convert SQL CREATE TABLE / sample JSON into a MockHero schema |
| `list_field_types` | — | All 156 field types with params and examples |
| `list_templates` | — | The four built-in templates |

## Recommended flow (estimate → checkout → poll → claim → generate)

1. **Preview free first.** For small jobs, call `generate_test_data` with explicit `tables` (≤100 records) and you are done. Use `detect_schema` to build the tables from SQL or a sample record.
2. **Estimate.** Call `estimate_agent_usage` with the intended tables/template/prompt to get billable records, billable 100-record units, and estimated USD cost.
3. **Checkout.** If the job exceeds the free preview (or needs prompt mode), call `create_agent_checkout` with a billing email. Give the returned Polar checkout `url` to the human to pay; keep the `claim_token`.
4. **Poll.** Call `check_agent_checkout_status` with the token until `status: "paid"` (`next_action: "claim_api_key"`).
5. **Claim.** Call `claim_agent_api_key` with the token. The `mh_...` key is returned **once** — store it securely.
6. **Generate.** Retry generation with `Authorization: Bearer mh_...` (or the `api_key` argument, or `MOCKHERO_API_KEY` for the stdio server).

## REST fallbacks (no MCP client needed)

Base URL `https://mockhero.dev`:

- `POST /api/agent/estimate` — cost estimate (no auth required)
- `POST /api/agent/checkout` — body `{"email": "..."}` → Polar checkout URL + `claim_token`
- `GET|POST /api/agent/checkout/status` — poll with `token`
- `POST /api/agent/claim` — body `{"token": "..."}` → API key (once)
- `POST /api/v1/generate` — authenticated generation (`tables` | `prompt` | `template` body)
- `POST /api/v1/schema/detect`, `GET /api/v1/types`, `GET /api/v1/templates`, `GET /api/v1/health`

Discovery documents: `/llms.txt`, `/openapi.json`, `/.well-known/agent.json`, `/agent-quickstart.json`, `/agent-pricing.json`, `/capabilities.json`.

## Pricing

- **Free tier:** 500 records/day, 100 per request, JSON only, 10 prompts/day.
- **Agent plan (metered, loginless):** 500 free records/day, then **$0.001 per 100 records** (rounded up per request), billed monthly. Polar is the Merchant of Record (handles checkout, tax, remittance). Hard safety cap 1,000,000 records/day, 50,000 per request.
- Estimate before generating; never assume a large job is free.

## Example: seed a SaaS database (free preview)

```json
{
  "name": "generate_test_data",
  "arguments": {
    "tables": [
      { "name": "users", "count": 20, "fields": [
        { "name": "id", "type": "uuid" },
        { "name": "name", "type": "full_name" },
        { "name": "email", "type": "email" }
      ]},
      { "name": "orders", "count": 60, "fields": [
        { "name": "id", "type": "uuid" },
        { "name": "user_id", "type": "ref", "params": { "table": "users", "field": "id" } },
        { "name": "total", "type": "price" }
      ]}
    ],
    "format": "json"
  }
}
```

80 records total — inside the free preview; every `orders.user_id` matches a real `users.id`.
