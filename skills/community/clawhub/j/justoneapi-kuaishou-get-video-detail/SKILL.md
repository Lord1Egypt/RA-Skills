---
name: Kuaishou Video Details API
description: Call GET /api/kuaishou/get-video-detail/v2 for Kuaishou Video Details through JustOneAPI with videoId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_kuaishou_get_video_detail"}}
---

# Kuaishou Video Details

Use this focused JustOneAPI skill for video Details in Kuaishou. It targets `GET /api/kuaishou/get-video-detail/v2`. Required non-token inputs are `videoId`. OpenAPI describes it as: Get Kuaishou video Details data, including video URL, caption, and author info, for in-depth content performance analysis and building databases of viral videos.

## Endpoint Scope

- Platform key: `kuaishou`
- Endpoint key: `get-video-detail`
- Platform family: Kuaishou
- Skill slug: `justoneapi-kuaishou-get-video-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoDetailsV2` | `v2` | `GET` | `/api/kuaishou/get-video-detail/v2` | Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `videoId` | `query` | all | n/a | `string` | The unique ID of the Kuaishou video, e.g. `3xg9avuebhtfcku` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoDetailsV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoDetailsV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoDetailsV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"videoId":"<videoId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoDetailsV2` on `/api/kuaishou/get-video-detail/v2`.
- Echo the required lookup scope (`videoId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Kuaishou video Details data, including video URL, caption, and author info, for in-depth content performance analysis and building databases of viral videos.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
