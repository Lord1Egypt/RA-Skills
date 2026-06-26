---
name: Douyin Creator Marketplace (Xingtu) Creator Search API
description: Call GET /api/douyin-xingtu/gw/api/gsearch/search_for_author_square/v1 for Douyin Creator Marketplace (Xingtu) Creator Search through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_gsearch_search_for_author_square"}}
---

# Douyin Creator Marketplace (Xingtu) Creator Search

Use this focused JustOneAPI skill for creator Search in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/gsearch/search_for_author_square/v1`. It has no required non-token parameters. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/gsearch/search_for_author_square`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-gsearch-search-for-author-square`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiGsearchSearchForAuthorSquareV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/gsearch/search_for_author_square/v1` | Creator Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `contentTag` | `query` | n/a | all | `string` | Content tag filter |
| `followerRange` | `query` | n/a | all | `string` | Follower range (e.g., 10-100) |
| `keyword` | `query` | n/a | all | `string` | Search keyword |
| `kolPriceRange` | `query` | n/a | all | `string` | KOL price range (e.g., 10000-50000) |
| `kolPriceType` | `query` | n/a | all | `string` | KOL price type. Available Values: - `视频1_20s`: Video 1-20s - `视频21_60s`: Video 21-60s - `视频60s以上`: Video > 60s - `定制短剧单集`: Mini-drama episode - `千次自然播放量`: CPM naturally - `短直种草视频`: Short-live seeding video - `短直预热视频`: Short-live warm-up video - `短直明星种草`: Celebrity short-live seeding - `短直明星预热`: Celebrity short-live warm-up - `明星视频`: Celebrity video - `合集视频`: Collection video - `抖音短视频共创_主投稿达人`: Douyin short video co-creation - main creator - `抖音短视频共创_参与达人`: Douyin short video co-creation - participant |
| `kolPriceType` enum | values | n/a | n/a | n/a | `千次自然播放量`, `合集视频`, `定制短剧单集`, `抖音短视频共创_主投稿达人`, `抖音短视频共创_参与达人`, `明星视频`, `短直明星种草`, `短直明星预热`, `短直种草视频`, `短直预热视频`, `视频1_20s`, `视频21_60s`, `视频60s以上` |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `searchType` | `query` | n/a | all | `string` | Search criteria type. Available Values: - `NICKNAME`: By Nickname - `CONTENT`: By Content |
| `searchType` enum | values | n/a | n/a | n/a | `CONTENT`, `NICKNAME` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiGsearchSearchForAuthorSquareV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiGsearchSearchForAuthorSquareV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiGsearchSearchForAuthorSquareV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gsearch_search_for_author_square&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_gsearch_search_for_author_square&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiGsearchSearchForAuthorSquareV1` on `/api/douyin-xingtu/gw/api/gsearch/search_for_author_square/v1`.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
