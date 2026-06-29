---
name: openmerch-people-enrichment
title: "OpenMerch People Enrichment"
description: >-
  Retrieve a full personal profile — full name, email address, LinkedIn URL,
  title, and employer — for a single person using their Apollo person ID.
  Powered by OpenMerch (paid API). Returns sensitive personal data. Install
  only if you have a lawful basis to process personal contact data and will
  handle results in compliance with applicable privacy law (GDPR, CCPA, etc.).
version: 1.0.0
emoji: "🔍"
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
          enrichment consumes your OpenMerch account balance/credits.
      - name: OPENMERCH_BASE_URL
        required: false
        description: >-
          OpenMerch API base URL. Defaults to https://api.openmerch.dev.
          Override only for staging/testing.
---

# People Enrichment (powered by OpenMerch)

Retrieve a full personal profile by Apollo person ID: full name, email address,
LinkedIn URL, title, and employer. Use the `id` returned by
`openmerch-people-search` as the lookup key.

## Companion skill

**Install `openmerch-people-search` alongside this skill** for the full
people-intelligence workflow. The two skills are designed to be used in tandem:

1. **Search** (`openmerch-people-search`) — find people at a company by domain and
   role keywords. Each result includes an `id` (Apollo person ID).
2. **Enrich** (this skill) — pass the `id` from step 1 to retrieve the full profile:
   email address, full name, LinkedIn URL, title, and employer.

If you already have an Apollo person ID from another source, you can run this skill
standalone. Otherwise, run `openmerch-people-search` first to get the ID.

The exact price is **confirmed by `/v1/plan` before anything runs**. The skill
never charges more than the planned `max_cost`. ClawHub does not handle billing
and takes no fee — the charge is between you and OpenMerch.

Get a key from the **Developer** page in the OpenMerch app:

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
# Optional — defaults to https://api.openmerch.dev:
# export OPENMERCH_BASE_URL="https://api.openmerch.dev"
```

## Privacy & Acceptable Use

This skill returns sensitive personal data: full name, email address, and
LinkedIn URL. Before running:

- Confirm you have a lawful basis to process this data (consent, legitimate
  interest, or another basis applicable in your jurisdiction).
- Store and share results only as required by your specific use case.
- Comply with GDPR, CCPA, and any other applicable privacy law.
- Do not use enriched data for unsolicited outreach, bulk profiling, or data
  brokering without authorization.

## What this calls

No hidden network behavior. This skill makes only these OpenMerch HTTP calls, in order:

1. `POST {OPENMERCH_BASE_URL}/v1/plan` — confirm the job is executable and get the price.
2. `POST {OPENMERCH_BASE_URL}/v1/execute` — run the enrichment (one job).
3. `GET  {OPENMERCH_BASE_URL}/v1/jobs/{job_id}` — **only if** the job is still `executing`, to poll
   until it finishes. Most runs return `completed` immediately and no polling is needed.

Every request sends the header `X-OpenMerch-Key: $OPENMERCH_API_KEY`.

## How to run

### Option A — reference script (deterministic)

Requires Node 18+ (no `npm install`):

```bash
node people-enrichment.mjs abc123
```

Prints a normalized JSON result to stdout and exits non-zero on error.

### Option B — agent-driven (instructions)

**1. Plan.** `POST /v1/plan`:

```json
{
  "job_type": "people_enrichment_v1",
  "input": {
    "operation": "people-enrichment",
    "params": {
      "id": "abc123"
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
    "operation": "people-enrichment",
    "params": {
      "id": "abc123"
    }
  },
  "max_cost": "<max_cost from step 1>",
  "idempotency_key": "<uuid>"
}
```

Reuse the same `idempotency_key` on retry for the same lookup to prevent double charges.
Generate a new key only for a genuinely new enrichment.

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
  -d '{"job_type":"people_enrichment_v1","input":{"operation":"people-enrichment","params":{"id":"abc123"}}}'
```

## Output

```json
{
  "id": "abc123",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "email_status": "verified",
  "title": "Senior Backend Engineer",
  "seniority": "senior",
  "linkedin_url": "https://www.linkedin.com/in/janedoe",
  "organization": "Stripe",
  "cost_usd": 0.008,
  "job_id": "…"
}
```

**Always present:** `job_id`.

**Present when available:** `cost_usd` (when the job returns cost data), plus all profile fields
(`id`, `first_name`, `last_name`, `email`, `email_status`, `title`, `seniority`, `linkedin_url`,
`organization`). Fields absent from the upstream response are omitted — never synthesized.

`cost_usd` is derived from `cost.total_microcents` (1 cent = 100,000 µ¢; $1.00 = 10,000,000).

## Notes

- One enrichment per run. Input is a single Apollo person ID.
- The skill executes a single atomic OpenMerch job — no multi-step orchestration.
- Apollo person IDs are returned by `openmerch-people-search` in the `id` field of each result.
