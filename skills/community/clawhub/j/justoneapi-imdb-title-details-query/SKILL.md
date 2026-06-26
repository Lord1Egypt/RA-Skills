---
name: IMDb Details API
description: Call GET /api/imdb/title-details-query/v1 for IMDb Details through JustOneAPI with id.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_imdb_title_details_query"}}
---

# IMDb Details

Use this focused JustOneAPI skill for details in IMDb. It targets `GET /api/imdb/title-details-query/v1`. Required non-token inputs are `id`. OpenAPI describes it as: Get IMDb title Details data, including metadata, release info, and cast, for deep title research and catalog enrichment.

## Endpoint Scope

- Platform key: `imdb`
- Endpoint key: `title-details-query`
- Platform family: IMDb
- Skill slug: `justoneapi-imdb-title-details-query`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `titleDetailsQuery` | `v1` | `GET` | `/api/imdb/title-details-query/v1` | Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `query` | all | n/a | `string` | The unique IMDb ID of the title (e.g., tt12037194) |
| `languageCountry` | `query` | n/a | all | `string` | Language and country preferences. Available Values: - `en_US`: English (US) - `fr_CA`: French (Canada) - `fr_FR`: French (France) - `de_DE`: German (Germany) - `hi_IN`: Hindi (India) - `it_IT`: Italian (Italy) - `pt_BR`: Portuguese (Brazil) - `es_ES`: Spanish (Spain) - `es_US`: Spanish (US) - `es_MX`: Spanish (Mexico) |
| `languageCountry` enum | values | n/a | n/a | n/a | `de_DE`, `en_US`, `es_ES`, `es_MX`, `es_US`, `fr_CA`, `fr_FR`, `hi_IN`, `it_IT`, `pt_BR` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `titleDetailsQuery` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `titleDetailsQuery`.

```bash
node {baseDir}/bin/run.mjs --operation "titleDetailsQuery" --token "$JUST_ONE_API_TOKEN" --params-json '{"id":"<id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_details_query&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_details_query&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `titleDetailsQuery` on `/api/imdb/title-details-query/v1`.
- Echo the required lookup scope (`id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get IMDb title Details data, including metadata, release info, and cast, for deep title research and catalog enrichment.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
