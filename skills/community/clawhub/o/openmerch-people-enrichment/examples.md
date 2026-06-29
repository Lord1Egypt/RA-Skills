# Examples

Natural things an OpenClaw user might ask, and what the skill does.

> **Privacy notice:** Results include email addresses, full names, and LinkedIn URLs.
> Use only for lawful, authorized purposes. Minimize storage and sharing of results.

## Example asks

- "Get the full profile for person ID abc123."
- "Enrich this lead — their Apollo ID is xyz789."
- "What's Jane Doe's email? Her Apollo ID is def456."

Each ask resolves to **one** OpenMerch job (`people_enrichment_v1`, `people-enrichment` operation)
for the given Apollo person ID.

Apollo person IDs are returned by `openmerch-people-search` in the `id` field of each result.

## Sample run

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
node people-enrichment.mjs abc123
```

## Sample output

All profile fields are included only when the upstream response contains them — not all
persons have every field populated. The values below are illustrative; the real price is
whatever `/v1/plan` quotes.

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
  "job_id": "f1e2d3c4-0000-0000-0000-abcdef123456"
}
```

## When it can't run

- If `/v1/plan` returns `can_execute: false`, the skill stops and reports why (e.g. no provider
  available, account/budget issue) — it does **not** execute or charge you.
- If the job ends `failed` or `cancelled`, the skill reports the `error.code` / `error.message`.
