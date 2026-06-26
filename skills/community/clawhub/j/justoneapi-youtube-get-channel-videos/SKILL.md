---
name: YouTube Channel Videos API
description: Call GET /api/youtube/get-channel-videos/v1 for YouTube Channel Videos through JustOneAPI with channelId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youtube_get_channel_videos"}}
---

# YouTube Channel Videos

Use this focused JustOneAPI skill for channel Videos in YouTube. It targets `GET /api/youtube/get-channel-videos/v1`. Required non-token inputs are `channelId`. OpenAPI describes it as: Retrieve a list of videos from a specific YouTube channel, providing detailed insights into content performance and upload history.

## Endpoint Scope

- Platform key: `youtube`
- Endpoint key: `get-channel-videos`
- Platform family: YouTube
- Skill slug: `justoneapi-youtube-get-channel-videos`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getChannelVideosV1` | `v1` | `GET` | `/api/youtube/get-channel-videos/v1` | Channel Videos |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `channelId` | `query` | all | n/a | `string` | The unique identifier for a YouTube channel |
| `cursor` | `query` | n/a | all | `string` | The cursor for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getChannelVideosV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getChannelVideosV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getChannelVideosV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"channelId":"<channelId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_channel_videos&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube_get_channel_videos&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getChannelVideosV1` on `/api/youtube/get-channel-videos/v1`.
- Echo the required lookup scope (`channelId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Retrieve a list of videos from a specific YouTube channel, providing detailed insights into content performance and upload history.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
