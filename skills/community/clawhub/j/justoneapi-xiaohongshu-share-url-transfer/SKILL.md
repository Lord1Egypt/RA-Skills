---
name: Xiaohongshu (RedNote) Share Link Resolution API
description: Call GET /api/xiaohongshu/share-url-transfer/v1 for Xiaohongshu (RedNote) Share Link Resolution through JustOneAPI with shareUrl.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_share_url_transfer"}}
---

# Xiaohongshu (RedNote) Share Link Resolution

Use this focused JustOneAPI skill for share Link Resolution in Xiaohongshu (RedNote). It targets `GET /api/xiaohongshu/share-url-transfer/v1`. Required non-token inputs are `shareUrl`. OpenAPI describes it as: Get Xiaohongshu (RedNote) share Link Resolution data, including helping extract note IDs, for downstream note and comment workflows.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `share-url-transfer`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-share-url-transfer`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `shareXiaohongshuUrlTransferV1` | `v1` | `GET` | `/api/xiaohongshu/share-url-transfer/v1` | Share Link Resolution |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `shareUrl` | `query` | all | n/a | `string` | RedNote share link URL to be resolved (short link or shared URL) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `shareXiaohongshuUrlTransferV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `shareXiaohongshuUrlTransferV1`.

```bash
node {baseDir}/bin/run.mjs --operation "shareXiaohongshuUrlTransferV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"shareUrl":"<shareUrl>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_share_url_transfer&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_share_url_transfer&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `shareXiaohongshuUrlTransferV1` on `/api/xiaohongshu/share-url-transfer/v1`.
- Echo the required lookup scope (`shareUrl`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) share Link Resolution data, including helping extract note IDs, for downstream note and comment workflows.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
