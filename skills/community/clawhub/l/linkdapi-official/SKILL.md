---
name: linkdapi-openclaw
description: Complete LinkdAPI integration OpenClaw skill. Includes all 50+ endpoints, Python/Node.js/Go SDKs, authentication, rate limits, and real-world examples. Use this skill whenever the user wants to look up LinkedIn profiles, search LinkedIn people or companies, enrich leads, research LinkedIn jobs, scrape LinkedIn posts or articles, do B2B prospecting, get LinkedIn company data, or call any LinkedIn data API. Always use this skill for ANY LinkedIn data task, even if the user just says "find me on LinkedIn" or "look up this company" or "search LinkedIn for engineers in Berlin".
version: 1.0.0
author: LinkdAPI Team
---

# LinkdAPI Skill — LinkedIn Data API

Use this skill to access **LinkedIn** professional data via the LinkdAPI REST API.

> Full endpoint reference with params, enums, and response schemas → `references/api-ref.md`
> Structured endpoint manifest (JSON) → `references/skills.json`

---

## ⚠️ Authentication — READ FIRST

| | Value |
|---|---|
| **Auth header** | `X-linkdapi-apikey` |
| **Base URL** | `https://linkdapi.com` |
| **Env var** | `LINKDAPI_KEY` |

```bash
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/overview?username=ryanroslansky" | jq .
```

⛔ **NEVER use `x-api-key` or `Authorization: Bearer` — they will return 401. The only correct header is `X-linkdapi-apikey`.**

---

## Core Concepts

| Term | Meaning | How to Get |
|---|---|---|
| `username` | LinkedIn vanity slug (`linkedin.com/in/USERNAME`) | From the URL |
| `urn` | Internal LinkedIn ID (`ACoAAAA...`) | From `profile/overview` response |
| `id` (company) | Numeric LinkedIn company ID | From `companies/company/info` or `companies/name-lookup` |
| `jobId` | Numeric LinkedIn job ID | From job search results |
| `geoUrn` | Location filter ID | From `geos/name-lookup` |
| `cursor` | Pagination token | From previous response |

**Always get URN first** when working with profile endpoints that require it.

---

## Endpoint Quick Reference

### Profile — `/api/v1/profile/`
| Endpoint | Params | Use |
|---|---|---|
| `overview` | `username` | Basic info + URN ← **start here** |
| `details` | `urn` | Positions, education, languages |
| `contact-info` | `username` | Email, phone, websites |
| `about` | `urn` | About section |
| `full` | `username` or `urn` | Everything in 1 request |
| `full-experience` | `urn` | Complete work history |
| `certifications` | `urn` | Certifications |
| `education` | `urn` | Education history |
| `skills` | `urn` | Skills + endorsements |
| `social-matrix` | `username` | Followers + connections |
| `recommendations` | `urn` | Given + received |
| `similar` | `urn` | Similar profiles |
| `reactions` | `urn`, `cursor` | Profile reactions |
| `interests` | `urn` | Interests |
| `services` | `urn` | Services offered |
| `username-to-urn` | `username` | Username → URN |

### Companies — `/api/v1/companies/`
| Endpoint | Params | Use |
|---|---|---|
| `name-lookup` | `query` | Search by name |
| `company/info` | `id` or `name` | Company details |
| `company/info-v2` | `id` | Extended info |
| `company/similar` | `id` | Similar companies |
| `company/employees-data` | `id` | Headcount + distribution |
| `company/affiliated-pages` | `id` | Subsidiaries |
| `company/posts` | `id`, `start` | Company posts |
| `company/universal-name-to-id` | `universalName` | Universal name → ID |
| `jobs` | `companyIDs`, `start` | Job listings |

### Jobs — `/api/v1/jobs/`
| Endpoint | Params | Use |
|---|---|---|
| `search` | `keyword`, `location`, `timePosted`, `workArrangement`, `geoId`, `companyIds`, `jobTypes`, `experience`, `salary`, `start` | V1 job search |
| `job/details` | `jobId` | Job info (open only) |
| `job/details-v2` | `jobId` | Job info (all statuses) |
| `job/similar` | `jobId` | Similar jobs |
| `job/people-also-viewed` | `jobId` | Related jobs |
| `job/hiring-team` | `jobId`, `start` | Hiring team |
| `posted-by-profile` | `profileUrn`, `start`, `count` | Jobs by a person |

### Search — `/api/v1/search/`
| Endpoint | Key Params | Use |
|---|---|---|
| `people` | `keyword`, `title`, `currentCompany`, `geoUrn`, `industry`, `firstName`, `lastName`, `start`, `count` | Find professionals |
| `companies` | `keyword`, `geoUrn`, `companySize`, `hasJobs`, `industry`, `start`, `count` | Find companies |
| `posts` | `keyword`, `sortBy`, `datePosted`, `authorJobTitle`, `fromOrganization`, `contentType`, `start` | Find posts |
| `jobs` | `keyword`, `workplaceTypes`, `datePosted`, `easyApply`, `companies`, `locations`, `experience`, `salary`, `under10Applicants`, `start`, `count` | V2 job search |
| `services` | `keyword`, `geoUrn`, `serviceCategory`, `profileLanguage`, `start`, `count` | Service providers |
| `schools` | `keyword`, `start`, `count` | Schools |

