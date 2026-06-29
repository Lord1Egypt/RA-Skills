---
name: openmerch-company-brief
title: "OpenMerch Company Brief"
description: Look up a company's profile by domain — industry, size, location, founding year, and funding data when available. Powered by OpenMerch.
version: 1.0.0
emoji: "🏢"
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
          lookup consumes your OpenMerch account balance/credits.
      - name: OPENMERCH_BASE_URL
        required: false
        description: >-
          OpenMerch API base URL. Defaults to https://api.openmerch.dev.
          Override only for staging/testing.
---

# Company Brief (powered by OpenMerch)

Look up a company's profile by domain: industry, size, location, founding year,
technologies, and funding data when available.

**Use when the caller already knows the company domain.** For people discovery,
person enrichment, or contact lookup, use the separate `openmerch-people-search`
and `openmerch-contact-discovery` skills.

The exact price is **confirmed by `/v1/plan` before anything runs** — OpenMerch
routes may vary, so the script always uses the live quote rather than a fixed
amount. The skill never charges more than the planned `max_cost`. ClawHub does
not handle billing and takes no fee — the charge is between you and OpenMerch.

Get a key from the **Developer** page in the OpenMerch app:

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
# Optional — defaults to https://api.openmerch.dev:
# export OPENMERCH_BASE_URL="https://api.openmerch.dev"
```

## When to trigger

Trigger for questions about a known company domain involving:

- Company profile or firmographic overview
- Industry or business category
- Headcount or employee count
- Location, headquarters, or geography
- Founding year
- Technologies used
- Funding data (total raised, latest stage) — when available
- LinkedIn presence

**Not in scope — use other skills:**

- Competitive analysis or comparisons between companies
- Employee or people discovery → use `openmerch-people-search`
- Full person profile or enrichment → use `openmerch-people-search` with `people-enrichment` op
- Contact or email lookup → use `openmerch-contact-discovery`
- Email verification → use `openmerch-email-verify`
- Broad web research or news

## What this calls

No hidden network behavior. This skill makes only these OpenMerch HTTP calls, in order:

1. `POST {OPENMERCH_BASE_URL}/v1/plan` — confirm the job is executable and get the price.
2. `POST {OPENMERCH_BASE_URL}/v1/execute` — run the enrichment (one job).
3. `GET  {OPENMERCH_BASE_URL}/v1/jobs/{job_id}` — **only if** the job is still `executing`, to poll
   until it finishes. Most runs return `completed` immediately and no polling is needed.

Every request sends the header `X-OpenMerch-Key: $OPENMERCH_API_KEY`.

## How to run

### Option A — reference script (deterministic)

Requires Node 18+ (no `npm install`). Accepts a bare domain or any URL — protocol
and path are stripped automatically:

```bash
node company-brief.mjs stripe.com
node company-brief.mjs https://stripe.com/about
```

Prints a normalized JSON result to stdout and exits non-zero on error.

### Option B — agent-driven (instructions)

**1. Plan.** `POST /v1/plan`:

```json
{
  "job_type": "company_enrichment_v1",
  "input": {
    "company_domain": "stripe.com"
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
  "job_type": "company_enrichment_v1",
  "input": {
    "company_domain": "stripe.com"
  },
  "max_cost": "<max_cost from step 1>",
  "idempotency_key": "<uuid>"
}
```

Reuse the same `idempotency_key` on retry for the same lookup to prevent double charges.
Generate a new key only for a genuinely new lookup.

**3. Poll only if needed.** If `status` is `"executing"`, poll `GET /v1/jobs/{job_id}` every ~1s
(cap ~8 tries / ~15s) until `status` is `completed`, `failed`, or `cancelled`.

**4. Report.** On `completed`, present the normalized result (below). On `failed`/`cancelled`,
report `error.code` and `error.message`. Always report `job_id`; include `cost_usd` when present.

### curl equivalent

```bash
BASE="${OPENMERCH_BASE_URL:-https://api.openmerch.dev}"

curl -sS -X POST "$BASE/v1/plan" \
  -H "X-OpenMerch-Key: $OPENMERCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_type":"company_enrichment_v1","input":{"company_domain":"stripe.com"}}'
```

## Output

```json
{
  "domain": "stripe.com",
  "name": "Stripe",
  "description": "Financial infrastructure for the internet.",
  "industry": "financial services",
  "employee_count": 7000,
  "location": "San Francisco, California, United States",
  "founded_year": 2010,
  "annual_revenue": "$1B+",
  "linkedin_url": "https://www.linkedin.com/company/stripe",
  "technologies": ["React", "Ruby on Rails", "AWS"],
  "funding": {
    "total_usd": 8700000000,
    "latest_stage": "Series I"
  },
  "raw": { "...": "verbatim OpenMerch job output" },
  "cost_usd": 0.006,
  "job_id": "…"
}
```

**Always present:** `domain`, `raw`, `job_id`.

**Present when available:** `cost_usd` (when the job returns cost data), plus all other fields
(`name`, `description`, `industry`, `employee_count`, `location`, `founded_year`,
`annual_revenue`, `linkedin_url`, `technologies`, `funding`). Fields absent from the
upstream response are omitted — never synthesized.

`raw` is the full unmodified OpenMerch job output and is the source of truth. `cost_usd` is
derived from `cost.total_microcents` (1 cent = 100,000 µ¢; $1.00 = 10,000,000).

## Notes

- One lookup per run. Input is a single company domain.
- The skill executes a single atomic OpenMerch job — no multi-step orchestration.
- Domain normalization strips protocol and path: `https://stripe.com/about` → `stripe.com`.
- Funding data (`funding.total_usd`, `funding.latest_stage`) is included only when the
  upstream response contains it. Not all companies have funding data available.
