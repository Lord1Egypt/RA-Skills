---
name: google-jobs-research
description: Searches Google's public careers site (careers.google.com) via the Crawlora API and pulls single job postings by id, returning clean JSON. Use when the user wants to search Google Jobs, see what roles Google is hiring for in a location, or pull the full detail of a specific Google Jobs posting.
---

# Google Jobs search

Search Google's public careers site and pull one posting's full detail —
description, responsibilities, and qualifications — as normalized JSON from
the Crawlora API, no scraping careers.google.com by hand.

## When to use this skill

- "Search for <role> jobs at Google in <location>."
- "What is Google currently hiring for in <team/location>?"
- "Pull the full detail (description, responsibilities, qualifications) for Google job id <id>."
- "Track new Google Jobs postings for <role> over time."

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Search** — `/google-jobs/search` takes a required `q` (search query),
   plus optional `location` (free text) and `page` (1-based). It parses
   careers.google.com's server-rendered search page's embedded job data, so
   each result already includes the description, responsibilities, and
   qualifications inline — no second call needed just to read a listing.
   Page size is fixed by Google at 20 results; pass `page` to walk further
   pages.
2. **Job detail** — `/google-jobs/job` takes the required `id` (the numeric
   Google job id returned by search) and re-fetches that single posting's
   full server-rendered detail page. Use it to refresh one posting or to
   fetch a job by id when you already have it from elsewhere (e.g. a saved
   link).

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search:
scripts/crawlora.sh /google-jobs/search q="software engineer" location="Mountain View" | jq '.'

# Job detail by id:
scripts/crawlora.sh /google-jobs/job id=123456789012345 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for both Google Jobs
endpoints this skill uses.

## Examples

- **Role search in a location:** `/google-jobs/search` with
  `q="data scientist"` and `location="New York"`, paging with `page=2`,
  `page=3` to collect more than 20 results.
- **Track a specific posting:** save the `id` from a search result, then poll
  `/google-jobs/job` for that `id` on a schedule to detect edits or removal
  (a `404`/empty response signals the posting closed).

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public careers.google.com postings; respect Google's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **Page size is fixed at 20** by Google — there's no `limit`/`per_page`
  param, only `page` to move through results.
- **`id` must be the numeric Google job id** from a search result's `id`
  field, not a slug or URL.
