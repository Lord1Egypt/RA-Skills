# OpenMerch Company Brief — examples

## Example user queries

- "What industry is stripe.com in?"
- "How many employees does airbnb.com have?"
- "When was anthropic.com founded?"
- "What technologies does rippling.com use?"
- "Does openai.com have any funding data?"
- "Give me a company profile for notion.so."
- "Where is linear.app headquartered?"

## Sample command

```bash
node company-brief.mjs stripe.com
```

## Sample output

All optional fields are shown below — actual output omits any field the upstream
provider did not return. `cost_usd` reflects the actual charged amount (illustrative
here); `/v1/plan` provides the authoritative price before execution.

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
  "raw": {
    "data": {
      "organization": { "...": "verbatim upstream response" }
    }
  },
  "cost_usd": 0.006,
  "job_id": "f1e2d3c4-0000-0000-0000-abcdef123456"
}
```

## URL input

The script accepts any URL — protocol and path are stripped automatically:

```bash
node company-brief.mjs https://stripe.com/about
```

Both calls above produce the same result for `stripe.com`.

## Minimal output (sparse upstream response)

When the upstream provider returns only partial data, the output omits missing
fields. Only `domain`, `raw`, and `job_id` are always present:

```json
{
  "domain": "example.com",
  "name": "Example Co",
  "raw": { "data": { "organization": { "name": "Example Co" } } },
  "job_id": "a1b2c3d4-0000-0000-0000-000000000000"
}
```
