---
name: Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis API
description: Call GET /api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1 for Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis through JustOneAPI with oAuthorId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_gauthor_get_author_content_hot_keywords"}}
---

# Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis

Use this focused JustOneAPI skill for kOL Content Keyword Analysis in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1`. Required non-token inputs are `oAuthorId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/gauthor/get_author_content_hot_keywords`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-gauthor-get-author-content-hot-keywords`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiGauthorGetAuthorContentHotKeywordsV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1` | KOL Content Keyword Analysis |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `oAuthorId` | `query` | all | n/a | `string` | Author's unique ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiGauthorGetAuthorContentHotKeywordsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiGauthorGetAuthorContentHotKeywordsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiGauthorGetAuthorContentHotKeywordsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oAuthorId":"<oAuthorId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gauthor_get_author_content_hot_keywords&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gauthor_get_author_content_hot_keywords&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiGauthorGetAuthorContentHotKeywordsV1` on `/api/douyin-xingtu/gw/api/gauthor/get_author_content_hot_keywords/v1`.
- Echo the required lookup scope (`oAuthorId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
