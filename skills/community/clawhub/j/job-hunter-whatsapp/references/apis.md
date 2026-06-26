# Job APIs Reference

## Free — No Auth Required

### LinkedIn Guest API (Best for country-specific jobs)

Endpoint: `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search`

Parameters:
- `keywords` — URL-encoded search (e.g., `%22senior+ios+engineer%22`)
- `location` — City or country (e.g., `India`, `Hyderabad`, `Bangalore`)
- `start` — Pagination offset (0, 25, 50...)
- `f_TPR` — Time filter: `r86400` (24h), `r604800` (week), `r2592000` (month)
- `f_E` — Experience level: `4` (Mid-Senior), `5` (Director)

Response: HTML. Parse with regex:
- Titles: `base-search-card__title">\s*(.*?)\s*<`
- Companies: `base-search-card__subtitle">\s*<a[^>]*>\s*(.*?)\s*</a`
- Locations: `job-search-card__location">\s*(.*?)\s*<`
- Links: `href="(https://in\.linkedin\.com/jobs/view/[^"?]+)` (adjust country prefix)

To read full JD, fetch the job URL and extract:
- Description: regex `description__text--rich">(.*?)</section` (singleline), then strip HTML tags
- Criteria: `job-criteria-text--criteria">\s*(.*?)\s*<`

**Requires User-Agent header.** No rate limit documented but be gentle (~5-10 calls/day).

### Jobicy

Endpoint: `https://jobicy.com/api/v2/remote-jobs`

Parameters:
- `count` — Results per page (max 50)
- `tag` — Job tag (e.g., `ios`, `swift`, `mobile-developer`)
- `geo` — Country code (optional)

Response: JSON `{ jobs: [{ id, url, jobTitle, companyName, jobGeo, annualSalaryMin, annualSalaryMax, ... }] }`

No auth. No documented rate limit.

### RemoteOK

Endpoint: `https://remoteok.com/api`

Parameters:
- `tag` — Job tag (e.g., `ios`, `swift`, `mobile`)

Response: JSON array. First element is metadata, rest are jobs:
`[{}, { id, url, position, company, location, salary_min, salary_max, tags[], ... }]`

**Requires User-Agent header** or returns 403. No auth. Be gentle.

### Remotive

Endpoint: `https://remotive.com/api/remote-jobs`

Parameters:
- `category` — e.g., `software-dev`
- `search` — keyword (e.g., `ios`)
- `limit` — max results

Response: JSON `{ jobs: [{ id, url, title, company_name, candidate_required_location, salary, tags[], ... }] }`

No auth. No documented rate limit.

## Free — API Key Required

### Adzuna (Country-specific job search)

Register: https://developer.adzuna.com (free tier)

Endpoint: `https://api.adzuna.com/v1/api/jobs/{country}/search/{page}`

Country codes: `in` (India), `us`, `gb`, `ca`, `au`, `de`, etc.

Parameters:
- `app_id` — Application ID
- `app_key` — Application key
- `results_per_page` — Max 50
- `what` — Search keywords (e.g., `senior ios engineer`)
- `where` — Location (e.g., `hyderabad`, `bangalore`)
- `max_days_old` — Filter by recency

Response: JSON `{ count, results: [{ title, company: { display_name }, location: { display_name }, redirect_url, salary_min, salary_max, ... }] }`

**Rate limit: ~250 calls/month free tier. Budget 4 calls/day.**

### JSearch (RapidAPI)

Subscribe: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch (Basic Free plan)

#### Job Search
Endpoint: `https://jsearch.p.rapidapi.com/search`

Headers:
- `x-rapidapi-key` — Your RapidAPI key
- `x-rapidapi-host` — `jsearch.p.rapidapi.com`

Parameters:
- `query` — Search string (e.g., `senior ios engineer india`)
- `page` — Page number
- `num_pages` — Pages to return
- `date_posted` — `all`, `today`, `3days`, `week`, `month`
- `country` — Country code (optional)

Response: JSON `{ status, data: [{ job_title, employer_name, job_city, job_state, job_country, job_apply_link, job_description, job_min_salary, job_max_salary, job_highlights: { Qualifications[], Responsibilities[] }, ... }] }`

#### Salary Estimation
Endpoint: `https://jsearch.p.rapidapi.com/estimated-salary`

Parameters:
- `job_title` — e.g., `senior ios engineer`
- `location` — e.g., `hyderabad india`
- `radius` — Search radius (100 = wide)

Response: JSON `{ data: [{ job_title, min_salary, max_salary, median_salary, salary_currency, salary_period }] }`

**Rate limit: 200 calls/month free tier. Budget 2 calls/day. API can be slow (20s+ timeout).**
