---
name: local-competitive-landscape
description: Compare observed local business supply, categories, attributes, hours, and review-sample themes across defined areas using Crawlora's Google Maps dataset, live Google Maps, Apple Maps, and Yelp. Use for matched-area competitor landscapes and coverage comparisons; for user-supplied candidate-site screening with access and diligence gaps, use business-location-screening. Neither estimates demand, sales, or site viability.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Local competitive landscape

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Compare like-for-like observations of businesses across defined areas. Produce a
traceable market map without turning search-result coverage into a population,
demand, revenue, or site-selection estimate.
For a pre-screen of user-supplied candidate business locations that also needs
route/access evidence and a missing-data checklist, use business-location-screening.

## Setup and API contract

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for exact
parameters and response behavior. Check the application `code` as well as HTTP
status. Stop on `401`/`403`, back off on `429`, and retry a transient `5xx` once.
A failed request is unavailable evidence, not an empty area. Keep Google Maps
calls at least one second apart.

## Define a comparable frame

1. Record each named area and its operational boundary: administrative name,
   radius with center coordinates, or explicit polygon supplied by the user.
   Record the business concept, inclusion rules, closure treatment, sources,
   filters, retrieval date, page/limit budget, and whether all available pages
   or only a bounded sample will be collected.
2. Use identical category, geography type, status filters, dates, pagination,
   and source mix across areas. Do not treat a Google radius in meters as
   equivalent to an Apple viewport `span` in latitude/longitude degrees. Keep a
   separate coverage row for every source and area when geometry differs.
3. Discover exact dataset category values with
   `/datasets/google-map-businesses/facets?facet=category`; pass returned values
   unchanged. A text query can return businesses whose primary category differs,
   so preserve every source's returned category and apply the stated inclusion
   rule locally.

```sh
scripts/crawlora.sh /datasets/google-map-businesses/facets \
  facet=category q=coffee permanently_closed=false
# Set CATEGORY to one exact `.data.items[].value` returned above.
scripts/crawlora.sh /datasets/google-map-businesses/search \
  category="$CATEGORY" lat=42.3736 lon=-71.1097 radius_m=2000 \
  permanently_closed=false sort=distance_asc page=1 page_size=100
scripts/crawlora.sh -X POST /google/map/search \
  '{"keyword":"coffee shop Cambridge Massachusetts","language":"en","country":"us"}'
```

## Collect and reconcile coverage

1. Use `/datasets/google-map-businesses/search` for a bounded indexed-corpus
   baseline. Capture `total`, page, page size, filters, and whether the result
   window was exhausted. Dataset totals describe Crawlora's indexed corpus, not
   the business population. A zero or short result cannot prove local absence.
   Preserve each record's dataset update/crawl timestamp separately from request
   retrieval time; matched request dates do not make stored records equally fresh.
   Use `/datasets/google-map-businesses/items/{place_id}` only when a stored row
   needs its full record.
2. Run the same live Google query wording for every area. Post-filter returned
   coordinates or addresses against the defined boundary. Search ranking and a
   bounded result list can omit relevant businesses, so retain both returned and
   in-area counts. Refresh selected ambiguous or representative rows with
   `/google/map/place/{place_id}`.
3. Run Apple searches with the same query, regional catalog, language, span, and
   limit. Record Apple's returned region and `relocated`; discard results outside
   the intended boundary. A relocated search is evidence about Apple's fallback,
   not about the target area. Apple has no pagination, so a full returned viewport
   is still a bounded result set.
4. Run Yelp with the same term and location convention, paging only to the stated
   bound. Refresh selected rows with `/yelp/business/{id}`. Provider search areas
   and ranking differ; compare source-specific observations before merging them.
5. Preserve businesses with unknown coordinates or status in an unknown bucket.
   `permanently_closed=false` excludes confirmed closures but can retain dataset
   rows with `null` status; it does not certify they are open. Radius searches
   omit locationless service-area businesses, so run a matched text/area check if
   those businesses are in scope and disclose the omission otherwise.

Deduplicate within each area and source by provider ID first. Across providers,
require consistent name, address, coordinates, phone, or domain evidence. Keep
chain branches separate unless the evidence identifies the same location. Retain
source-specific IDs and disagreements after a merge. Do not assume a dataset
`place_id` and live Google `place_id` are interchangeable when their formats or
provenance differ: use the raw dataset ID for the stored-item endpoint, then
resolve the business through live search using name and address before calling
live Google detail unless ID compatibility has been established. Assign a business
to every area whose boundary contains it, but do not sum overlapping-area counts
as a unique total.

## Compare the areas

Create three linked outputs:

- **Coverage ledger:** area, source, query/category, geometry, filters, page or
  limit range, retrieved count, in-area count, unknown-location count, relocated
  status, exhausted/bounded/failed status, and retrieval time.
- **Business matrix:** area membership, canonical branch, provider IDs, source
  names and categories, address/coordinates, status, hours/attributes when
  returned, rating, review count, source URLs, retrieval time, and match confidence.
- **Comparison:** deduplicated observed counts and category/attribute mix within
  each matched frame, with unknowns and source disagreements shown beside every
  conclusion.

Treat `rating: null` and `review_count: null` as unknown, distinct from numeric
zero. Compare ratings only within the same platform and state sample sizes; do
not blend Google, Apple, and Yelp rating scales or rank areas from cross-platform
averages. Use `/google/map/place/{place_id}/reviews` only for a small, disclosed
sample of visible review themes. Report theme counts within that sample, retain
source/date, and do not infer customer-population prevalence.

Missing hours or service attributes are unknown, never evidence that a service
is absent. Keep returned attributes source-specific and date them; do not infer
that an unlisted amenity, offering, or schedule is unavailable.

Call a finding a **proven service gap** only when the service definition is
explicit, complete eligible-business coverage establishes the candidate set, and
verified service attributes establish absence across that set. Bounded map and
directory listings ordinarily support only an **observed gap in the collected
sample** with **search omission risk**. State which one the evidence supports. Do
not turn business counts, ratings, or review themes into demand, revenue, market
share, sales potential, or site-viability claims.
