---
name: Zhihu Column Article List API
description: Call GET /api/zhihu/get-column-article-list/v1 for Zhihu Column Article List through JustOneAPI with columnId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_zhihu_get_column_article_list"}}
---

# Zhihu Column Article List

Use this focused JustOneAPI skill for column Article List in Zhihu. It targets `GET /api/zhihu/get-column-article-list/v1`. Required non-token inputs are `columnId`. OpenAPI describes it as: Get Zhihu column Article List data, including article metadata and list ordering, for column monitoring and content collection.

## Endpoint Scope

- Platform key: `zhihu`
- Endpoint key: `get-column-article-list`
- Platform family: Zhihu
- Skill slug: `justoneapi-zhihu-get-column-article-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getColumnArticleListV1` | `v1` | `GET` | `/api/zhihu/get-column-article-list/v1` | Column Article List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `columnId` | `query` | all | n/a | `string` | Column ID |
| `offset` | `query` | n/a | all | `integer` | Start offset, begins with 0 |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getColumnArticleListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getColumnArticleListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getColumnArticleListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"columnId":"<columnId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_column_article_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getColumnArticleListV1` on `/api/zhihu/get-column-article-list/v1`.
- Echo the required lookup scope (`columnId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Zhihu column Article List data, including article metadata and list ordering, for column monitoring and content collection.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
