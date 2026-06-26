---
name: Social Media Cross-Platform Search API
description: Call GET /api/search/v1 for Social Media Cross-Platform Search through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_search_v1"}}
---

# Social Media Cross-Platform Search

Use this focused JustOneAPI skill for cross-Platform Search in Social Media. It targets `GET /api/search/v1`. It has no required non-token parameters. OpenAPI describes it as: Get cross-platform social media search data, including Xiaohongshu, Douyin, Kuaishou, WeChat, Bilibili, Weibo and Zhihu results, for trend research and monitoring.

## Endpoint Scope

- Platform key: `search`
- Endpoint key: `v1`
- Platform family: Social Media
- Skill slug: `justoneapi-search-v1`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchCrossPlatformV1` | `v1` | `GET` | `/api/search/v1` | Cross-Platform Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `end` | `query` | n/a | all | `string` | End time of the search period (yyyy-MM-dd HH:mm:ss). Required for initial request |
| `keyword` | `query` | n/a | all | `string` | Search query string. Supports: - Multiple keywords (AND): keyword1 keyword2 - Multiple keywords (OR): keyword1~keyword2 - Excluded keywords (NOT): required_keyword -excluded_keyword |
| `nextCursor` | `query` | n/a | all | `string` | Pagination cursor provided by the 'nextCursor' field in the previous response |
| `source` | `query` | n/a | all | `string` | Target social media platform for search filtering. Available Values: - `ALL`: All platforms - `NEWS`: News - `WEIBO`: Sina Weibo - `WEIXIN`: Weixin (WeChat) - `ZHIHU`: Zhihu - `DOUYIN`: Douyin (TikTok China) - `XIAOHONGSHU`: Xiaohongshu (Little Red Book) - `BILIBILI`: Bilibili - `KUAISHOU`: Kuaishou |
| `source` enum | values | n/a | n/a | n/a | `ALL`, `BILIBILI`, `DOUYIN`, `KUAISHOU`, `NEWS`, `WEIBO`, `WEIXIN`, `XIAOHONGSHU`, `ZHIHU` |
| `start` | `query` | n/a | all | `string` | Start time of the search period (yyyy-MM-dd HH:mm:ss). Required for initial request |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchCrossPlatformV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchCrossPlatformV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchCrossPlatformV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search_v1&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search_v1&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchCrossPlatformV1` on `/api/search/v1`.
- Prioritize fields that support this endpoint purpose: Get cross-platform social media search data, including Xiaohongshu, Douyin, Kuaishou, WeChat, Bilibili, Weibo and Zhihu results, for trend research and monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
