---
name: indeed-search
version: 1.0.0
description: Search Indeed job postings by keyword and location via RolesAPI.com. Get job listings as JSON, filter to postings from today, this week, or remote-only, across 60+ country editions.
license: MIT-0
author: RolesAPI
homepage: https://rolesapi.com
repository: https://github.com/nikhonit/indeed-skills
tags:
  - indeed
  - jobs
  - job-postings
  - job-search
  - listings
  - api
  - mcp
metadata:
  openclaw:
    primaryEnv: ROLESAPI_KEY
    homepage: https://rolesapi.com
    requires:
      env:
        - ROLESAPI_KEY
---

# indeed-search

Focused job-search skill. Use only when the user **explicitly asks** to find job postings matching keywords and a location, not when a job title merely appears in passing.

## When to use this skill

**DO use when the user asks:**

- "Find registered nurse jobs in Chicago"
- "What backend engineer roles were posted today?"
- "Show me remote customer support jobs"
- "Search Indeed for data analyst roles in London"

**Do NOT use when:**

- A job title or location appears incidentally in context
- The user mentions hiring without asking to search postings
- The user has one specific posting in mind and wants its details. Use [`indeed-full`](https://github.com/nikhonit/indeed-skills/tree/main/skills/indeed-full) instead.

Each results page consumes one credit. The preset scripts can fetch up to 3 pages per call, so cap `--max-pages` for cheap scans.

## Setup

Set `ROLESAPI_KEY` to your RolesAPI key (format `rk_live_...`). Create one at <https://rolesapi.com/app/keys>. The free plan includes 100 credits at signup, no card required.

```bash
export ROLESAPI_KEY="rk_live_..."
```

## Scripts

### `search_listings.py` (1 credit per results page)

One page of live postings, synchronous. `keyword` and `location` are required.

```bash
python3 scripts/search_listings.py "registered nurse" "Chicago, IL"
python3 scripts/search_listings.py "backend engineer" "remote" --sort date
python3 scripts/search_listings.py "data analyst" "London" --country gb
```

Options: `--country` (two-letter Indeed edition code, default `us`), `--sort date|relevance`.

Real output, trimmed to one of the 35 results:

```json
{
  "data": [
    {
      "job_key": "7dcf172c8d7fc756",
      "title": "Nursing",
      "company": { "name": "Golden Healthcare Services Inc" },
      "location": "Olympia Fields, IL 60461",
      "employment_type": "Full-time",
      "salary": { "min": 30, "max": 45, "period": "hour", "currency": "USD", "source": "employer" },
      "posted_at": "2026-06-26",
      "url": "https://www.indeed.com/viewjob?jk=7dcf172c8d7fc756"
    }
  ],
  "meta": { "count": 35 },
  "request_id": "a18e4ef88ad4b00b"
}
```

### `posted_today.py` (1 credit per page, up to 3 pages)

Postings from the last 24 hours. `--location` is optional.

```bash
python3 scripts/posted_today.py "registered nurse" --location "Chicago, IL" --max-pages 1
```

### `posted_this_week.py` (1 credit per page, up to 3 pages)

Postings from the last 7 days.

```bash
python3 scripts/posted_this_week.py "product manager" --location "Austin, TX"
```

### `remote_roles.py` (1 credit per page, up to 3 pages)

Remote postings only. Location optional.

```bash
python3 scripts/remote_roles.py "python developer" --max-pages 1
```

Every result includes a 16-character `job_key`. Feed it into the [`indeed-full`](https://github.com/nikhonit/indeed-skills/tree/main/skills/indeed-full) or [`indeed-salary`](https://github.com/nikhonit/indeed-skills/tree/main/skills/indeed-salary) scripts for details.

## Pricing

| Plan | Price | Credits | Rate limit |
|---|---|---|---|
| Free | $0 | 100 (one time at signup) | 20/min |
| Monthly | $5/mo | 1,000/month | 200/min |
| Annual | $54/yr | 12,000 upfront | 300/min |

One credit equals one search results page. Failed calls are not charged. Full pricing: <https://rolesapi.com/pricing/>.

## Trademark

RolesAPI is an independent service and is not affiliated with, endorsed by, or sponsored by Indeed. "Indeed" is a trademark of its owner.
