---
name: Xiaohongshu Creator Marketplace (Pugongying) Creator Search API
description: Call GET /api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Search through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Creator Search

Use this focused JustOneAPI skill for creator Search in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1`. It has no required non-token parameters. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `api/solar/cooperator/blogger/v2`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-api-solar-cooperator-blogger-v2`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `apiSolarCooperatorBloggerV2V1` | `v1` | `GET` | `/api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1` | Creator Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `contentTag` | `query` | n/a | all | `string` | Content categories, separated by commas |
| `fansAge` | `query` | n/a | all | `string` | Target fans age group. Available Values: - `ALL`: All ages - `LT_18`: Under 18 - `AGE_18_24`: 18 to 24 - `AGE_25_34`: 25 to 34 - `AGE_35_44`: 35 to 44 - `GT_44`: Above 44 |
| `fansAge` enum | values | n/a | n/a | n/a | `AGE_18_24`, `AGE_25_34`, `AGE_35_44`, `ALL`, `GT_44`, `LT_18` |
| `fansGender` | `query` | n/a | all | `string` | Target fans gender. Available Values: - `ALL`: All genders - `MALE_HIGH`: Mainly Male - `FE_MALE_HIGH`: Mainly Female |
| `fansGender` enum | values | n/a | n/a | n/a | `ALL`, `FE_MALE_HIGH`, `MALE_HIGH` |
| `fansNumberLower` | `query` | n/a | all | `integer` | Minimum number of fans |
| `fansNumberUpper` | `query` | n/a | all | `integer` | Maximum number of fans |
| `gender` | `query` | n/a | all | `string` | KOL's gender. Available Values: - `ALL`: All genders - `MALE`: Male - `FEMALE`: Female |
| `gender` enum | values | n/a | n/a | n/a | `ALL`, `FEMALE`, `MALE` |
| `keyword` | `query` | n/a | all | `string` | Search keyword |
| `page` | `query` | n/a | all | `integer` | Page number |
| `searchType` | `query` | n/a | all | `string` | Search criteria type. Available Values: - `NICKNAME`: Search by nickname - `NOTE`: Search by note content |
| `searchType` enum | values | n/a | n/a | n/a | `NICKNAME`, `NOTE` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `apiSolarCooperatorBloggerV2V1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `apiSolarCooperatorBloggerV2V1`.

```bash
node {baseDir}/bin/run.mjs --operation "apiSolarCooperatorBloggerV2V1" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `apiSolarCooperatorBloggerV2V1` on `/api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1`.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) creator Search data, including filters, returning profile, and audience, for discovery, comparison, and shortlist building.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
