---
name: Douyin Creator Marketplace (Xingtu) Creator Profile API
description: Call GET /api/douyin-xingtu/gw/api/author/get_author_base_info/v1 for Douyin Creator Marketplace (Xingtu) Creator Profile through JustOneAPI with oAuthorId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_author_get_author_base_info"}}
---

# Douyin Creator Marketplace (Xingtu) Creator Profile

Use this focused JustOneAPI skill for creator Profile in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/author/get_author_base_info/v1`. Required non-token inputs are `oAuthorId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/author/get_author_base_info`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-author-get-author-base-info`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiAuthorGetAuthorBaseInfoV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/author/get_author_base_info/v1` | Creator Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `oAuthorId` | `query` | all | n/a | `string` | Author's unique ID |
| `platform` | `query` | n/a | all | `string` | Platform type. Available Values: - `SHORT_VIDEO`: Short video - `LIVE_STREAMING`: Live streaming - `PICTURE_TEXT`: Picture and text - `SHORT_DRAMA`: Short drama |
| `platform` enum | values | n/a | n/a | n/a | `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA`, `SHORT_VIDEO` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiAuthorGetAuthorBaseInfoV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiAuthorGetAuthorBaseInfoV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiAuthorGetAuthorBaseInfoV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oAuthorId":"<oAuthorId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_base_info&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_author_get_author_base_info&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiAuthorGetAuthorBaseInfoV1` on `/api/douyin-xingtu/gw/api/author/get_author_base_info/v1`.
- Echo the required lookup scope (`oAuthorId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
