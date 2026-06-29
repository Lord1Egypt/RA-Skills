---
name: Google SERP Local Search API
description: Call GET /api/v1/google/local/search for Google SERP Local Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_local_search"}}
---

# Google SERP Local Search

Use this focused Just Serp API skill for Google SERP Local Search. It targets `GET /api/v1/google/local/search`. Required inputs are `query`. OpenAPI describes it as: Get Google local Search data, including business listings, ratings, and contact details, for local lead generation and competitor research.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `local/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-local-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `localSearch` | `v1` | `GET` | `/api/v1/google/local/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `domain` | `query` | n/a | all | `string` | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a> |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `location` | `query` | n/a | all | `string` | The textual location name (e.g., 'New York, NY') to localize the search results |
| `ludocid` | `query` | n/a | all | `string` | The unique Google Business Profile listing ID (CID) to get details for a specific business |
| `page` | `query` | n/a | all | `integer` | The results page number. Use 0 for the first page, 1 for the second, and so on |
| `query` | `query` | all | n/a | `string` | The search query for local businesses (e.g., 'pizza', 'dentist near me') |
| `tbs` | `query` | n/a | all | `string` | Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty |
| `uule` | `query` | n/a | all | `string` | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `localSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `localSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "localSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_local_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `localSearch` on `/api/v1/google/local/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google local Search data, including business listings, ratings, and contact details, for local lead generation and competitor research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
