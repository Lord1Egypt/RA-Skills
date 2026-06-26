---
name: YouTube Video Details API
description: Call GET /api/youtube/get-video-detail/v1 for YouTube Video Details through JustOneAPI with videoId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youtube_get_video_detail"}}
---

# YouTube Video Details

Use this focused JustOneAPI skill for video Details in YouTube. It targets `GET /api/youtube/get-video-detail/v1`. Required non-token inputs are `videoId`. OpenAPI describes it as: Get YouTube video Details data, including its title, description, and view counts, for tracking video engagement and statistics, extracting video metadata for content analysis, and verifying video availability and status.

## Endpoint Scope

- Platform key: `youtube`
- Endpoint key: `get-video-detail`
- Platform family: YouTube
- Skill slug: `justoneapi-youtube-get-video-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getYoutubeVideoDetailV1` | `v1` | `GET` | `/api/youtube/get-video-detail/v1` | Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `videoId` | `query` | all | n/a | `string` | The unique identifier for a YouTube video |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getYoutubeVideoDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getYoutubeVideoDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getYoutubeVideoDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"videoId":"<videoId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_video_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_video_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getYoutubeVideoDetailV1` on `/api/youtube/get-video-detail/v1`.
- Echo the required lookup scope (`videoId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get YouTube video Details data, including its title, description, and view counts, for tracking video engagement and statistics, extracting video metadata for content analysis, and verifying video availability and status.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
