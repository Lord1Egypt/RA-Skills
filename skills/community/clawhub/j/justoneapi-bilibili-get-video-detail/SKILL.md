---
name: Bilibili Video Details API
description: Call GET /api/bilibili/get-video-detail/v2 for Bilibili Video Details through JustOneAPI with bvid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_video_detail"}}
---

# Bilibili Video Details

Use this focused JustOneAPI skill for video Details in Bilibili. It targets `GET /api/bilibili/get-video-detail/v2`. Required non-token inputs are `bvid`. OpenAPI describes it as: Get Bilibili video Details data, including metadata (title, tags, and publishing time), for tracking video performance and engagement metrics and analyzing content metadata and uploader information.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-video-detail`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-video-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getBilibiliVideoDetailV2` | `v2` | `GET` | `/api/bilibili/get-video-detail/v2` | Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `bvid` | `query` | all | n/a | `string` | Bilibili Video ID (BVID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getBilibiliVideoDetailV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getBilibiliVideoDetailV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getBilibiliVideoDetailV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"bvid":"<bvid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getBilibiliVideoDetailV2` on `/api/bilibili/get-video-detail/v2`.
- Echo the required lookup scope (`bvid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili video Details data, including metadata (title, tags, and publishing time), for tracking video performance and engagement metrics and analyzing content metadata and uploader information.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
