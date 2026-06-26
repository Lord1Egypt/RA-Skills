---
name: Douyin Creator Marketplace (Xingtu) Audience Distribution API
description: Call GET /api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Distribution through JustOneAPI with oAuthorId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution"}}
---

# Douyin Creator Marketplace (Xingtu) Audience Distribution

Use this focused JustOneAPI skill for audience Distribution in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1`. Required non-token inputs are `oAuthorId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) audience Distribution data, including demographic and interest-based audience segmentation, for creator evaluation, campaign planning, and marketplace research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/data_sp/author_audience_distribution`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-data-sp-author-audience-distribution`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiDataSpAuthorAudienceDistributionV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1` | Audience Distribution |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `linkType` | `query` | n/a | all | `string` | Link type filter. Available Values: - `CONNECTED`: Connected - `AWARE`: Aware - `INTERESTED`: Interested - `LIKE`: Like - `FOLLOW`: Follow |
| `linkType` enum | values | n/a | n/a | n/a | `AWARE`, `CONNECTED`, `FOLLOW`, `INTERESTED`, `LIKE` |
| `oAuthorId` | `query` | all | n/a | `string` | Author's unique ID |
| `platform` | `query` | n/a | all | `string` | Platform type. Available Values: - `SHORT_VIDEO`: Short video - `LIVE_STREAMING`: Live streaming - `PICTURE_TEXT`: Picture and text - `SHORT_DRAMA`: Short drama |
| `platform` enum | values | n/a | n/a | n/a | `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA`, `SHORT_VIDEO` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiDataSpAuthorAudienceDistributionV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiDataSpAuthorAudienceDistributionV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiDataSpAuthorAudienceDistributionV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oAuthorId":"<oAuthorId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_author_audience_distribution&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiDataSpAuthorAudienceDistributionV1` on `/api/douyin-xingtu/gw/api/data_sp/author_audience_distribution/v1`.
- Echo the required lookup scope (`oAuthorId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) audience Distribution data, including demographic and interest-based audience segmentation, for creator evaluation, campaign planning, and marketplace research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
