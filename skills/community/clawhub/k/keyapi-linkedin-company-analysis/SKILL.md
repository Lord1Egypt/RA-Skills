---
name: keyapi-linkedin-company-analysis
description: Explore and analyze LinkedIn companies — retrieve company profiles, employee directories, published posts, job listings with rich filters, job counts, and individual job details.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"🏢"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-linkedin-company-analysis

> Explore and analyze LinkedIn companies — from company profiles and employee directories to job market intelligence and content activity.

This skill provides comprehensive LinkedIn company intelligence using the KeyAPI MCP service. It enables retrieval of company profiles, employee lists, published posts, job listings with advanced filtering, job counts, and individual job details — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve a company's full LinkedIn profile including size, industry, and description
- Browse a company's employee directory for talent mapping or org research
- Analyze a company's published content and thought leadership activity
- Discover open job listings with filters for role type, experience level, and location
- Track job posting volume as a proxy for company growth or hiring momentum
- Retrieve detailed job descriptions including requirements and responsibilities

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **KEYAPI_TOKEN** | A valid API token from [keyapi.ai](https://keyapi.ai/). Register at the site to obtain your free token. Set it as an environment variable: `export KEYAPI_TOKEN=your_token_here` |
| **Node.js** | v18 or higher |
| **Dependencies** | Run `npm install` in the skill directory to install `@modelcontextprotocol/sdk` |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## MCP Server Configuration

All tool calls in this skill target the KeyAPI LinkedIn MCP server:

```
Server URL : https://mcp.keyapi.ai/linkedin/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform linkedin --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Company profile, size, industry, description | `get_company_profile` | Company overview, competitive profiling |
| Employee directory and headcount | `get_company_people` | Org mapping, talent research, key contact discovery |
| Company-published posts and content | `get_company_posts` | Content strategy analysis, brand voice audit |
| Open job listings with filters | `get_company_jobs` | Hiring intelligence, role availability, talent demand signals |
| Total active job count | `get_company_job_count` | Growth proxy, hiring velocity tracking |
| Individual job description and requirements | `get_job_detail` | Role qualification analysis, JD benchmarking |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Company overview**: Use `get_company_profile` with `company` (name) or `company_id`.
- **Hiring intelligence**: Use `get_company_jobs` with filters, then `get_job_detail` for specific roles.
- **Growth signals**: Use `get_company_job_count` to track hiring volume over time.
- **Content audit**: Use `get_company_posts` with `sort_by: "recent"` or `"top"`.
- **Org research**: Use `get_company_people` to browse the employee directory.

> **Company Identifier: `company` vs. `company_id`**
>
> `get_company_profile` accepts either:
> - `company` — the company's URL slug (e.g., `rapidapi` from `https://www.linkedin.com/company/rapidapi`). Resolves in a single request.
> - `company_id` — the numeric internal ID. Using `company_id` costs 1 additional internal request.
>
> All other company nodes (`get_company_people`, `get_company_posts`, `get_company_jobs`, `get_company_job_count`) require `company_id`. **Call `get_company_profile` first** with the `company` slug to obtain the `company_id`.

> **`get_job_detail` Identifier**
>
> `get_job_detail` requires a `job_id` — the numeric ID found in the job listing URL (e.g., `https://www.linkedin.com/jobs/view/1234567890` → `job_id: "1234567890"`). Obtain it from `get_company_jobs` response data.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available filter options:

```bash
node scripts/run.js --platform linkedin --schema <tool_name>

# Examples
node scripts/run.js --platform linkedin --schema get_company_profile
node scripts/run.js --platform linkedin --schema get_company_jobs
node scripts/run.js --platform linkedin --schema get_job_detail
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform linkedin --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform linkedin --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get company profile by slug:**

```bash
node scripts/run.js --platform linkedin --tool get_company_profile \
  --params '{"company":"openai"}' --pretty
```

**Example — get company jobs with filters:**

```bash
node scripts/run.js --platform linkedin --tool get_company_jobs \
  --params '{"company_id":"783611","experience_level":"mid_senior","remote":"remote","job_type":"full_time","page":1}' --pretty
```

**Example — get job detail with skills:**

```bash
node scripts/run.js --platform linkedin --tool get_job_detail \
  --params '{"job_id":"1234567890","include_skills":true}' --pretty
```

**Example — get company posts sorted by recent:**

```bash
node scripts/run.js --platform linkedin --tool get_company_posts \
  --params '{"company_id":"10649600","sort_by":"recent","page":1}' --pretty
```

**Pagination:**

| Endpoint | Pagination parameter | Notes |
|---|---|---|
| `get_company_people`, `get_company_posts`, `get_company_jobs` | `page` (int, 1-indexed) | Increment page to fetch subsequent results |
| `get_company_profile`, `get_company_job_count`, `get_job_detail` | — | Single-call response |

**`get_company_jobs` filter reference:**

| Parameter | Options | Description |
|---|---|---|
| `sort_by` | `recent`, `relevant` | Sort order for job listings |
| `date_posted` | `anytime`, `past_month`, `past_week`, `past_24_hours` | Recency filter |
| `experience_level` | `internship`, `entry_level`, `associate`, `mid_senior`, `director`, `executive` | Seniority filter |
| `remote` | `onsite`, `remote`, `hybrid` | Work location type |
| `job_type` | `full_time`, `part_time`, `contract`, `temporary`, `volunteer`, `internship`, `other` | Employment type |
| `easy_apply` | boolean string | Filter for LinkedIn Easy Apply jobs |
| `under_10_applicants` | boolean string | Filter for low-competition roles |
| `fair_chance_employer` | boolean string | Filter for fair chance employers |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_company_profile/
    │   └── {params_hash}.json
    ├── get_company_people/
    │   └── {params_hash}.json
    ├── get_company_posts/
    │   └── {params_hash}.json
    ├── get_company_jobs/
    │   └── {params_hash}.json
    ├── get_company_job_count/
    │   └── {params_hash}.json
    └── get_job_detail/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured company intelligence report:

1. **Company Overview** — Name, industry, company size, headquarters, founding year, description, LinkedIn follower count.
2. **People & Org Structure** — Employee count, key roles identified, department distribution (where available).
3. **Content Activity** — Post frequency, top-performing content, engagement patterns, brand messaging themes.
4. **Hiring Intelligence** — Open role count, role distribution by function and seniority, remote vs. onsite ratio, hiring velocity signals.
5. **Job Market Signals** — Roles with fewer than 10 applicants (opportunity windows), easy-apply availability, date-posted distribution.
6. **Actionable Insights** — Growth indicators, talent demand patterns, competitive positioning signals.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Company ID resolution** | `get_company_people`, `get_company_posts`, `get_company_jobs`, `get_company_job_count` all require `company_id`. Call `get_company_profile` first with the `company` slug to obtain it. |
| **`get_company_profile` identifier** | Pass `company` (URL slug) for a single-request lookup. `company_id` is also accepted but costs 1 additional internal request. |
| **`get_job_detail` ID source** | Extract `job_id` from the job listing URL or from `get_company_jobs` response data. |
| **`get_company_posts` sort** | Use `sort_by: "top"` for highest-engagement posts; `sort_by: "recent"` for latest activity. |
| **Pagination** | All list endpoints use `page` (1-indexed). No pagination token required. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request up to 3 times with a 2–3 second pause between attempts before reporting the error. |
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; ensure `company_id` is provided where required |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — company or job may not exist | Verify the company slug or `company_id`; confirm the job listing is still active |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
