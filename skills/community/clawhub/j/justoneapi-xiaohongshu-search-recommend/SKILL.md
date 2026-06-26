---
name: Xiaohongshu (RedNote) Keyword Suggestions API
description: Call GET /api/xiaohongshu/search-recommend/v1 for Xiaohongshu (RedNote) Keyword Suggestions through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_search_recommend"}}
---

# Xiaohongshu (RedNote) Keyword Suggestions

Use this focused JustOneAPI skill for keyword Suggestions in Xiaohongshu (RedNote). It targets `GET /api/xiaohongshu/search-recommend/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Xiaohongshu (RedNote) keyword Suggestions data, including suggested queries, keyword variants, and query metadata, for expanding keyword sets for content research and seo/pseo workflows and improving search coverage by using platform-recommended terms.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `search-recommend`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-search-recommend`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchRecommendV1` | `v1` | `GET` | `/api/xiaohongshu/search-recommend/v1` | Keyword Suggestions |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keyword |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchRecommendV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchRecommendV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchRecommendV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_recommend&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_recommend&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchRecommendV1` on `/api/xiaohongshu/search-recommend/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) keyword Suggestions data, including suggested queries, keyword variants, and query metadata, for expanding keyword sets for content research and seo/pseo workflows and improving search coverage by using platform-recommended terms.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
