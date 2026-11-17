---
name: mapsdata-google-maps-leads
description: Search live Google Maps businesses or enrich supplied companies with Mapsdata when a user needs local leads, business details, owner or decision-maker names, verified emails, phone intelligence, social profiles, CSV-ready data, or API-driven prospecting.
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      env:
        - MAPSDATA_API_KEY
      bins:
        - curl
    primaryEnv: MAPSDATA_API_KEY
    envVars:
      - name: MAPSDATA_API_KEY
        required: true
        description: Mapsdata API key created at https://www.mapsdata.io/api-access
    emoji: "🗺️"
    homepage: https://www.mapsdata.io
---

# Mapsdata Google Maps Leads

Use Mapsdata to discover local businesses from Google Maps, run the complete contact-enrichment pipeline, or enrich companies the user already has from business names and website URLs.

Base URL: `https://www.mapsdata.io/api/v1`

API documentation: `https://www.mapsdata.io/docs`

## Before Calling the API

- Read the API key from `MAPSDATA_API_KEY`. If it is missing, direct the user to `https://www.mapsdata.io/api-access` and ask them to set it at runtime.
- Never print, persist, commit, log, or place the API key in a generated file. Do not put it directly in a shell command when an environment variable is available.
- A creation request reserves lead credits. If the user explicitly asked to run a search or enrichment with clear scope, that request authorizes the matching job. Otherwise, explain the intended workflow and credit reservation and ask before creating it.
- Read-only account, location, category, status, list, and result requests do not consume lead credits.

Authenticate every request with:

```bash
-H "x-api-key: $MAPSDATA_API_KEY"
```

## Choose the Workflow

Use the smallest workflow that satisfies the request:

1. **Discovery only**: `POST /searches` with `enrich_contacts: false`. Returns Google Maps business data without contact enrichment.
2. **Complete pipeline**: `POST /searches` with `enrich_contacts: true`. Discovers businesses and enriches owners, decision makers, emails, phones, social profiles, and verification data.
3. **Standalone enrichment**: `POST /enrichments`. Use when the user already has business names and absolute website URLs.
4. **Selective two-stage workflow**: run discovery without contact enrichment, select businesses with useful websites, then submit only those businesses for standalone enrichment. Discovery and enrichment are charged separately.

## Check the Account First

Before creating work, call:

```bash
curl -sS "https://www.mapsdata.io/api/v1/account" \
  -H "x-api-key: $MAPSDATA_API_KEY"
```

Use `credits_remaining` and `max_results_per_search` as the runtime source of truth.

- Searches must request at least 100 businesses.
- Free accounts receive one 100-credit job and can request at most 100 search results.
- Active paid accounts can request 100 to 700 search results, subject to remaining credits.
- Standalone enrichment accepts 1 to 700 unique businesses, subject to plan and remaining credits.
- Never silently reduce the user's requested quantity. If it exceeds the live limit or balance, explain the constraint and ask whether to use an affordable value.

## Search Workflow

### 1. Resolve the Location

Use the same location catalog as the Mapsdata UI:

```bash
curl -sS "https://www.mapsdata.io/api/v1/locations?q=New%20York&country=US" \
  -H "x-api-key: $MAPSDATA_API_KEY"
```

If multiple locations match, ask the user which one they mean. Copy the selected result's `label` to `input.location` and `country_code` to `input.countryCode`.

### 2. Optionally Resolve a Category

When category precision matters, call:

```bash
curl -sS "https://www.mapsdata.io/api/v1/categories?q=plumber" \
  -H "x-api-key: $MAPSDATA_API_KEY"
```

Use the selected category's `display_name` as `input.query`. Free-text queries remain valid when the user wants a broader search.

### 3. Create One Idempotent Search

Generate one stable `Idempotency-Key` for the logical job and retain it for retries. Do not create a new key because a request or poll timed out.

```bash
curl -sS -X POST "https://www.mapsdata.io/api/v1/searches" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAPSDATA_API_KEY" \
  -H "Idempotency-Key: chicago-plumbers-2026-10-01" \
  -d '{
    "name": "Chicago plumbers",
    "input": {
      "query": "plumbers",
      "location": "Chicago, Illinois",
      "countryCode": "US",
      "maxResults": 100,
      "language": "en"
    },
    "enrich_contacts": true
  }'
```

Persist the returned `job_id`. Mapsdata returns `202 Accepted` and makes the job visible in the user's dashboard.

### 4. Poll Status and Read Live Results

Poll every 5 to 10 seconds:

```bash
curl -sS "https://www.mapsdata.io/api/v1/searches/JOB_ID" \
  -H "x-api-key: $MAPSDATA_API_KEY"
```