### Posts — `/api/v1/posts/`
| Endpoint | Params | Use |
|---|---|---|
| `featured` | `urn` | Featured posts |
| `all` | `urn`, `cursor`, `start` | All posts paginated |
| `info` | `urn` | Single post |
| `comments` | `urn`, `start`, `count`, `cursor` | Comments |
| `likes` | `urn`, `start` | Likes |

### Comments — `/api/v1/comments/`
| Endpoint | Params | Use |
|---|---|---|
| `all` | `urn`, `cursor` | All comments |
| `likes` | `urn`, `start` | Comment likes |

### Articles — `/api/v1/articles/`
| Endpoint | Params | Use |
|---|---|---|
| `all` | `urn`, `start` | All articles |
| `article/info` | `url` | Article details |
| `article/reactions` | `urn`, `start` | Reactions |

### Lookups
| Path | Params | Use |
|---|---|---|
| `/api/v1/geos/name-lookup` | `query` | → geoUrn for location filters |
| `/api/v1/g/title-skills-lookup` | `query` | → skill/title IDs |
| `/api/v1/g/services-lookup` | `query` | → service category IDs |

### Services — `/api/v1/services/`
| Endpoint | Params | Use |
|---|---|---|
| `service/details` | `vanityname` | Service page |
| `service/similar` | `vanityname` | Similar services |

### System
| Path | Use |
|---|---|
| `status/` | Health check (no auth) |

---

## Common Workflows

### Lead Enrichment (Profile Research)

```bash
# Step 1: Get URN
PROFILE=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/overview?username=TARGET_USERNAME")
URN=$(echo $PROFILE | jq -r '.data.urn')
echo "$(echo $PROFILE | jq -r '.data.fullName') → $URN"

# Step 2: Enrich in parallel
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/full-experience?urn=$URN" | jq '.data.experience[0]' &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/skills?urn=$URN" | jq '.data.skills[:5]' &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/contact-info?username=TARGET_USERNAME" | jq '.data' &
wait

# Or use full endpoint (one request, more credits)
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/full?username=TARGET_USERNAME" | jq .data
```

### Company Research

```bash
CO_ID=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/company/info?name=google" | jq -r '.data.id')

curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/company/employees-data?id=$CO_ID" | jq .data &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/company/similar?id=$CO_ID" | jq .data &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/jobs?companyIDs=$CO_ID&start=0" | jq .data &
wait
```

### ICP People Search

```bash
GEO_URN=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/geos/name-lookup?query=San+Francisco" | jq -r '.data[0].urn')

curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/search/people?keyword=VP+Sales&title=VP+Sales&geoUrn=$GEO_URN&start=0" \
  | jq '.data.items'
```

### Job Market Intel

```bash
# V2 (richest filters)
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/search/jobs?keyword=Software+Engineer&workplaceTypes=remote&datePosted=1week&easyApply=true" \
  | jq .data

# V1 (classic, location string)
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/jobs/search?keyword=Marketing+Manager&location=London&timePosted=1week&workArrangement=hybrid" \
  | jq .data
```

### Content Research

```bash
# Posts by a profile
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/posts/all?urn=$URN&start=0" | jq .data

# Search posts by keyword
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/search/posts?keyword=AI+marketing&sortBy=date_posted&datePosted=past-week" \
  | jq .data

# Articles
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/articles/all?urn=$URN&start=0" | jq .data
```

---

## Error Handling

All responses: `{ "success": bool, "statusCode": int, "message": string, "errors": null|string, "data": ... }`

```bash
RESULT=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/overview?username=someuser")

if echo $RESULT | jq -e '.success == true' > /dev/null 2>&1; then
  echo "OK: $(echo $RESULT | jq -r '.data.fullName')"
else
  CODE=$(echo $RESULT | jq -r '.statusCode')
  MSG=$(echo $RESULT | jq -r '.message')
  echo "Error $CODE: $MSG"
  # 401=invalid key | 404=not found | 429=rate limited (retry with backoff) | 500=server error
  [ "$CODE" = "429" ] && sleep 5 && echo "Retry after backoff"
fi
```

---

## B2B Marketing Playbook

| Goal | Endpoints |
|---|---|
| Lead enrichment | `profile/overview` → `profile/full-experience` + `profile/skills` + `profile/contact-info` |
| ICP targeting | `geos/name-lookup` → `search/people` with `title` + `currentCompany` + `geoUrn` |
| Competitor intel | `companies/company/posts` or `search/posts?fromOrganization=ID` |
| Hiring signals | `companies/jobs?companyIDs=ID` reveals growth areas |
| Content inspiration | `posts/all` on top voices + `posts/info` for engagement stats |
| Warm outreach prep | `profile/recommendations` + `posts/all` before messaging |
| Job trigger events | `jobs/posted-by-profile` to find who is hiring actively |

---

## Reference Files

- **`references/api-ref.md`** — Full parameter schemas, all enums, and response field descriptions for every endpoint. Read this when you need exact param names or response field shapes.
- **`references/skills.json`** — Machine-readable manifest of all endpoints (for dynamic tooling or integrations).
