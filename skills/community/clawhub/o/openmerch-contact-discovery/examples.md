# Examples

Natural things an OpenClaw user might ask, and what the skill does.

## Example asks

- "Find Jane Doe's work email at acme.com."
- "What is the email address for John Smith at rippling.com?"
- "Look up the contact email for Sarah Chen at stripe.com."
- "Find the work email for Conrad Parker at rippling.com using OpenMerch."

Each ask resolves to **one** OpenMerch job (`contact_discovery_v1`, `email-finder` operation)
for the single name + domain combination.

## Sample run

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
node find-email.mjs Jane Doe acme.com
```

## Sample output

`position` and `linkedin_url` appear only when the provider has them. `raw` is the full
unmodified OpenMerch job output and is the source of truth for all fields.

```json
{
  "email": "jane@acme.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "domain": "acme.com",
  "position": "Head of Sales",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "score": 90,
  "raw": {
    "data": {
      "data": {
        "email": "jane@acme.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "score": 90,
        "domain": "acme.com",
        "position": "Head of Sales",
        "linkedin_url": "https://linkedin.com/in/janedoe"
      }
    }
  },
  "cost_usd": 0.013,
  "job_id": "f1e2d3c4-0000-0000-0000-abcdef123456"
}
```

> Note: `score` is a 0–100 confidence value from the provider. 90+ indicates high confidence.
> The values above are illustrative. The real price is whatever `/v1/plan` quotes, and `cost_usd`
> reflects the actual `cost.total_microcents` OpenMerch charged.

## When it can't run

- If `/v1/plan` returns `can_execute: false`, the skill stops and reports why (e.g. no provider
  available, account/budget issue) — it does **not** execute or charge you.
- If the job ends `failed` or `cancelled`, the skill reports the `error.code` / `error.message`.
- This skill finds email addresses — it does not verify deliverability or check reputation.
