---
name: Douyin Creator Marketplace (Xingtu) Video Details API
description: Call GET /api/douyin-xingtu/get-video-detail/v1 for Douyin Creator Marketplace (Xingtu) Video Details through JustOneAPI with detailId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_get_video_detail"}}
---

# Douyin Creator Marketplace (Xingtu) Video Details

Use this focused JustOneAPI skill for video Details in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/get-video-detail/v1`. Required non-token inputs are `detailId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) video Details data, including performance fields from the legacy Douyin Xingtu endpoint, for content review and integration compatibility.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `get-video-detail`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-get-video-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getDouyinXingtuVideoDetailV1` | `v1` | `GET` | `/api/douyin-xingtu/get-video-detail/v1` | Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `detailId` | `query` | all | n/a | `string` | Video detail ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getDouyinXingtuVideoDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getDouyinXingtuVideoDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getDouyinXingtuVideoDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"detailId":"<detailId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_video_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_video_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getDouyinXingtuVideoDetailV1` on `/api/douyin-xingtu/get-video-detail/v1`.
- Echo the required lookup scope (`detailId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) video Details data, including performance fields from the legacy Douyin Xingtu endpoint, for content review and integration compatibility.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
