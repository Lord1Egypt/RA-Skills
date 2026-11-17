---
name: indeed-research
description: Searches Indeed job postings and pulls single job listings via the Crawlora API — keyword + location search, location autocomplete, and job detail by job key — returning clean JSON. Use when the user wants to search Indeed for jobs, look up location suggestions for an Indeed search, or fetch the full detail of a specific Indeed posting.
---

# Indeed job search

Search Indeed job postings by keyword and location, resolve a valid location
string via autocomplete, and pull the full detail of a single posting — all
as normalized JSON from the Crawlora API, no scraping indeed.com by hand.

## When to use this skill

- "Search for <role> jobs in <location> on Indeed."
- "What's the right Indeed location string for <partial city/area>?"
- "Pull the full detail for this Indeed job (job key <jk>)."
- "Find recent <role> postings on Indeed within the last N days."
- "Page through Indeed search results for <role>."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Resolve a location (optional but recommended)** — `/indeed/locations/suggest`
   takes a partial location string (`q`) and returns Indeed's own autocomplete
   suggestions, the same ones the app's search bar offers, so you can build a
   valid `l` value for search instead of guessing.
2. **Search** — `/indeed/search` takes keywords (`q`, required) plus optional
   `l` (location), `radius`, `fromage` (only jobs posted within the last N
   days), `sort` (`relevance` or `date`), and `page` for pagination. Each
   result includes a `job_key` for pulling full detail.
3. **Job detail** — `/indeed/job` takes `jk` (the 16-character hex job key
   from a search result) and returns the full posting.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Resolve a location string:
scripts/crawlora.sh /indeed/locations/suggest q="san fran" | jq '.'

# Search:
scripts/crawlora.sh /indeed/search q="staff engineer" l="San Francisco, CA" fromage=7 sort=date | jq '.'

# Job detail (jk from a search result):
scripts/crawlora.sh /indeed/job jk=abcdef0123456789 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for all Indeed endpoints this skill uses.

## Examples

- **Role search with a fuzzy location:** `/indeed/locations/suggest` on the
  user's rough city name to get a valid `l` value, then `/indeed/search`
  with that value plus `q` and `sort=date` for the newest postings first.
- **Enrich a search result:** run `/indeed/search`, take the `job_key` off
  any hit, and call `/indeed/job` to pull the full description, salary, and
  application details for that one posting.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public Indeed postings; respect Indeed's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`page` 2+ and `fromage` fall back to a slower page-based transport** —
  page 1 with no `fromage` uses Indeed's fast credential-free GraphQL API;
  requesting page 2+ or filtering by `fromage` switches transports, with
  the same normalized response shape either way.
- **Location autocomplete has no page-based fallback** — `/indeed/locations/suggest`
  is GraphQL-only, so it can fail independently of search/job-detail.
- Results are paginated on `/indeed/search` — pass `page` to walk the full list.
