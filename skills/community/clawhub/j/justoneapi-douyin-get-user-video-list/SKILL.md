---
name: Douyin (TikTok China) User Published Videos API
description: Call GET /api/douyin/get-user-video-list/v3 for Douyin (TikTok China) User Published Videos through JustOneAPI with secUid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_get_user_video_list"}}
---

# Douyin (TikTok China) User Published Videos

Use this focused JustOneAPI skill for user Published Videos in Douyin (TikTok China). It targets `GET /api/douyin/get-user-video-list/v3`. Required non-token inputs are `secUid`. OpenAPI describes it as: Get Douyin (TikTok China) user Published Videos data, including captions, covers, and publish times, for account monitoring.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `get-user-video-list`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-get-user-video-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserVideoListV3` | `v3` | `GET` | `/api/douyin/get-user-video-list/v3` | User Published Videos |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `maxCursor` | `query` | n/a | all | `integer` | Pagination cursor; use 0 for the first page, and the `max_cursor` from the previous response for subsequent pages |
| `secUid` | `query` | all | n/a | `string` | The unique user ID (sec_uid) on Douyin |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserVideoListV3` for the documented `v3` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserVideoListV3`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserVideoListV3" --token "$JUST_ONE_API_TOKEN" --params-json '{"secUid":"<secUid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_video_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_video_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserVideoListV3` on `/api/douyin/get-user-video-list/v3`.
- Echo the required lookup scope (`secUid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) user Published Videos data, including captions, covers, and publish times, for account monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
