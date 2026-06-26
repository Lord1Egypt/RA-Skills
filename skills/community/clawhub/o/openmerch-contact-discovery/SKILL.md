---
name: openmerch-contact-discovery
title: "OpenMerch Contact Discovery"
description: Find a professional's work email from their name and company domain. Powered by OpenMerch. Not email verification.
version: 1.0.2
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
          lookup consumes your OpenMerch account balance/credits.
      - name: OPENMERCH_BASE_URL
        required: false
        description: >-
          OpenMerch API base URL. Defaults to https://api.openmerch.dev.
          Override only for staging/testing.
---

# Contact discovery — email finder (powered by OpenMerch)

Find a professional's work email address given their first name, last name, and
company domain. **This skill is for contact lookup — not email verification or
deliverability checking.** It returns a found email address with a confidence
score, plus available profile fields (title, LinkedIn URL) when the provider
has them.

The exact price is **confirmed by `/v1/plan` before anything runs** — currently
roughly **$0.008–$0.013** per lookup depending on the routed provider. The skill
never charges more than the planned `max_cost`. ClawHub does not handle billing
and takes no fee — the charge is between you and OpenMerch.

Get a key from the **Developer** page in the OpenMerch app:

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
# Optional — defaults to https://api.openmerch.dev:
# export OPENMERCH_BASE_URL="https://api.openmerch.dev"
```

## What this calls

No hidden network behavior. This skill makes only these OpenMerch HTTP calls, in order:

1. `POST {OPENMERCH_BASE_URL}/v1/plan` — confirm the job is executable and get the price.
2. `POST {OPENMERCH_BASE_URL}/v1/execute` — run the lookup (one job).
3. `GET  {OPENMERCH_BASE_URL}/v1/jobs/{job_id}` — **only if** the job is still `executing`, to poll
   until it finishes. Most runs return `completed` immediately and no polling is needed.

Every request sends the header `X-OpenMerch-Key: $OPENMERCH_API_KEY`.

## How to run

### Option A — reference script (deterministic)

Requires Node 18+ (no `npm install`):

```bash
node find-email.mjs Jane Doe acme.com
```

Prints a normalized JSON result to stdout and exits non-zero on error.

### Option B — agent-driven (instructions)

**1. Plan.** `POST /v1/plan`:

```json
{
  "job_type": "contact_discovery_v1",
  "input": {
    "operation": "email-finder",
    "params": {
      "first_name": "Jane",
      "last_name": "Doe",
      "domain": "acme.com"
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
  "job_type": "contact_discovery_v1",
  "input": {
    "operation": "email-finder",
    "params": {
      "first_name": "Jane",
      "last_name": "Doe",
      "domain": "acme.com"
    }
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
report `error.code` and `error.message`. Always report `cost_usd` and `job_id`.

### curl equivalent

```bash
BASE="${OPENMERCH_BASE_URL:-https://api.openmerch.dev}"

curl -sS -X POST "$BASE/v1/plan" \
  -H "X-OpenMerch-Key: $OPENMERCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_type":"contact_discovery_v1","input":{"operation":"email-finder","params":{"first_name":"Jane","last_name":"Doe","domain":"acme.com"}}}'
```

## Output

```json
{
  "email": "jane@acme.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "domain": "acme.com",
  "position": "Head of Sales",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "score": 90,
  "raw": { "...": "verbatim OpenMerch job output" },
  "cost_usd": 0.013,
  "job_id": "…"
}
```

`position` and `linkedin_url` appear only when the provider returns them. `score` is a
0–100 confidence value; 90+ indicates high confidence. `raw` is the full unmodified
OpenMerch job output and is the source of truth. `cost_usd` is derived from the actual
`cost.total_microcents` charged.

## Notes & limits

- One lookup per run. Input requires first name, last name, and company domain.
- This skill is for finding an email address — it does not verify deliverability.
- The skill executes a single atomic OpenMerch job — no multi-step orchestration.
- All monetary values from OpenMerch are in microcents (1 cent = 100,000 µ¢;
  $1.00 = 10,000,000). `cost_usd` is `cost.total_microcents / 10000000`.
