---
name: Google SERP Patents Search API
description: Call GET /api/v1/google/patents/search for Google SERP Patents Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_patents_search"}}
---

# Google SERP Patents Search

Use this focused Just Serp API skill for Google SERP Patents Search. It targets `GET /api/v1/google/patents/search`. Required inputs are `query`. OpenAPI describes it as: Get Google patent Search data, including filters, for patent discovery and portfolio monitoring.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `patents/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-patents-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `patentSearch` | `v1` | `GET` | `/api/v1/google/patents/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `after` | `query` | n/a | all | `string` | Earliest date to include. Format: 'type:YYYYMMDD' (e.g., 'filing:20200101') |
| `assignee` | `query` | n/a | all | `string` | Filter by patent assignee(s). Multiple values can be comma-separated |
| `before` | `query` | n/a | all | `string` | Latest date to include. Format: 'type:YYYYMMDD' (e.g., 'publication:20230101') |
| `clustered` | `query` | n/a | all | `boolean` | If set to true, results will be grouped by classification |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `dups` | `query` | n/a | all | `string` | Deduplication method. Supported values: 'language' (by Publication) |
| `inventor` | `query` | n/a | all | `string` | Filter by patent inventor(s). Multiple values can be comma-separated |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `litigation` | `query` | n/a | all | `string` | Filter by litigation status. Supported values: 'YES', 'NO' |
| `num` | `query` | n/a | all | `integer` | The number of results to return per page (range: 1-100) |
| `page` | `query` | n/a | all | `integer` | The results page number. Use 0 for the first page, 1 for the second, and so on |
| `patents` | `query` | n/a | all | `boolean` | Whether to include Google Patents results |
| `query` | `query` | all | n/a | `string` | The search query for patents (e.g., 'autonomous vehicles', 'blockchain security') |
| `scholar` | `query` | n/a | all | `boolean` | Whether to include Google Scholar results |
| `sort` | `query` | n/a | all | `string` | Sorting order for patent results. Supported values: 'new' (Newest), 'old' (Oldest) |
| `status` | `query` | n/a | all | `string` | Filter by patent status. Supported values: 'GRANT', 'APPLICATION' |
| `type` | `query` | n/a | all | `string` | Filter by patent type. Supported values: 'PATENT', 'DESIGN' |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `patentSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `patentSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "patentSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_patents_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `patentSearch` on `/api/v1/google/patents/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google patent Search data, including filters, for patent discovery and portfolio monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
