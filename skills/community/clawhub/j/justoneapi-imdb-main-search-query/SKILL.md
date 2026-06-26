---
name: IMDb Keyword Search API
description: Call GET /api/imdb/main-search-query/v1 for IMDb Keyword Search through JustOneAPI with searchTerm.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_imdb_main_search_query"}}
---

# IMDb Keyword Search

Use this focused JustOneAPI skill for keyword Search in IMDb. It targets `GET /api/imdb/main-search-query/v1`. Required non-token inputs are `searchTerm`. OpenAPI describes it as: Get IMDb keyword Search data, including matched results, metadata, and ranking signals, for entity discovery and entertainment research.

## Endpoint Scope

- Platform key: `imdb`
- Endpoint key: `main-search-query`
- Platform family: IMDb
- Skill slug: `justoneapi-imdb-main-search-query`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `mainSearchQuery` | `v1` | `GET` | `/api/imdb/main-search-query/v1` | Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `languageCountry` | `query` | n/a | all | `string` | Language and country preferences. Available Values: - `en_US`: English (US) - `fr_CA`: French (Canada) - `fr_FR`: French (France) - `de_DE`: German (Germany) - `hi_IN`: Hindi (India) - `it_IT`: Italian (Italy) - `pt_BR`: Portuguese (Brazil) - `es_ES`: Spanish (Spain) - `es_US`: Spanish (US) - `es_MX`: Spanish (Mexico) |
| `languageCountry` enum | values | n/a | n/a | n/a | `de_DE`, `en_US`, `es_ES`, `es_MX`, `es_US`, `fr_CA`, `fr_FR`, `hi_IN`, `it_IT`, `pt_BR` |
| `limit` | `query` | n/a | all | `integer` | Maximum number of results to return (1-300) |
| `searchTerm` | `query` | all | n/a | `string` | The term to search for (e.g., 'fire') |
| `type` | `query` | n/a | all | `string` | Category of results to include in search. Available Values: - `Top`: Top Results - `Movies`: Movies - `Shows`: TV Shows - `People`: People - `Interests`: Interests - `Episodes`: Episodes - `Podcast`: Podcasts - `Video_games`: Video Games |
| `type` enum | values | n/a | n/a | n/a | `Episodes`, `Interests`, `Movies`, `People`, `Podcast`, `Shows`, `Top`, `Video_games` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `mainSearchQuery` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `mainSearchQuery`.

```bash
node {baseDir}/bin/run.mjs --operation "mainSearchQuery" --token "$JUST_ONE_API_TOKEN" --params-json '{"searchTerm":"<searchTerm>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_main_search_query&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_main_search_query&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `mainSearchQuery` on `/api/imdb/main-search-query/v1`.
- Echo the required lookup scope (`searchTerm`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get IMDb keyword Search data, including matched results, metadata, and ranking signals, for entity discovery and entertainment research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
