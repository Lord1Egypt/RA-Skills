---
name: Zhihu Keyword Search API
description: Call GET /api/zhihu/search/v1 for Zhihu Keyword Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_zhihu_search"}}
---

# Zhihu Keyword Search

Use this focused JustOneAPI skill for keyword Search in Zhihu. It targets `GET /api/zhihu/search/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Zhihu keyword Search data, including matched results, metadata, and ranking signals, for topic discovery and content research.

## Endpoint Scope

- Platform key: `zhihu`
- Endpoint key: `search`
- Platform family: Zhihu
- Skill slug: `justoneapi-zhihu-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchZhihuV1` | `v1` | `GET` | `/api/zhihu/search/v1` | Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keywords |
| `offset` | `query` | n/a | all | `integer` | Start offset, begins with 0 |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchZhihuV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchZhihuV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchZhihuV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_search&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchZhihuV1` on `/api/zhihu/search/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Zhihu keyword Search data, including matched results, metadata, and ranking signals, for topic discovery and content research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
