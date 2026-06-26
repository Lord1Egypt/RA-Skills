---
name: IMDb Chart Rankings API
description: Call GET /api/imdb/title-chart-rankings/v1 for IMDb Chart Rankings through JustOneAPI with rankingsChartType.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_imdb_title_chart_rankings"}}
---

# IMDb Chart Rankings

Use this focused JustOneAPI skill for chart Rankings in IMDb. It targets `GET /api/imdb/title-chart-rankings/v1`. Required non-token inputs are `rankingsChartType`. OpenAPI describes it as: Get IMDb title Chart Rankings data, including positions in lists such as Top 250 and related charts, for ranking monitoring and title benchmarking.

## Endpoint Scope

- Platform key: `imdb`
- Endpoint key: `title-chart-rankings`
- Platform family: IMDb
- Skill slug: `justoneapi-imdb-title-chart-rankings`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `titleChartRankings` | `v1` | `GET` | `/api/imdb/title-chart-rankings/v1` | Chart Rankings |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `languageCountry` | `query` | n/a | all | `string` | Language and country preferences. Available Values: - `en_US`: English (US) - `fr_CA`: French (Canada) - `fr_FR`: French (France) - `de_DE`: German (Germany) - `hi_IN`: Hindi (India) - `it_IT`: Italian (Italy) - `pt_BR`: Portuguese (Brazil) - `es_ES`: Spanish (Spain) - `es_US`: Spanish (US) - `es_MX`: Spanish (Mexico) |
| `languageCountry` enum | values | n/a | n/a | n/a | `de_DE`, `en_US`, `es_ES`, `es_MX`, `es_US`, `fr_CA`, `fr_FR`, `hi_IN`, `it_IT`, `pt_BR` |
| `rankingsChartType` | `query` | all | n/a | `string` | Type of rankings chart to retrieve. Available Values: - `TOP_250`: Top 250 Movies - `TOP_250_TV`: Top 250 TV Shows |
| `rankingsChartType` enum | values | n/a | n/a | n/a | `TOP_250`, `TOP_250_TV` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `titleChartRankings` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `titleChartRankings`.

```bash
node {baseDir}/bin/run.mjs --operation "titleChartRankings" --token "$JUST_ONE_API_TOKEN" --params-json '{"rankingsChartType":"TOP_250"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_chart_rankings&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_chart_rankings&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `titleChartRankings` on `/api/imdb/title-chart-rankings/v1`.
- Echo the required lookup scope (`rankingsChartType`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get IMDb title Chart Rankings data, including positions in lists such as Top 250 and related charts, for ranking monitoring and title benchmarking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
