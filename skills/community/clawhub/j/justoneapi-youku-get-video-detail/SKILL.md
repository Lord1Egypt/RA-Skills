---
name: YOUKU Video Details API
description: Call GET /api/youku/get-video-detail/v1 for YOUKU Video Details through JustOneAPI with videoId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youku_get_video_detail"}}
---

# YOUKU Video Details

Use this focused JustOneAPI skill for video Details in YOUKU. It targets `GET /api/youku/get-video-detail/v1`. Required non-token inputs are `videoId`. OpenAPI describes it as: Get YOUKU video Details data, including video ID, title, and description, for fetching comprehensive metadata for a single video, tracking engagement metrics like play counts and likes, and integrating detailed video info into third-party dashboards.

## Endpoint Scope

- Platform key: `youku`
- Endpoint key: `get-video-detail`
- Platform family: YOUKU
- Skill slug: `justoneapi-youku-get-video-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getYoukuVideoDetailV1` | `v1` | `GET` | `/api/youku/get-video-detail/v1` | Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `videoId` | `query` | all | n/a | `string` | The unique identifier for the video |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getYoukuVideoDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getYoukuVideoDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getYoukuVideoDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"videoId":"<videoId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_video_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_video_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getYoukuVideoDetailV1` on `/api/youku/get-video-detail/v1`.
- Echo the required lookup scope (`videoId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get YOUKU video Details data, including video ID, title, and description, for fetching comprehensive metadata for a single video, tracking engagement metrics like play counts and likes, and integrating detailed video info into third-party dashboards.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
