---
name: WeChat Official Accounts User Published Posts API
description: Call GET /api/weixin/get-user-post/v1 for WeChat Official Accounts User Published Posts through JustOneAPI with wxid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weixin_get_user_post"}}
---

# WeChat Official Accounts User Published Posts

Use this focused JustOneAPI skill for user Published Posts in WeChat Official Accounts. It targets `GET /api/weixin/get-user-post/v1`. Required non-token inputs are `wxid`. OpenAPI describes it as: Get WeChat Official Accounts user Published Posts data, including titles, publish times, and summaries, for account monitoring.

## Endpoint Scope

- Platform key: `weixin`
- Endpoint key: `get-user-post`
- Platform family: WeChat Official Accounts
- Skill slug: `justoneapi-weixin-get-user-post`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserPost` | `v1` | `GET` | `/api/weixin/get-user-post/v1` | User Published Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `wxid` | `query` | all | n/a | `string` | The ID of the Weixin Official Account (e.g., 'rmrbwx') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserPost` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserPost`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserPost" --token "$JUST_ONE_API_TOKEN" --params-json '{"wxid":"<wxid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_user_post&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_user_post&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserPost` on `/api/weixin/get-user-post/v1`.
- Echo the required lookup scope (`wxid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get WeChat Official Accounts user Published Posts data, including titles, publish times, and summaries, for account monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
