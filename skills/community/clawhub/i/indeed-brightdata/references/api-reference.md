# Bright Data Indeed API Reference

## Authentication

All requests use Bearer token authentication:
```
Authorization: Bearer <BRIGHTDATA_API_KEY>
```
API key from: https://brightdata.com/cp/setting/users

## Base Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| POST | `https://api.brightdata.com/datasets/v3/scrape?dataset_id=<ID>` | Sync — up to ~20 inputs, returns data inline |
| POST | `https://api.brightdata.com/datasets/v3/trigger?dataset_id=<ID>` | Async batch — returns `snapshot_id` |
| GET | `https://api.brightdata.com/datasets/v3/progress/<snapshot_id>` | Poll batch status (`running` / `ready`) |
| GET | `https://api.brightdata.com/datasets/v3/snapshot/<snapshot_id>?format=json` | Fetch completed batch data |
| GET | `https://api.brightdata.com/datasets/list` | List available dataset IDs |

## Query Parameters

### Common (all endpoints)

| Param | Type | Description |
|-------|------|-------------|
| `dataset_id` | string | Required. The scraper dataset ID |
| `format` | string | Response format: `json` (default), `csv`, `ndjson` |
| `uncompressed_webhook` | boolean | If true, webhook data is uncompressed |
| `limit_per_input` | integer | Max results per input URL/keyword |
| `limit_multiple_results` | integer | Max total results across all inputs |
| `include_errors` | boolean | Include error records in output |

### Discovery-specific (added to trigger URL)

| Param | Type | Description |
|-------|------|-------------|
| `type` | string | `discover_new` for discovery mode |
| `discover_by` | string | `keyword`, `url`, or `industry_and_state` |

## Dataset IDs

### Jobs
- **Dataset ID**: `gd_l4dx9j9sscpvs7no2`
- Used for all job endpoints (collect and discover)

### Companies
- Dataset IDs must be discovered via `GET /datasets/list`
- Use `indeed_list_datasets.sh` to find them
- Store discovered IDs in `~/.config/indeed-brightdata/datasets.json`

## Job Endpoints

### 1. Jobs — Collect by URL

Collect detailed job data from specific Indeed job URLs.

**Request:**
```json
[{"url": "https://www.indeed.com/viewjob?jk=abc123"}]
```

**Endpoint:** `POST /scrape?dataset_id=gd_l4dx9j9sscpvs7no2`

### 2. Jobs — Discover by Keyword

Search for jobs by keyword, country, and location.

**Request:**
```json
[{
  "keyword_search": "software engineer",
  "country": "US",
  "domain": "indeed.com",
  "location": "Austin, TX",
  "date_posted": "Last 7 days",
  "pay": "$50,000+",
  "location_radius": "25"
}]
```

**Endpoint:** `POST /trigger?dataset_id=gd_l4dx9j9sscpvs7no2&type=discover_new&discover_by=keyword`

**Optional fields:** `date_posted`, `posted_by`, `pay`, `location_radius`

### 3. Jobs — Discover by URL

Discover jobs from a company's Indeed jobs page.

**Request:**
```json
[{"url": "https://www.indeed.com/cmp/Google/jobs"}]
```

**Endpoint:** `POST /trigger?dataset_id=gd_l4dx9j9sscpvs7no2&type=discover_new&discover_by=url`

## Company Endpoints

### 4. Companies — Collect by URL

Collect company info from an Indeed company page.

**Request:**
```json
[{"url": "https://www.indeed.com/cmp/Google"}]
```

**Endpoint:** `POST /scrape?dataset_id=<COMPANY_DATASET_ID>`

### 5. Companies — Discover by Company List

Discover companies from a browse-companies page.

**Request:**
```json
[{"url": "https://www.indeed.com/companies/browse-companies"}]
```

**Endpoint:** `POST /trigger?dataset_id=<COMPANY_DATASET_ID>&type=discover_new&discover_by=url`

