---
name: Douyin Creator Marketplace (Xingtu) Creator Order Experience API
description: Call GET /api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1 for Douyin Creator Marketplace (Xingtu) Creator Order Experience through JustOneAPI with oAuthorId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_aggregator_get_author_order_experience"}}
---

# Douyin Creator Marketplace (Xingtu) Creator Order Experience

Use this focused JustOneAPI skill for creator Order Experience in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1`. Required non-token inputs are `oAuthorId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) creator Order Experience data, including commercial history and transaction-related indicators, for creator evaluation, campaign planning, and marketplace research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/aggregator/get_author_order_experience`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-aggregator-get-author-order-experience`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiAggregatorGetAuthorOrderExperienceV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1` | Creator Order Experience |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `oAuthorId` | `query` | all | n/a | `string` | Author's unique ID |
| `period` | `query` | n/a | all | `string` | Time period. Available Values: - `DAY_30`: Last 30 days - `DAY_90`: Last 90 days |
| `period` enum | values | n/a | n/a | n/a | `DAY_30`, `DAY_90` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiAggregatorGetAuthorOrderExperienceV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiAggregatorGetAuthorOrderExperienceV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiAggregatorGetAuthorOrderExperienceV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oAuthorId":"<oAuthorId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_order_experience&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_aggregator_get_author_order_experience&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiAggregatorGetAuthorOrderExperienceV1` on `/api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1`.
- Echo the required lookup scope (`oAuthorId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) creator Order Experience data, including commercial history and transaction-related indicators, for creator evaluation, campaign planning, and marketplace research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
