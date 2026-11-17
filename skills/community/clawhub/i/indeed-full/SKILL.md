---
name: indeed-full
version: 1.0.0
description: Complete Indeed job postings toolkit via RolesAPI.com. Search Indeed job postings by keyword and location, fetch full role details, look up salary for a job posting, and get descriptions, company info, and benefits across 60+ country editions.
license: MIT-0
author: RolesAPI
homepage: https://rolesapi.com
repository: https://github.com/nikhonit/indeed-skills
tags:
  - indeed
  - jobs
  - job-postings
  - job-search
  - salary
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

# indeed-full

Complete Indeed job postings toolkit via [RolesAPI.com](https://rolesapi.com). Use when the user **explicitly asks** to search job listings, look up a specific posting, check a salary, or pull role data for analysis.

## When to use this skill

Each script call consumes RolesAPI credits, so this skill activates only when the user's request is genuinely about jobs data, not when a job title or company merely appears in passing.

**DO use when the user:**

- Asks to search Indeed job postings by keyword and location (`search_listings.py`)
- Pastes an Indeed viewjob URL and asks about that posting (`get_role_by_url.py`)
- Has a job key and wants the full normalized posting (`get_role.py`)
- Asks what a specific posting pays (`get_salary.py`)
- Wants the full job description text (`get_description.py`)
- Asks about the hiring company or its rating (`get_company.py`)
- Asks what benefits a posting lists (`get_benefits.py`)
- Wants to check remaining API credits (`check_account.py`)

**Do NOT use when:**

- A job title or company appears incidentally in context
- The user is discussing careers abstractly without asking for data on specific postings
- The user has not signaled they want a job data lookup

When the intent is ambiguous, ask the user to confirm before calling a script. Calls cost credits and can return large records the user may not want.

## Setup

Set `ROLESAPI_KEY` to your RolesAPI key (format `rk_live_...`). Create one at <https://rolesapi.com/app/keys>. The free plan includes 100 credits at signup, no card required.

```bash
export ROLESAPI_KEY="rk_live_..."
```

## Scripts

All scripts live in `scripts/`, use only the Python standard library, print pretty JSON to stdout, and exit nonzero with the API error message on failure. Run them with `python3`.

### `search_listings.py` (1 credit per results page)

Search live postings by keyword and location. Both arguments are required. Returns role summaries with `job_key`s you can feed into the detail scripts.

```bash
python3 scripts/search_listings.py "registered nurse" "Chicago, IL" --sort date
python3 scripts/search_listings.py "data analyst" "London" --country gb
```

### `get_role.py` (1 credit)

Fetch one full normalized posting by 16-character job key: title, company with rating, location, employment type, salary, benefits, full description, posted date, and canonical URL. Use `--fields` to trim the payload, e.g. `--fields title,company.name,salary`.

```bash
python3 scripts/get_role.py 7dcf172c8d7fc756
```

### `get_role_by_url.py` (1 credit)

Same as above but takes a pasted Indeed viewjob URL. Use when the user shares a link.

```bash
python3 scripts/get_role_by_url.py "https://www.indeed.com/viewjob?jk=7dcf172c8d7fc756"
```

### `get_salary.py` (1 credit)

Only the salary object: min, max, currency, period, and whether the figure came from the employer or an estimate. Cheaper to reason over than the full posting.

```bash
python3 scripts/get_salary.py 7dcf172c8d7fc756
```

Real output:

```json
{
  "data": {
    "title": "Nursing",
    "company": {
      "name": "Golden Healthcare Services Inc"
    },
    "location": "Olympia Fields, IL 60461",
    "salary": {
      "min": 30,
      "max": 45,
      "period": "hour",
      "source": "employer",
      "currency": "USD"
    }
  },
  "request_id": "a18e4fa32b51ce3e"
}
```

Postings that list no salary omit the `salary` key.

### `get_description.py` (1 credit)

Only the description slice of a posting.

### `get_company.py` (1 credit)

Only the company slice: name, rating, and company page URL.

### `get_benefits.py` (1 credit)

Only the benefits list.

### `check_account.py` (free, no credits consumed)

Account check: plan, rate limit, and credit balance (`GET /v1/me`). Pass `--usage` for recent usage records (`GET /v1/usage`).

```bash
python3 scripts/check_account.py
```

## Going async

For high-volume work the API also offers async endpoints: `POST /v1/search` and `POST /v1/search/with-details` return a job id you poll at `GET /v1/jobs/{id}`, and `POST /v1/roles/batch` enriches up to 500 postings in one job with completion events via signed webhooks. See <https://rolesapi.com/api/search/> and <https://rolesapi.com/api/roles/>. These scripts stick to the synchronous endpoints, which cover most agent use.

## Pricing

| Plan | Price | Credits | Rate limit |
|---|---|---|---|
| Free | $0 | 100 (one time at signup) | 20/min |
| Monthly | $5/mo | 1,000/month | 200/min |
| Annual | $54/yr | 12,000 upfront | 300/min |

One credit equals one role detail or one search results page. Failed calls are not charged. Full pricing: <https://rolesapi.com/pricing/>.

## Errors

Errors print to stderr and the script exits nonzero. The API returns `{"error": {"code": "...", "message": "..."}}` with codes like `invalid_request`, `not_found`, `out_of_credits`, and `rate_limited`. Scripts retry once on 429 honoring the `Retry-After` header. On `out_of_credits` the script points to <https://rolesapi.com/app/billing>.

## API reference

- OpenAPI spec: <https://rolesapi.com/openapi.json>
- REST docs: <https://rolesapi.com/api/roles/> and <https://rolesapi.com/api/listings/>
- Hosted MCP server (zero-install alternative to this skill): <https://api.rolesapi.com/mcp>

## Trademark

RolesAPI is an independent service and is not affiliated with, endorsed by, or sponsored by Indeed. "Indeed" is a trademark of its owner.
