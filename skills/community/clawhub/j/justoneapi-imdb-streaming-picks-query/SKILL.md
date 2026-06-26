---
name: IMDb Streaming Picks API
description: Call GET /api/imdb/streaming-picks-query/v1 for IMDb Streaming Picks through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_imdb_streaming_picks_query"}}
---

# IMDb Streaming Picks

Use this focused JustOneAPI skill for streaming Picks in IMDb. It targets `GET /api/imdb/streaming-picks-query/v1`. It has no required non-token parameters. OpenAPI describes it as: Get IMDb streaming Picks data, including curated titles available across streaming surfaces, for content discovery and watchlist research.

## Endpoint Scope

- Platform key: `imdb`
- Endpoint key: `streaming-picks-query`
- Platform family: IMDb
- Skill slug: `justoneapi-imdb-streaming-picks-query`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `streamingPicksQuery` | `v1` | `GET` | `/api/imdb/streaming-picks-query/v1` | Streaming Picks |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `languageCountry` | `query` | n/a | all | `string` | Language and country preferences. Available Values: - `en_US`: English (US) - `fr_CA`: French (Canada) - `fr_FR`: French (France) - `de_DE`: German (Germany) - `hi_IN`: Hindi (India) - `it_IT`: Italian (Italy) - `pt_BR`: Portuguese (Brazil) - `es_ES`: Spanish (Spain) - `es_US`: Spanish (US) - `es_MX`: Spanish (Mexico) |
| `languageCountry` enum | values | n/a | n/a | n/a | `de_DE`, `en_US`, `es_ES`, `es_MX`, `es_US`, `fr_CA`, `fr_FR`, `hi_IN`, `it_IT`, `pt_BR` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `streamingPicksQuery` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `streamingPicksQuery`.

```bash
node {baseDir}/bin/run.mjs --operation "streamingPicksQuery" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_streaming_picks_query&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_streaming_picks_query&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `streamingPicksQuery` on `/api/imdb/streaming-picks-query/v1`.
- Prioritize fields that support this endpoint purpose: Get IMDb streaming Picks data, including curated titles available across streaming surfaces, for content discovery and watchlist research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
