---
name: Google SERP Jobs Search API
description: Call GET /api/v1/google/jobs/search for Google SERP Jobs Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_jobs_search"}}
---

# Google SERP Jobs Search

Use this focused Just Serp API skill for Google SERP Jobs Search. It targets `GET /api/v1/google/jobs/search`. Required inputs are `query`. OpenAPI describes it as: Get Google jobs Search data, including titles, companies, and locations, for aggregating job board results, analyzing hiring trends, and monitoring recruitment activity.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `jobs/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-jobs-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `jobsSearch` | `v1` | `GET` | `/api/v1/google/jobs/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `chips` | `query` | n/a | all | `string` | Additional search filters (chips) such as job type, date posted, etc. Use values returned in previous responses |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `lrad` | `query` | n/a | all | `string` | Search radius in miles around the specified location |
| `ltype` | `query` | n/a | all | `string` | Filter by job location type. Set to '1' for work-from-home (remote) jobs |
| `next_page_token` | `query` | n/a | all | `string` | Token for retrieving the next page of job results. Found in 'next_page_token' of a previous response |
| `query` | `query` | all | n/a | `string` | The job search query (e.g., 'software engineer', 'data scientist London') |
| `uds` | `query` | n/a | all | `string` | Advanced Google-provided filter string for job results |
| `uule` | `query` | n/a | all | `string` | Encoded location string (UULE) to localize job results to a specific geographic area |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `jobsSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `jobsSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "jobsSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_jobs_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `jobsSearch` on `/api/v1/google/jobs/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google jobs Search data, including titles, companies, and locations, for aggregating job board results, analyzing hiring trends, and monitoring recruitment activity.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
