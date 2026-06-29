# Examples

Natural things an OpenClaw user might ask, and what the skill does.

## Example asks

- "Find SREs at Amazon."
- "Who are the engineering managers at Stripe?"
- "Find VP of Product roles at Notion."
- "Show me backend engineers at stripe.com."

Each ask resolves to **one** OpenMerch job (`people_enrichment_v1`, `people-search` operation)
for the domain + keyword combination. Results include first name, obfuscated last name, title,
and company — one page of up to 25 matches.

## Sample run

```bash
export OPENMERCH_API_KEY="om_live_xxxxxxxx"
node people-search.mjs stripe.com "backend engineer"
```

## Sample output

Last names are obfuscated by the provider. `total_entries` is the provider's total match count
across all pages (included when available). The values below are illustrative; the real price is
whatever `/v1/plan` quotes.

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
    },
    {
      "id": "def456",
      "first_name": "Marcus",
      "last_name_obfuscated": "W.",
      "title": "Staff Engineer",
      "organization": "Stripe"
    }
  ],
  "cost_usd": 0.0059,
  "job_id": "f1e2d3c4-0000-0000-0000-abcdef123456"
}
```

> Note: last names are obfuscated. For full profiles (email, LinkedIn URL, full name),
> use the **openmerch-people-enrichment** skill with the `id` returned here.

## When it can't run

- If `/v1/plan` returns `can_execute: false`, the skill stops and reports why (e.g. no provider
  available, account/budget issue) — it does **not** execute or charge you.
- If the job ends `failed` or `cancelled`, the skill reports the `error.code` / `error.message`.
- `per_page` and `page` must be positive integers; the script exits with a usage error otherwise.
