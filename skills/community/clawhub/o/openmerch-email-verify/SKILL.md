---
name: openmerch-email-verify
title: "OpenMerch Email Verify"
description: Verify an email address's deliverability and reputation. Powered by OpenMerch.
version: 1.0.3
emoji: "✉️"
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
          verification consumes your OpenMerch account balance/credits.
      - name: OPENMERCH_BASE_URL
        required: false
        description: >-
          OpenMerch API base URL. Defaults to https://api.openmerch.dev.
          Override only for staging/testing.
---

> [!WARNING]
> **This skill is temporarily unavailable.** The underlying email reputation
> provider is experiencing an outage. `/v1/plan` will return "no viable candidates"
> until the provider is restored and the service is re-enabled. Do not use until
> this notice is removed.

# Email verify (powered by OpenMerch)

Verify whether an email address is deliverable, and surface basic reputation signals
(disposable / free-provider / role address, a quality score), for a single address.

This skill uses OpenMerch to plan, route, and execute the check. You give it one email address; it
returns a normalized result plus the raw provider output.

## Requirements & cost

This skill uses OpenMerch to plan, route, and execute the email check. **OpenMerch is an external
paid API**: you need an OpenMerch account and an API key, and **each verification consumes your
OpenMerch account balance/credits**. The exact price is **confirmed by the `/v1/plan` call before
anything runs** — that quote is the source of truth for what you pay (currently roughly
**$0.006–$0.007** per email, depending on OpenMerch pricing policy). The skill never charges more
than the planned `max_cost`. ClawHub does not handle this billing and takes no fee — the charge is
between you and OpenMerch.

Get a key from the **Developer** page in the OpenMerch app and set it as an environment variable:

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
# Optional — defaults to https://api.openmerch.dev:
# export OPENMERCH_BASE_URL="https://api.openmerch.dev"
```

## What this calls

No hidden network behavior. This skill makes only these OpenMerch HTTP calls, in order:

1. `POST {OPENMERCH_BASE_URL}/v1/plan` — confirm the job is executable and get the price.
2. `POST {OPENMERCH_BASE_URL}/v1/execute` — run the verification (one job).
3. `GET  {OPENMERCH_BASE_URL}/v1/jobs/{job_id}` — **only if** the job is still `executing`, to poll
   until it finishes.

Every request sends the header `X-OpenMerch-Key: $OPENMERCH_API_KEY`. POST bodies send
`Content-Type: application/json`. Base URL is `OPENMERCH_BASE_URL` or `https://api.openmerch.dev`.

## How to run

You can run this two ways. **Both do exactly the same calls.**

### Option A — reference script (deterministic)

Requires Node 18+ (uses built-in `fetch`; no `npm install`):

```bash
node verify-email.mjs jane@acme.com
```

It prints a JSON result to stdout (see "Output" below) and exits non-zero on error.

### Option B — agent-driven (instructions)

If you (the agent) are running the flow with your own HTTP tools, follow these steps exactly:

**1. Plan.** `POST /v1/plan`:

```json
{ "job_type": "email_reputation_v1", "input": { "email": "<EMAIL>" } }
```

- If the response `can_execute` is not `true`, **stop** and report the reason. Do not execute.
- Set `max_cost = quoted_customer_price_microcents` if present, otherwise
  `estimated_cost.max_microcents`. `/v1/plan` is the source of truth for the price — never hardcode
  one.

**2. Execute.** Generate one UUID v4 as `idempotency_key` for this submission. `POST /v1/execute`:

```json
{
  "job_type": "email_reputation_v1",
  "input": { "email": "<EMAIL>" },
  "max_cost": <max_cost from step 1>,
  "idempotency_key": "<uuid>"
}
```

- **Reuse the same `idempotency_key`** if you retry this same submission (e.g. after a timeout).
  Generate a **new** key only for a genuinely new verification. This prevents double charges.

**3. Poll only if needed.** If the execute response `status` is `"executing"`, poll
`GET /v1/jobs/{job_id}` every ~1s (cap ~8 tries / ~15s) until `status` is `completed`, `failed`, or
`cancelled`. Most runs return `completed` immediately and no polling is needed.

**4. Report.** On `completed`, present the normalized result (below). On `failed`/`cancelled`,
report `error.code` and `error.message`. Always report `cost.total_microcents` (the actual amount
charged) and the `job_id`.

### curl equivalent

```bash
BASE="${OPENMERCH_BASE_URL:-https://api.openmerch.dev}"

# 1. Plan
curl -sS -X POST "$BASE/v1/plan" \
  -H "X-OpenMerch-Key: $OPENMERCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_type":"email_reputation_v1","input":{"email":"jane@acme.com"}}'

# 2. Execute
# Replace <MAX_COST_FROM_PLAN> with quoted_customer_price_microcents from /v1/plan,
# or estimated_cost.max_microcents if no quote was returned. Do not hardcode a price.
curl -sS -X POST "$BASE/v1/execute" \
  -H "X-OpenMerch-Key: $OPENMERCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_type":"email_reputation_v1","input":{"email":"jane@acme.com"},"max_cost":<MAX_COST_FROM_PLAN>,"idempotency_key":"'"$(uuidgen)"'"}'

# 3. Poll only if status was "executing"
# curl -sS "$BASE/v1/jobs/<job_id>" -H "X-OpenMerch-Key: $OPENMERCH_API_KEY"
```

## Output

The skill returns a normalized object. The `summary` fields are **best-effort** and appear only when
the underlying provider response contains them; `raw` is always the full, unmodified OpenMerch job
output and is the source of truth. `cost_usd` is derived from the actual charged
`cost.total_microcents`.

```json
{
  "email": "jane@acme.com",
  "summary": {
    "deliverable": true,
    "is_disposable": false,
    "is_free_email": false,
    "quality_score": 0.95
  },
  "raw": { "...": "verbatim OpenMerch job output" },
  "cost_usd": 0.007,
  "job_id": "…"
}
```

## Notes & limits

- One email per run. For a list, call the skill once per address.
- The skill executes a single atomic OpenMerch job — no multi-step orchestration.
- All monetary values from OpenMerch are in **microcents** (1 cent = 100,000 microcents;
  $1.00 = 10,000,000). `cost_usd` is `cost.total_microcents / 10000000`.
