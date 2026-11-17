---
name: local-business-prospecting
description: Build and qualify local-business prospect lists by category and geography using Crawlora's Google Maps dataset, live Google Maps, Apple Maps, Yelp, and public business websites. Use when the user wants a deduplicated lead shortlist or CSV with business contacts and qualification evidence.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Local-business prospecting

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Produce a business shortlist with transparent selection criteria and source
evidence. Researching a list does not authorize sending outreach or importing it
into a CRM; perform those actions only when the user requests them.

## Setup and requests

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill's directory or by absolute
path. It calls `https://api.crawlora.net/api/v1` with `x-api-key` and prints JSON.
Keep the key in the environment. Read [reference/endpoints.md](reference/endpoints.md)
for the exact parameters; providers use different geography and pagination fields.

## Workflow

1. Establish the business type, geography, requested count, and qualification
   criteria from the user's brief. If a material criterion is missing, ask;
   otherwise state a reasonable assumption and start with a small discovery page.
2. Search `/datasets/google-map-businesses/search` for bulk discovery. Use
   `/facets?facet=category` to discover exact, possibly localized category labels.
   Search supports `page_size` up to 100 and a 10,000-record result window.
   Radius searches require `lat`, `lon`, and `radius_m` (maximum 50,000 meters).
   Dataset counts describe this indexed corpus, not every business in the area.
3. For fresh discovery or sparse dataset results, use live Google Maps search.
   Apple Maps and Yelp can supplement coverage; read their individual parameters
   in the reference. Preserve source identities when merging results.
4. Deduplicate by provider ID first. Across providers, compare normalized name,
   address, domain, and phone; require consistent evidence before merging. A
   shared chain website alone does not make two branches the same business.
5. Refresh the most relevant candidates with live place detail. Inspect the
   business's own website only when contact or qualification evidence is needed.
   `POST /web/scrape` takes flat `url` and `formats` fields; `POST /extract` takes
   flat `url` and `schema` fields. Neither uses the catalog body label as a wrapper.
   Extract only publicly published business contact details and retain the exact
   source page. Do not infer email addresses or claim deliverability verification.
6. Apply the user's explicit rules, retain exclusion reasons, and stop when the
   requested count is met or the search bounds are reached. If scoring helps,
   explain the weights. A low rating is evidence of reviews, not proof of buying intent.

```sh
# Start with a small indexed discovery page:
scripts/crawlora.sh /datasets/google-map-businesses/search \
  q=coffee city=Cambridge country=US page_size=10

# Live discovery; body fields are flat, not nested under mapSearchOption:
scripts/crawlora.sh -X POST /google/map/search \
  '{"keyword":"coffee cambridge massachusetts","language":"en","country":"us"}'
```

## Output and limits

Return a table or CSV as requested. Useful columns are `business_name`,
`provider_ids`, `address`, `website`, `public_phone`, `public_email`, `rating`,
`review_count`, `qualification_evidence`, `source_urls`, `retrieved_at`, and
`refresh_status`. Keep dataset refresh time separate from retrieval time.

- `permanently_closed=false` excludes known closures but still includes unknown
  status (`null`). It does not certify that every result is open.
- `rating: null` is unknown; do not coerce it to zero. The dataset has a minimum
  rating filter, not a maximum: apply a “below four stars” rule locally, excluding
  unknown ratings. Google's review endpoint returns a small first-page sample.
- Locationless service-area businesses can lack coordinates. A radius query
  cannot discover them; use text/area searches if they belong in the brief.
- Bound discovery pages and live enrichments to the requested task. Report a
  shortfall rather than padding the list with weak matches.
- Keep Google Maps calls at least one second apart. On `429`, back off; retry a
  transient `5xx` once. Stop on `401`/`403`. Check application `code` too. Keep
  useful results when one source fails and mark which rows were not refreshed.
