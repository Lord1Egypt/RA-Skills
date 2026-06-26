---
name: Douyin (TikTok China) Video Details API
description: Call GET /api/douyin/get-video-detail/v2 for Douyin (TikTok China) Video Details through JustOneAPI with videoId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_get_video_detail"}}
---

# Douyin (TikTok China) Video Details

Use this focused JustOneAPI skill for video Details in Douyin (TikTok China). It targets `GET /api/douyin/get-video-detail/v2`. Required non-token inputs are `videoId`. OpenAPI describes it as: Get Douyin (TikTok China) video Details data, including author details, publish time, and engagement counts, for video research, archiving, and performance analysis.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `get-video-detail`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-get-video-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getDouyinVideoDetailV2` | `v2` | `GET` | `/api/douyin/get-video-detail/v2` | Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `videoId` | `query` | all | n/a | `string` | The unique video identifier (aweme_id or model_id) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getDouyinVideoDetailV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getDouyinVideoDetailV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getDouyinVideoDetailV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"videoId":"<videoId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getDouyinVideoDetailV2` on `/api/douyin/get-video-detail/v2`.
- Echo the required lookup scope (`videoId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) video Details data, including author details, publish time, and engagement counts, for video research, archiving, and performance analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
