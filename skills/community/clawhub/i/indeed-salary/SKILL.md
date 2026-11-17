---
name: indeed-salary
version: 1.0.0
description: Look up salary for an Indeed job posting via RolesAPI.com. Pass a job key or a pasted Indeed URL and get min, max, currency, period, and employer-vs-estimate provenance. One script, minimum surface area.
license: MIT-0
author: RolesAPI
homepage: https://rolesapi.com
repository: https://github.com/nikhonit/indeed-skills
tags:
  - indeed
  - jobs
  - salary
  - compensation
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

# indeed-salary

Focused salary skill. Use only when the user **explicitly asks** what a job posting pays.

## When to use this skill

**DO use when the user asks:**

- "What does this job pay?" (with an Indeed link)
- "Look up the salary for job key a1b2c3d4e5f60718"
- "Is that nurse posting's salary from the employer or an estimate?"
- "Compare pay on these three postings"

**Do NOT use when:**

- The user asks about market-wide or average salaries rather than a specific posting
- A posting appears incidentally in context
- You also need the description, company, or benefits. Use [`indeed-full`](https://github.com/nikhonit/indeed-skills/tree/main/skills/indeed-full) instead, it bundles everything in one install.

## Setup

Set `ROLESAPI_KEY` to your RolesAPI key (format `rk_live_...`). Create one at <https://rolesapi.com/app/keys>. The free plan includes 100 credits at signup, no card required.

```bash
export ROLESAPI_KEY="rk_live_..."
```

## Scripts

### `get_salary.py` (1 credit)

Accepts either a 16-character job key or a pasted Indeed viewjob URL.

```bash
python3 scripts/get_salary.py 7dcf172c8d7fc756
python3 scripts/get_salary.py "https://www.indeed.com/viewjob?jk=7dcf172c8d7fc756"
python3 scripts/get_salary.py 7dcf172c8d7fc756 --country gb
```

Real output (job key path):

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

`source` is `employer` when the figure comes from the posting itself and `estimated` when it is an Indeed estimate. Postings with no salary information omit the `salary` key.

## Pricing

| Plan | Price | Credits | Rate limit |
|---|---|---|---|
| Free | $0 | 100 (one time at signup) | 20/min |
| Monthly | $5/mo | 1,000/month | 200/min |
| Annual | $54/yr | 12,000 upfront | 300/min |

One credit per lookup. Failed calls are not charged. Full pricing: <https://rolesapi.com/pricing/>.

## Trademark

RolesAPI is an independent service and is not affiliated with, endorsed by, or sponsored by Indeed. "Indeed" is a trademark of its owner.
