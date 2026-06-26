---
name: Bilibili Video Danmaku API
description: Call GET /api/bilibili/get-video-danmu/v2 for Bilibili Video Danmaku through JustOneAPI with aid and cid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_video_danmu"}}
---

# Bilibili Video Danmaku

Use this focused JustOneAPI skill for video Danmaku in Bilibili. It targets `GET /api/bilibili/get-video-danmu/v2`. Required non-token inputs are `aid` and `cid`. OpenAPI describes it as: Get Bilibili video Danmaku data, including timeline positions and comment text, for audience reaction analysis and subtitle-style comment review.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-video-danmu`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-video-danmu`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoDanmuV2` | `v2` | `GET` | `/api/bilibili/get-video-danmu/v2` | Video Danmaku |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `aid` | `query` | all | n/a | `string` | Bilibili Archive ID (AID) |
| `cid` | `query` | all | n/a | `string` | Bilibili Chat ID (CID) |
| `page` | `query` | n/a | all | `string` | Page number for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoDanmuV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoDanmuV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoDanmuV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"aid":"<aid>","cid":"<cid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_danmu&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_danmu&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoDanmuV2` on `/api/bilibili/get-video-danmu/v2`.
- Echo the required lookup scope (`aid` and `cid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili video Danmaku data, including timeline positions and comment text, for audience reaction analysis and subtitle-style comment review.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
