---
name: IMDb News by Category API
description: Call GET /api/imdb/news-by-category-query/v1 for IMDb News by Category through JustOneAPI with category.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_imdb_news_by_category_query"}}
---

# IMDb News by Category

Use this focused JustOneAPI skill for news by Category in IMDb. It targets `GET /api/imdb/news-by-category-query/v1`. Required non-token inputs are `category`. OpenAPI describes it as: Get IMDb news by Category data, including headlines, summaries, and source metadata, for media monitoring and news research.

## Endpoint Scope

- Platform key: `imdb`
- Endpoint key: `news-by-category-query`
- Platform family: IMDb
- Skill slug: `justoneapi-imdb-news-by-category-query`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `newsByCategoryQuery` | `v1` | `GET` | `/api/imdb/news-by-category-query/v1` | News by Category |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `category` | `query` | all | n/a | `string` | News category to filter by. Available Values: - `TOP`: Top News - `MOVIE`: Movie News - `TV`: TV News - `CELEBRITY`: Celebrity News |
| `category` enum | values | n/a | n/a | n/a | `CELEBRITY`, `MOVIE`, `TOP`, `TV` |
| `languageCountry` | `query` | n/a | all | `string` | Language and country preferences. Available Values: - `en_US`: English (US) - `fr_CA`: French (Canada) - `fr_FR`: French (France) - `de_DE`: German (Germany) - `hi_IN`: Hindi (India) - `it_IT`: Italian (Italy) - `pt_BR`: Portuguese (Brazil) - `es_ES`: Spanish (Spain) - `es_US`: Spanish (US) - `es_MX`: Spanish (Mexico) |
| `languageCountry` enum | values | n/a | n/a | n/a | `de_DE`, `en_US`, `es_ES`, `es_MX`, `es_US`, `fr_CA`, `fr_FR`, `hi_IN`, `it_IT`, `pt_BR` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `newsByCategoryQuery` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `newsByCategoryQuery`.

```bash
node {baseDir}/bin/run.mjs --operation "newsByCategoryQuery" --token "$JUST_ONE_API_TOKEN" --params-json '{"category":"TOP"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_news_by_category_query&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_news_by_category_query&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `newsByCategoryQuery` on `/api/imdb/news-by-category-query/v1`.
- Echo the required lookup scope (`category`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get IMDb news by Category data, including headlines, summaries, and source metadata, for media monitoring and news research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
