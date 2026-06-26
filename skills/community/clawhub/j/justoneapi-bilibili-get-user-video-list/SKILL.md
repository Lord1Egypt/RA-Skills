---
name: Bilibili User Published Videos API
description: Call GET /api/bilibili/get-user-video-list/v2 for Bilibili User Published Videos through JustOneAPI with uid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_user_video_list"}}
---

# Bilibili User Published Videos

Use this focused JustOneAPI skill for user Published Videos in Bilibili. It targets `GET /api/bilibili/get-user-video-list/v2`. Required non-token inputs are `uid`. OpenAPI describes it as: Get Bilibili user Published Videos data, including titles, covers, and publish times, for creator monitoring and content performance analysis.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-user-video-list`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-user-video-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getBilibiliUserVideoListV2` | `v2` | `GET` | `/api/bilibili/get-user-video-list/v2` | User Published Videos |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `param` | `query` | n/a | all | `string` | Pagination parameter from previous response |
| `uid` | `query` | all | n/a | `string` | Bilibili User ID (UID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getBilibiliUserVideoListV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getBilibiliUserVideoListV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getBilibiliUserVideoListV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"uid":"<uid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_video_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_video_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getBilibiliUserVideoListV2` on `/api/bilibili/get-user-video-list/v2`.
- Echo the required lookup scope (`uid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili user Published Videos data, including titles, covers, and publish times, for creator monitoring and content performance analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
