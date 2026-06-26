---
name: Toutiao Search API
description: Call 2 search versions for Toutiao App Keyword Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_toutiao_search"}}
---

# Toutiao Search

Use this focused JustOneAPI skill for app Keyword Search and web Keyword Search in Toutiao. It targets 2 versioned paths under `/api/toutiao/search`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Toutiao app Keyword Search data, including matching articles, videos, and authors, for topic discovery and monitoring.

## Endpoint Scope

- Platform key: `toutiao`
- Endpoint key: `search`
- Platform family: Toutiao
- Skill slug: `justoneapi-toutiao-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchToutiaoV1` | `v1` | `GET` | `/api/toutiao/search/v1` | App Keyword Search |
| `searchV2` | `v2` | `GET` | `/api/toutiao/search/v2` | Web Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keyword or query |
| `page` | `query` | n/a | `searchToutiaoV1` | `integer` | Page number for pagination |
| `searchId` | `query` | n/a | `searchToutiaoV1` | `string` | Search session ID for consistent pagination (not required for the first page) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 2 endpoint versions because their paths share `search` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `searchToutiaoV1` (`v1`): required inputs `keyword`.
- `searchV2` (`v2`): required inputs `keyword`.

## Run This Endpoint

Supported operation IDs in this skill: `searchToutiaoV1`, `searchV2`.

```bash
node {baseDir}/bin/run.mjs --operation "searchToutiaoV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_search&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchToutiaoV1` on `/api/toutiao/search/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Toutiao app Keyword Search data, including matching articles, videos, and authors, for topic discovery and monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
