---
name: Xiaohongshu (RedNote) User Profile API
description: Call 2 get-user versions for Xiaohongshu (RedNote) User Profile through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_get_user"}}
---

# Xiaohongshu (RedNote) User Profile

Use this focused JustOneAPI skill for user Profile in Xiaohongshu (RedNote). It targets 2 versioned paths under `/api/xiaohongshu/get-user`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Xiaohongshu (RedNote) user Profile data, including follower counts and bio details, for creator research, account analysis, and competitor monitoring.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `get-user`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-get-user`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserV3` | `v3` | `GET` | `/api/xiaohongshu/get-user/v3` | User Profile |
| `getUserV4` | `v4` | `GET` | `/api/xiaohongshu/get-user/v4` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `userId` | `query` | all | n/a | `string` | Unique user identifier on Xiaohongshu |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 2 endpoint versions because their paths share `get-user` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getUserV3` (`v3`): required inputs `userId`.
- `getUserV4` (`v4`): required inputs `userId`.

## Run This Endpoint

Supported operation IDs in this skill: `getUserV3`, `getUserV4`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserV3" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserV3` on `/api/xiaohongshu/get-user/v3`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) user Profile data, including follower counts and bio details, for creator research, account analysis, and competitor monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
