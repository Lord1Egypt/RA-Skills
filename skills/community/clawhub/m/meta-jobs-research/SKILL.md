---
name: meta-jobs-research
description: Searches and pulls postings from Meta's public careers site (metacareers.com) via the Crawlora API — full catalog listing, filtered search by team/technology/location/employment-type, and single-posting detail — returning clean JSON. Use when the user wants to find Meta job openings, track a category or team's open roles over time, or look up one specific Meta posting by id.
---

# Meta Jobs search

Search and enumerate Meta's open requisitions straight from metacareers.com
as normalized JSON from the Crawlora API, no scraping the careers site by
hand.

## When to use this skill

- "Search Meta jobs for <team/technology> in <location>."
- "What is Meta currently hiring for in AI/AR-VR/Security?"
- "Track every new Meta requisition this week." — walk `/meta-jobs/list` by
  `last_modified` on a schedule.
- "Look up this Meta job id" — pull the full posting detail.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Full-catalog listing** — `/meta-jobs/list` pages through Meta's own
   public job sitemap: every open requisition's id, canonical URL, and
   last-modified timestamp, with no team/location/keyword filtering. Use
   this for full-catalog enumeration or change tracking via
   `last_modified`.
2. **Filtered search** — `/meta-jobs/search` hits Meta's own anonymous
   jobsearch GraphQL endpoint with the same team/technology/location/
   employment-type/keyword/remote/sort filters the live search page offers.
   All filters are optional and AND together; an empty request returns
   Meta's entire open-requisition catalog in one response. `q` matches
   team, technology, location, or ref/req-code — it is NOT a free-text
   search over job titles or descriptions.
3. **Single-posting detail** — `/meta-jobs/job` returns one Meta Careers
   posting by its numeric job id (the `id` field returned by search or
   list), parsed from metacareers.com's server-rendered job detail page.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Filtered search — AI team, remote-only, newest first:
scripts/crawlora.sh /meta-jobs/search teams="Artificial Intelligence" is_remote_only=true sort_by_new=true | jq '.'

# Full catalog, paged:
scripts/crawlora.sh /meta-jobs/list page=1 page_size=200 | jq '.'

# Single posting by id (id comes from search/list results):
scripts/crawlora.sh /meta-jobs/job id=1234567890123456 | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for all Meta Jobs endpoints this skill uses.

## Examples

- **"Is Meta ramping up hiring in AR/VR?"** — `/meta-jobs/search`
  `teams=AR/VR` `sort_by_new=true`, review the resulting postings' dates
  and locations for a hiring-velocity read.
- **Weekly new-requisition diff:** page `/meta-jobs/list` by
  `last_modified`, store the id set, and diff against last week's run to
  surface newly-opened roles.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public postings from metacareers.com; respect Meta's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **`q` is a facet-name match, not full-text search** — it matches team,
  technology, location, or ref/req-code, not job titles or descriptions;
  use `teams` for a topical filter instead.
- **`teams` and `roles` are closed enums** — see `reference/endpoints.md`
  for the exact values (team names double as technology names in the same
  field); values outside the enum won't match.
- **`offices` is a repeatable location-id filter in Meta's own id format**
  (e.g. `menlo-park`, `london`), not a free-text city name, and not a
  closed enum — get valid ids from search results.
- Results are paginated on `/meta-jobs/list` (`page`, `page_size`, max 200)
  — walk it to enumerate the full catalog.
