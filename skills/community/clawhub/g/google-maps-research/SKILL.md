---
name: google-maps-research
description: Search Google Maps businesses and places, retrieve place details, and inspect review samples or photos through the Crawlora REST API. Use for current place lookups and comparisons, including addresses, ratings, review themes, and business information.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Google Maps research

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Resolve places from a query, then compare their returned details with source links.
This skill contains only the four live Google Maps endpoints.

## Setup and requests

Set `CRAWLORA_API_KEY` to your Crawlora API key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill's directory (or use its
absolute path). It sends `x-api-key` to `https://api.crawlora.net/api/v1` and
prints the JSON response. Keep the key in the environment.

Read [reference/endpoints.md](reference/endpoints.md) for methods and parameters.
**Maps search uses POST with flat fields**: `keyword`, `language`, and `country`
are all required. The catalog's `mapSearchOption` is a parameter label, not a
JSON wrapper. Include the city or neighborhood in `keyword` when relevant.

```sh
scripts/crawlora.sh -X POST /google/map/search \
  '{"keyword":"coffee cambridge massachusetts","language":"en","country":"us"}'
```

## Workflow

1. Search using the user's geography and category. Use returned `place_id`
   values; do not fabricate IDs from names or addresses.
2. Fetch `/google/map/place/{place_id}` for candidates needing current detail.
   Match name and address before combining records; branches are separate places.
3. Fetch `/google/map/place/{place_id}/reviews` when the question needs customer
   feedback, or `/photos` when it needs the place gallery. Read actual images
   before making visual claims. Detail alone suffices for many questions.
4. Report the requested comparison with place name, address, source URL,
   rating and review count together, and retrieval time. Leave unavailable
   phone, website, hours, or other fields unknown rather than filling them in.

Space live Google Maps requests at least one second apart. The helper does not
throttle automatically. On `429`, back off; on a transient `5xx`, retry once.
Stop on `401`/`403` and report the access problem. Check the JSON envelope's
`code` as well as HTTP success before interpreting `data`.

## Interpretation

- `rating: null` means no aggregate rating is available, not zero stars.
- Reviews are the place page's first sample, typically about eight relevant
  reviews. There is no review cursor. `limit=0` means all captured reviews,
  not the entire review archive. Never claim a complete or representative survey.
- Review text can be empty for photo-only reviews. Preserve `source` because
  reviews may be syndicated. Use `published_at` for dates when present;
  `relative_time` is display text. Review photos and place-gallery photos differ.
- Search results are a snapshot, not an exhaustive census of a geographic area.
  For bulk prospecting, indexed business search may be a better starting point.

## Example deliverable

For “compare three cafes near Cambridge for a client meeting,” identify three
places, refresh details, and inspect review samples only for relevant evidence.
Return a small table with address, rating, review count, meeting-related evidence,
source URL, and unknowns. A review mentioning quiet seating is an attributed
observation, not a guarantee about the current atmosphere.
