---
name: Taobao and Tmall Product Reviews API
description: Call GET /api/taobao/get-item-comment/v3 for Taobao and Tmall Product Reviews through JustOneAPI with itemId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_taobao_get_item_comment"}}
---

# Taobao and Tmall Product Reviews

Use this focused JustOneAPI skill for product Reviews in Taobao and Tmall. It targets `GET /api/taobao/get-item-comment/v3`. Required non-token inputs are `itemId`. OpenAPI describes it as: Get Taobao and Tmall product Reviews data, including ratings, timestamps, and reviewer signals, for feedback analysis and product research.

## Endpoint Scope

- Platform key: `taobao`
- Endpoint key: `get-item-comment`
- Platform family: Taobao and Tmall
- Skill slug: `justoneapi-taobao-get-item-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getItemCommentV3` | `v3` | `GET` | `/api/taobao/get-item-comment/v3` | Product Reviews |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `itemId` | `query` | all | n/a | `string` | AUnique product identifier on Taobao/Tmall (item ID) |
| `orderType` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `feedbackdate`: Sort by feedback date - `general`: General sorting |
| `orderType` enum | values | n/a | n/a | n/a | `feedbackdate`, `general` |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getItemCommentV3` for the documented `v3` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getItemCommentV3`.

```bash
node {baseDir}/bin/run.mjs --operation "getItemCommentV3" --token "$JUST_ONE_API_TOKEN" --params-json '{"itemId":"<itemId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getItemCommentV3` on `/api/taobao/get-item-comment/v3`.
- Echo the required lookup scope (`itemId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Taobao and Tmall product Reviews data, including ratings, timestamps, and reviewer signals, for feedback analysis and product research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
