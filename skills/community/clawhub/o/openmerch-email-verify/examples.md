# Examples

Natural things an OpenClaw user might ask, and what the skill does.

## Example asks

- "Verify whether `jane@acme.com` is a real, deliverable address."
- "Is `info@somecompany.io` a disposable or role-based email?"
- "Check the reputation of this email before I add it to my outreach list: `bob@startup.dev`."
- "Run an email deliverability check on `sales@example.com` using OpenMerch."

Each ask resolves to **one** OpenMerch job (`email_reputation_v1`) for the single address.

## Sample run

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
node verify-email.mjs jane@acme.com
```

## Sample output

The exact `raw` keys are owned by the upstream provider and may change; `summary` only includes
fields that were actually present. `raw` is the source of truth.

```json
{
  "email": "jane@acme.com",
  "summary": {
    "deliverable": true,
    "is_disposable": false,
    "is_free_email": false,
    "quality_score": 0.95
  },
  "raw": {
    "email_address": "jane@acme.com",
    "email_deliverability": {
      "status": "deliverable",
      "is_disposable_email": false,
      "is_free_email": false
    },
    "email_quality": { "score": 0.95 }
  },
  "cost_usd": 0.007,
  "job_id": "f1e2d3c4-0000-0000-0000-abcdef123456"
}
```

> Note: the values above are illustrative. The real price is whatever `/v1/plan` quotes for your
> account, and `cost_usd` reflects the actual `cost.total_microcents` OpenMerch charged.

## When it can't run

- If `/v1/plan` returns `can_execute: false`, the skill stops and reports why (e.g. no provider
  available, account/budget issue) — it does **not** execute or charge you.
- If the job ends `failed` or `cancelled`, the skill reports the `error.code` / `error.message`.
