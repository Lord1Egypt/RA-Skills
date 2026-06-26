---
name: Kuaishou Video Comments API
description: Call GET /api/kuaishou/get-video-comment/v1 for Kuaishou Video Comments through JustOneAPI with videoId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_kuaishou_get_video_comment"}}
---

# Kuaishou Video Comments

Use this focused JustOneAPI skill for video Comments in Kuaishou. It targets `GET /api/kuaishou/get-video-comment/v1`. Required non-token inputs are `videoId`. OpenAPI describes it as: Retrieves public comments of a Kuaishou video, including comment content, author info, like count, and reply count. Typical use cases: - Sentiment analysis and community feedback monitoring - Gathering engagement data for specific videos.

## Endpoint Scope

- Platform key: `kuaishou`
- Endpoint key: `get-video-comment`
- Platform family: Kuaishou
- Skill slug: `justoneapi-kuaishou-get-video-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoCommentsV1` | `v1` | `GET` | `/api/kuaishou/get-video-comment/v1` | Video Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `pcursor` | `query` | n/a | all | `string` | Pagination cursor for subsequent pages |
| `videoId` | `query` | all | n/a | `string` | The unique ID of the Kuaishou video, e.g. `3xbknvct79h46h9` or refer_photo_id `177012131237` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoCommentsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoCommentsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoCommentsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"videoId":"<videoId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_video_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoCommentsV1` on `/api/kuaishou/get-video-comment/v1`.
- Echo the required lookup scope (`videoId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Retrieves public comments of a Kuaishou video, including comment content, author info, like count, and reply count. Typical use cases: - Sentiment analysis and community feedback monitoring - Gathering engagement data for specific videos.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
