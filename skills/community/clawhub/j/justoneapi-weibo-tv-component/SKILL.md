---
name: Weibo TV Video Details API
description: Call GET /api/weibo/tv-component/v1 for Weibo TV Video Details through JustOneAPI with oid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_tv_component"}}
---

# Weibo TV Video Details

Use this focused JustOneAPI skill for tV Video Details in Weibo. It targets `GET /api/weibo/tv-component/v1`. Required non-token inputs are `oid`. OpenAPI describes it as: Get Weibo tV Video Details data, including media URLs, author details, and engagement counts, for video research, archiving, and performance analysis.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `tv-component`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-tv-component`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `tvComponentV1` | `v1` | `GET` | `/api/weibo/tv-component/v1` | TV Video Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `oid` | `query` | all | n/a | `string` | Weibo video/object ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `tvComponentV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `tvComponentV1`.

```bash
node {baseDir}/bin/run.mjs --operation "tvComponentV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oid":"<oid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_tv_component&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_tv_component&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `tvComponentV1` on `/api/weibo/tv-component/v1`.
- Echo the required lookup scope (`oid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo tV Video Details data, including media URLs, author details, and engagement counts, for video research, archiving, and performance analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
