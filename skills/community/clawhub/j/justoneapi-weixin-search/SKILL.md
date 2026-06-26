---
name: WeChat Official Accounts Keyword Search API
description: Call GET /api/weixin/search/v1 for WeChat Official Accounts Keyword Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weixin_search"}}
---

# WeChat Official Accounts Keyword Search

Use this focused JustOneAPI skill for keyword Search in WeChat Official Accounts. It targets `GET /api/weixin/search/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get WeChat Official Accounts keyword Search data, including account names, titles, and publish times, for content discovery.

## Endpoint Scope

- Platform key: `weixin`
- Endpoint key: `search`
- Platform family: WeChat Official Accounts
- Skill slug: `justoneapi-weixin-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchWeixinV1` | `v1` | `GET` | `/api/weixin/search/v1` | Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | The search keyword |
| `offset` | `query` | n/a | all | `integer` | Pagination offset (starts with 0, increment by 20) |
| `searchType` | `query` | n/a | all | `string` | Type of search results (accounts, articles, etc.). Available Values: - `_0`: All - `_1`: WeChat Official Account - `_2`: Article - `_7`: WeChat Channel - `_262208`: Wechat Mini Program - `_384`: Emoji - `_16777728`: Encyclopedia - `_9`: Live - `_1024`: Book - `_512`: Music - `_16384`: News - `_8192`: Wechat Index - `_8`: Moments |
| `searchType` enum | values | n/a | n/a | n/a | `_0`, `_1`, `_1024`, `_16384`, `_16777728`, `_2`, `_262208`, `_384`, `_512`, `_7`, `_8`, `_8192`, `_9` |
| `sortType` | `query` | n/a | all | `string` | Sorting criteria for search results. Available Values: - `_0`: Default - `_2`: Latest - `_4`: Hot |
| `sortType` enum | values | n/a | n/a | n/a | `_0`, `_2`, `_4` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchWeixinV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchWeixinV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchWeixinV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_search&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchWeixinV1` on `/api/weixin/search/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get WeChat Official Accounts keyword Search data, including account names, titles, and publish times, for content discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
