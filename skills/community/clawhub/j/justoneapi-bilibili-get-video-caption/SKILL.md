---
name: Bilibili Video Captions API
description: Call GET /api/bilibili/get-video-caption/v2 for Bilibili Video Captions through JustOneAPI with aid, bvid, and cid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_video_caption"}}
---

# Bilibili Video Captions

Use this focused JustOneAPI skill for video Captions in Bilibili. It targets `GET /api/bilibili/get-video-caption/v2`. Required non-token inputs are `aid`, `bvid`, and `cid`. OpenAPI describes it as: Get Bilibili video Captions data, including caption data, for transcript extraction and multilingual content analysis.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-video-caption`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-video-caption`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoCaptionV1` | `v2` | `GET` | `/api/bilibili/get-video-caption/v2` | Video Captions |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `aid` | `query` | all | n/a | `string` | Bilibili AID |
| `bvid` | `query` | all | n/a | `string` | Bilibili Video ID (BVID) |
| `cid` | `query` | all | n/a | `string` | Bilibili CID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoCaptionV1` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoCaptionV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoCaptionV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"bvid":"<bvid>","aid":"<aid>","cid":"<cid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_caption&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_caption&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoCaptionV1` on `/api/bilibili/get-video-caption/v2`.
- Echo the required lookup scope (`aid`, `bvid`, and `cid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili video Captions data, including caption data, for transcript extraction and multilingual content analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