### 6. Companies — Discover by Industry & State

**Request:**
```json
[{"industry": "Technology", "state": "Texas"}]
```

**Endpoint:** `POST /trigger?dataset_id=<COMPANY_DATASET_ID>&type=discover_new&discover_by=industry_and_state`

### 7. Companies — Discover by Keyword

**Request:**
```json
[{"keyword": "Tesla"}]
```

**Endpoint:** `POST /trigger?dataset_id=<COMPANY_DATASET_ID>&type=discover_new&discover_by=keyword`

## Response Schema — Job Listings

| Field | Type | Description |
|-------|------|-------------|
| `jobid` | string | Indeed job ID |
| `company_name` | string | Employer name |
| `job_title` | string | Position title |
| `description_text` | string | Plain text job description |
| `benefits` | array | List of benefits |
| `qualifications` | array | Required qualifications |
| `job_type` | string | Full-time, Part-time, Contract, etc. |
| `location` | string | Job location |
| `salary_formatted` | string | Salary display string |
| `company_rating` | number | Company rating (1-5) |
| `company_reviews_count` | integer | Number of reviews |
| `country` | string | Country code |
| `date_posted` | string | Relative date ("3 days ago") |
| `date_posted_parsed` | string | ISO date |
| `region` | string | State/region |
| `company_link` | string | Indeed company page URL |
| `company_website` | string | Company's own website |
| `domain` | string | Indeed domain used |
| `apply_link` | string | Direct apply URL |
| `url` | string | Indeed job listing URL |
| `is_expired` | boolean | Whether listing has expired |
| `job_location` | object | Structured location data |
| `logo_url` | string | Company logo URL |
| `shift_schedule` | array | Shift/schedule details |
| `job_description_formatted` | string | HTML formatted description |

## Response Schema — Company Info

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Company name |
| `description` | string | Company description |
| `url` | string | Indeed company page URL |
| `website` | string | Company website |
| `industry` | string | Industry category |
| `company_size` | string | Employee count range |
| `revenue` | string | Revenue range |
| `logo` | string | Logo URL |
| `headquarters` | string | HQ location |
| `country_code` | string | Country code |
| `details` | array | Additional company details |
| `related_companies` | array | Similar companies |
| `benefits` | array | Employee benefits |
| `salaries` | object | `{count, link}` |
| `reviews` | object | `{count, url}` |
| `company_id` | string | Indeed company ID |
| `jobs_count` | integer | Number of open positions |
| `overall_rating` | number | Overall rating (1-5) |
| `q&a_count` | integer | Q&A count |
| `interviews_count` | integer | Interview reviews count |
| `photos_count` | integer | Photos count |

## Country / Domain Mapping

| Country | Domain | Code |
|---------|--------|------|
| United States | indeed.com | US |
| United Kingdom | uk.indeed.com | GB |
| Canada | ca.indeed.com | CA |
| Australia | au.indeed.com | AU |
| India | in.indeed.com | IN |
| Germany | de.indeed.com | DE |
| France | fr.indeed.com | FR |
| Japan | jp.indeed.com | JP |
| Brazil | br.indeed.com | BR |
| Mexico | mx.indeed.com | MX |

## Valid `date_posted` Values

- `Last 24 hours`
- `Last 3 days`
- `Last 7 days`
- `Last 14 days`

## Rate Limits

- Synchronous (`/scrape`): Up to 1,000 concurrent requests
- Async batch (`/trigger`): Up to 100 concurrent requests
- HTTP 429: Rate limit exceeded — back off and retry
- Discovery scrapers automatically use batch mode

## Error Responses

| HTTP Status | Meaning |
|-------------|---------|
| 200 | Success |
| 401 | Invalid or missing API key |
| 404 | Invalid dataset_id or snapshot_id |
| 429 | Rate limit exceeded |
| 500 | Bright Data server error |

Error response body:
```json
{"error": "description of the error"}
```
