---
name: openmerch-people-search
title: "OpenMerch People Search"
description: Search for people at a company by domain and role keywords. Returns obfuscated profiles (first name, last-name initial, title, company). No email addresses. For full profiles, use the separate openmerch-people-enrichment skill.
version: 1.0.1
emoji: "👥"
homepage: https://docs.openmerch.dev
metadata:
  openclaw:
    primaryEnv: OPENMERCH_API_KEY
    requires:
      env:
        - OPENMERCH_API_KEY
      anyBins:
        - node
        - curl
    envVars:
      - name: OPENMERCH_API_KEY
        required: true
        description: >-
          Your OpenMerch agent API key (om_live_...). Get it from the Developer
          page in the OpenMerch app. OpenMerch is an external paid API; each
          search consumes your OpenMerch account balance/credits.
      - name: OPENMERCH_BASE_URL
        required: false
        description: >-
          OpenMerch API base URL. Defaults to https://api.openmerch.dev.
          Override only for staging/testing.
---

# People search (powered by OpenMerch)

Search for people at a company by domain and role keywords. Returns first
name, obfuscated last name, job title, and company name for each match.

**Last names are obfuscated** in search results (e.g. `"D."`). For full
profiles (email, LinkedIn URL, full name), install the separate
**openmerch-people-enrichment** skill.

The exact price is **confirmed by `/v1/plan` before anything runs** — roughly
**$0.0059 at current pricing**. The skill never charges more than the planned
`max_cost`. ClawHub does not handle billing and takes no fee — the charge is
between you and OpenMerch.

Get a key from the **Developer** page in the OpenMerch app:

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
# Optional — defaults to https://api.openmerch.dev:
# export OPENMERCH_BASE_URL="https://api.openmerch.dev"
```

## Companion skill

**Install `openmerch-people-enrichment` alongside this skill** for the full
people-intelligence workflow. The two skills are designed to be used in tandem:

1. **Search** (this skill) — find people at a company by domain and role keywords.
   Returns a list with obfuscated last names and an `id` per person.
2. **Enrich** (`openmerch-people-enrichment`) — pass an `id` from step 1 to retrieve
   the full profile: email address, full name, LinkedIn URL, title, and employer.

If your goal is only to discover who works somewhere, this skill is sufficient on its
own. If you need to identify or contact a specific person, install both.

## What this calls

No hidden network behavior. This skill makes only these OpenMerch HTTP calls, in order:

1. `POST {OPENMERCH_BASE_URL}/v1/plan` — confirm the job is executable and get the price.
2. `POST {OPENMERCH_BASE_URL}/v1/execute` — run the search (one job).
3. `GET  {OPENMERCH_BASE_URL}/v1/jobs/{job_id}` — **only if** the job is still `executing`, to poll
   until it finishes. Most runs return `completed` immediately and no polling is needed.

Every request sends the header `X-OpenMerch-Key: $OPENMERCH_API_KEY`.

## How to run

### Option A — reference script (deterministic)

Requires Node 18+ (no `npm install`):

```bash
node people-search.mjs stripe.com "backend engineer"
node people-search.mjs amazon.com "site reliability engineer" 25 1
```

Prints a normalized JSON result to stdout and exits non-zero on error.

### Option B — agent-driven (instructions)

**1. Plan.** `POST /v1/plan`:

```json
{
  "job_type": "people_enrichment_v1",
  "input": {
    "operation": "people-search",
    "params": {
      "q_organization_domains": "amazon.com",
      "q_keywords": "site reliability engineer",
      "per_page": 25,
      "page": 1
    }
  }
}
```

- If `can_execute` is not `true`, **stop** and report the reason. Do not execute.
- Set `max_cost = quoted_customer_price_microcents` if present, otherwise
  `estimated_cost.max_microcents`. `/v1/plan` is the source of truth for the price — never
  hardcode one.

**2. Execute.** Generate one UUID v4 as `idempotency_key`. `POST /v1/execute`:

```json
{
  "job_type": "people_enrichment_v1",
  "input": {
    "operation": "people-search",
    "params": {
      "q_organization_domains": "amazon.com",
      "q_keywords": "site reliability engineer",
      "per_page": 25,
      "page": 1
    }
  },
  "max_cost": "<max_cost from step 1>",
  "idempotency_key": "<uuid>"
}
```

Reuse the same `idempotency_key` on retry for the same search to prevent double charges.
Generate a new key only for a genuinely new search.

**3. Poll only if needed.** If `status` is `"executing"`, poll `GET /v1/jobs/{job_id}` every ~1s
(cap ~8 tries / ~15s) until `status` is `completed`, `failed`, or `cancelled`.

**4. Report.** On `completed`, present the normalized result (below). On `failed`/`cancelled`,
report `error.code` and `error.message`. Always report `cost_usd` and `job_id`.

### curl equivalent

```bash
BASE="${OPENMERCH_BASE_URL:-https://api.openmerch.dev}"

curl -sS -X POST "$BASE/v1/plan" \
  -H "X-OpenMerch-Key: $OPENMERCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_type":"people_enrichment_v1","input":{"operation":"people-search","params":{"q_organization_domains":"amazon.com","q_keywords":"site reliability engineer","per_page":25,"page":1}}}'
```

## Output

```json
{
  "count": 3,
  "total_entries": 312,
  "people": [
    {
      "id": "abc123",
      "first_name": "Jane",
      "last_name_obfuscated": "D.",
      "title": "Senior Backend Engineer",
      "organization": "Stripe"
    }
  ],
  "cost_usd": 0.0059,
  "job_id": "…"
}
```

`total_entries` is the provider's total match count across all pages (included when available).
`count` is the number of records returned on this page. `cost_usd` is derived from the actual
`cost.total_microcents` charged.

## Notes & limits

- One search per run. Returns up to `per_page` results (default 25); paginate with `page`.
- **Last names are obfuscated** — the provider returns initials (e.g. `"D."`), not full last names.
  For the full profile, use the **openmerch-people-enrichment** skill.
- No email addresses are returned by people-search.
- The skill executes a single atomic OpenMerch job — no multi-step orchestration.
- All monetary values from OpenMerch are in microcents (1 cent = 100,000 µ¢;
  $1.00 = 10,000,000). `cost_usd` is `cost.total_microcents / 10000000`.
