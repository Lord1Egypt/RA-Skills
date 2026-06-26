---
name: Kuaishou User Published Videos API
description: Call GET /api/kuaishou/get-user-video-list/v2 for Kuaishou User Published Videos through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_kuaishou_get_user_video_list"}}
---

# Kuaishou User Published Videos

Use this focused JustOneAPI skill for user Published Videos in Kuaishou. It targets `GET /api/kuaishou/get-user-video-list/v2`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Kuaishou user Published Videos data, including covers, publish times, and engagement metrics, for creator monitoring and content performance analysis.

## Endpoint Scope

- Platform key: `kuaishou`
- Endpoint key: `get-user-video-list`
- Platform family: Kuaishou
- Skill slug: `justoneapi-kuaishou-get-user-video-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKuaishouUserVideoListV2` | `v2` | `GET` | `/api/kuaishou/get-user-video-list/v2` | User Published Videos |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `pcursor` | `query` | n/a | all | `string` | Pagination cursor for subsequent pages |
| `userId` | `query` | all | n/a | `string` | The unique user ID on Kuaishou |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKuaishouUserVideoListV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKuaishouUserVideoListV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getKuaishouUserVideoListV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_video_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_video_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKuaishouUserVideoListV2` on `/api/kuaishou/get-user-video-list/v2`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Kuaishou user Published Videos data, including covers, publish times, and engagement metrics, for creator monitoring and content performance analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
