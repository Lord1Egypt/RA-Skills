---
name: job-market-research
description: Researches job postings, hiring signals, and freelance gigs via the Crawlora API — Indeed, Google/Amazon/Apple/Meta/Tesla careers sites, any company's ATS board (Greenhouse, Lever, Workday, SmartRecruiters, Ashby, and more), plus Upwork and Fiverr — returning clean JSON. Use when the user wants to search job postings, see what a specific company is hiring for, aggregate hiring signals for a company, or research freelance gigs and sellers.
---

# Job market & hiring research

Search job postings, pull a company's live openings straight from its ATS,
and research freelance gigs — all as normalized JSON from the Crawlora API,
no scraping job boards or ATS pages by hand.

## When to use this skill

- "Search for <role> jobs in <location>." (Indeed, Google/Amazon/Apple/Meta/Tesla careers)
- "What is <company> currently hiring for?" — pull their ATS board directly.
- "Which ATS does <company> use?" / "find any company's job board."
- "Is <company> hiring aggressively?" — aggregate hiring-signal analysis.
- "Find freelancers / gigs for <skill>" (Upwork, Fiverr).

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **Job boards & search engines** — `/indeed/search` (keyword + location),
   `/google-jobs/search` (careers.google.com), and the dedicated
   `/amazon-jobs/search`, `/apple-jobs/search`, `/meta-jobs/search`,
   `/tesla-jobs/list` for those employers. Each has a matching `.../job`
   (or `/list`/`/board`) detail endpoint for one posting.
2. **Any company's ATS board** — first resolve which system they use:
   `/jobs/company-search` probes Greenhouse, Lever, Ashby, SmartRecruiters,
   Workday, and more for a company slug. Then list postings via the matching
   endpoint: `/jobs/greenhouse/board` (param `token`), `/jobs/lever/postings`,
   `/jobs/workday/board`, `/jobs/smartrecruiters/postings`,
   `/jobs/ashby/board` (param `org`), `/jobs/recruitee/offers`, `/jobs/workable/postings`,
   `/jobs/rippling/board`, `/jobs/icims/board`, `/jobs/oracle/board`,
   `/jobs/ukg/board`, `/jobs/personio/feed`, `/jobs/pinpoint/board`,
   `/jobs/teamtailor/jobs`, `/jobs/eightfold/board`, `/jobs/gem/board` — one
   endpoint per ATS, each with a matching single-posting detail endpoint.
   Each ATS uses its own slug param name (`token`, `company`, `org`,
   `tenant`+`datacenter`+`site`, or `domain`) — see `reference/endpoints.md`.
3. **Hiring signals** — `/jobs/hiring-signals` aggregates a company's ATS
   board into a hiring-velocity summary (headcount growth proxy) in one
   call. Pass `provider` (the ATS name) plus that provider's slug param
   (e.g. `provider=greenhouse` + `token=<slug>`, or `provider=ashby` + `org=<slug>`).
4. **Freelance** — `/upwork/search` / `/fiverr/search` for gigs and jobs;
   `/upwork/job/{id}`, `/fiverr/gig/{username}/{slug}` for detail;
   `/upwork/freelancer/{id}`, `/fiverr/seller/{username}` for profiles.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# Search:
scripts/crawlora.sh /indeed/search q="staff engineer" l="Remote" | jq '.'

# Resolve then pull a company's ATS board:
scripts/crawlora.sh /jobs/company-search slug=stripe | jq '.'
scripts/crawlora.sh /jobs/greenhouse/board token=stripe | jq '.data'

# Hiring signals:
scripts/crawlora.sh /jobs/hiring-signals provider=greenhouse token=stripe | jq '.'

# Freelance:
scripts/crawlora.sh /upwork/search q="react developer" | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every Indeed,
Google/Amazon/Apple/Meta/Tesla Jobs, ATS (`Jobs` group), Upwork, and Fiverr
endpoint this skill uses.

## Examples

- **"Is company X scaling?"** — `/jobs/company-search` to find their board,
  `/jobs/hiring-signals` for a velocity summary, then the raw board endpoint
  to see which teams/roles are open.
- **Cross-source role search:** `/indeed/search` + `/google-jobs/search` for
  the same title/location, dedupe by company + title.
- **Competitor hiring watch:** pull the ATS boards of 3-4 competitors on a
  schedule and diff new postings between runs.
- **Freelance rate-check:** `/upwork/search` for a skill, collect budgets
  across postings to estimate a market rate.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public postings/boards; respect each source's terms.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- **ATS boards need the company's board slug**, not their public brand name —
  use `/jobs/company-search` first if you don't already know it.
- Results are paginated on most `search`/board-list endpoints — pass `page`
  to walk the full list.