Treat only `completed` and `failed` as terminal. Active states can include `queued`, `starting`, `running`, `importing`, and `enriching`.

Partial businesses appear before completion:

```bash
curl -sS "https://www.mapsdata.io/api/v1/searches/JOB_ID/results?page=1&page_size=500" \
  -H "x-api-key: $MAPSDATA_API_KEY"
```

During a long job, summarize real progress from the status response rather than implying that the job is stuck.

### 5. Fetch the Final Result Set

After the job becomes terminal, fetch again from page 1. Increment `page` until `has_more` is `false`, deduplicate by result `id`, and confirm that the collected count matches `total`.

Do not report an email as verified merely because it exists. Inspect `email_verifications` and `email_verification_status`. Treat invalid addresses as unusable and describe catch-all, risky, or unknown results accurately.

## Standalone Enrichment Workflow

Use this for companies the user already has:

```bash
curl -sS -X POST "https://www.mapsdata.io/api/v1/enrichments" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MAPSDATA_API_KEY" \
  -H "Idempotency-Key: supplied-businesses-2026-10-01" \
  -d '{
    "name": "Businesses to enrich",
    "businesses": [
      {
        "business_name": "Example Plumbing Company",
        "website_url": "https://example.com"
      }
    ]
  }'
```

Requirements:

- Each item needs a real business name and an absolute `http://` or `https://` company website URL.
- Remove duplicate name-and-website pairs before submission.
- Persist the returned `job_id`.
- Poll `GET /enrichments/{job_id}` every 5 to 10 seconds.
- Read live rows from `GET /enrichments/{job_id}/results` and repeat full pagination after completion.
- Do not poll enrichment jobs through `/searches/{id}` or search jobs through `/enrichments/{id}`.

## Result Fields

Use the fields that actually exist instead of inventing aliases:

- Business: `title`, `category`, `categories`, `address`, `city`, `state`, `postal_code`, `country_code`, `rating`, `review_count`, `business_status`.
- Google identity: `position`, `rank`, `place_id`, `cid`, `google_maps_url`, `claimed`.
- Website and phones: `website`, `phone`, `additional_phones`, `phone_types`, `phone_verifications`.
- People: `owner_name`, `owner_names`, `decision_maker_names`, `verified_owner_names`, `verified_decision_maker_names`.
- Emails: `emails`, `owner_emails`, `decision_maker_emails`, `email_verifications`, `email_verification_status`.
- Public profiles: `socials`.
- Pipeline: per-source enrichment statuses plus the parent job status.

Standalone enrichment begins with the submitted name and website. Google Maps-only fields can remain `null` because no Maps discovery was requested.

## Error and Retry Behavior

- `401`: key missing, invalid, revoked, or no longer associated with a user. Stop and ask the user to replace it.
- `402`: insufficient credits or inactive subscription. Explain the required and available credits; do not retry unchanged.
- `403`: free-plan, plan, or 700-business product limit exceeded. Offer a permitted size.
- `404`: job not found for this account or wrong endpoint family. Verify the ID and route.
- `409`: idempotency key was reused with a different request. Restore the original body or use a new key only for genuinely new work.
- `422`: invalid input, including a search below 100 results. Correct the request before retrying.
- `428`: production creation omitted `Idempotency-Key`. Add the original logical key.
- `429`: request or active-job limit reached. Honor `Retry-After`, then use exponential backoff with jitter.
- `503`: required production service unavailable. Retry later with the same creation body and idempotency key.

The account-wide request limit is 1,000 requests per rolling 60 seconds across all API keys. There is no separate daily or monthly request cap.

## Present the Result

Give the user:

- Job ID, terminal status, requested quantity, returned count, and credits charged.
- A concise coverage summary for websites, business emails, owner or decision-maker names, direct emails, and phone numbers.
- A clear distinction between business contacts and named-person contacts.
- Verification status alongside every email used in the answer.
- A structured table or file only when it suits the requested output.
- A direct statement that the same job and leads are available in their Mapsdata dashboard.

Never initiate outreach, send messages, upload leads to another service, or export private data beyond the requested destination without the user's explicit authorization.

## References

- Quickstart: `https://www.mapsdata.io/docs`
- Complete endpoint reference: `https://www.mapsdata.io/docs/endpoints/create-search`
- Data fields: `https://www.mapsdata.io/docs/reference/data-fields`
- Plans and credits: `https://www.mapsdata.io/docs/reference/plans-and-credits`
- Errors and rate limits: `https://www.mapsdata.io/docs/reference/errors-and-rate-limits`
- Machine-readable product reference: `https://www.mapsdata.io/llms-full.txt`
- Machine-readable pricing: `https://www.mapsdata.io/pricing.md`

