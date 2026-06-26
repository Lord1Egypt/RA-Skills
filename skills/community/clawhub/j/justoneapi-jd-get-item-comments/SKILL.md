---
name: JD.com Product Comments API
description: Call GET /api/jd/get-item-comments/v1 for JD.com Product Comments through JustOneAPI with itemId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_jd_get_item_comments"}}
---

# JD.com Product Comments

Use this focused JustOneAPI skill for product Comments in JD.com. It targets `GET /api/jd/get-item-comments/v1`. Required non-token inputs are `itemId`. OpenAPI describes it as: Get JD.com product Comments data, including ratings, timestamps, and reviewer signals, for customer feedback analysis and product research.

## Endpoint Scope

- Platform key: `jd`
- Endpoint key: `get-item-comments`
- Platform family: JD.com
- Skill slug: `justoneapi-jd-get-item-comments`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getItemCommentsV1` | `v1` | `GET` | `/api/jd/get-item-comments/v1` | Product Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `itemId` | `query` | all | n/a | `string` | A unique product identifier on JD.com (item ID) |
| `page` | `query` | n/a | all | `string` | Page number for paginated comments |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getItemCommentsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getItemCommentsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getItemCommentsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"itemId":"<itemId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_comments&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_comments&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getItemCommentsV1` on `/api/jd/get-item-comments/v1`.
- Echo the required lookup scope (`itemId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get JD.com product Comments data, including ratings, timestamps, and reviewer signals, for customer feedback analysis and product research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
