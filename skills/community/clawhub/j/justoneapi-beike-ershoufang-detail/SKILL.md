---
name: Beike Resale Housing Details API
description: Call GET /api/beike/ershoufang/detail/v1 for Beike Resale Housing Details through JustOneAPI with cityId and houseCode.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_beike_ershoufang_detail"}}
---

# Beike Resale Housing Details

Use this focused JustOneAPI skill for resale Housing Details in Beike. It targets `GET /api/beike/ershoufang/detail/v1`. Required non-token inputs are `cityId` and `houseCode`. OpenAPI describes it as: Get Beike resale Housing Details data, including - Pricing (total and unit price), Physical attributes (area, and layout, for displaying a full property profile to users and detailed price comparison between specific listings.

## Endpoint Scope

- Platform key: `beike`
- Endpoint key: `ershoufang/detail`
- Platform family: Beike
- Skill slug: `justoneapi-beike-ershoufang-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `ershoufangDetailV1` | `v1` | `GET` | `/api/beike/ershoufang/detail/v1` | Resale Housing Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cityId` | `query` | all | n/a | `string` | The ID of the city (e.g., '110000' for Beijing) |
| `houseCode` | `query` | all | n/a | `string` | The unique identifier for the property listing |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `ershoufangDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `ershoufangDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "ershoufangDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"cityId":"<cityId>","houseCode":"<houseCode>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_ershoufang_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_ershoufang_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `ershoufangDetailV1` on `/api/beike/ershoufang/detail/v1`.
- Echo the required lookup scope (`cityId` and `houseCode`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Beike resale Housing Details data, including - Pricing (total and unit price), Physical attributes (area, and layout, for displaying a full property profile to users and detailed price comparison between specific listings.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
