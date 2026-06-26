---
name: WeChat Official Accounts Article Details API
description: Call GET /api/weixin/get-article-detail/v1 for WeChat Official Accounts Article Details through JustOneAPI with articleUrl.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weixin_get_article_detail"}}
---

# WeChat Official Accounts Article Details

Use this focused JustOneAPI skill for article Details in WeChat Official Accounts. It targets `GET /api/weixin/get-article-detail/v1`. Required non-token inputs are `articleUrl`. OpenAPI describes it as: Get WeChat Official Accounts article Details data, including body content, for article archiving, research, and content analysis.

## Endpoint Scope

- Platform key: `weixin`
- Endpoint key: `get-article-detail`
- Platform family: WeChat Official Accounts
- Skill slug: `justoneapi-weixin-get-article-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getWeixinArticleDetailV1` | `v1` | `GET` | `/api/weixin/get-article-detail/v1` | Article Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `articleUrl` | `query` | all | n/a | `string` | The URL of the Weixin article |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getWeixinArticleDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getWeixinArticleDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getWeixinArticleDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"articleUrl":"<articleUrl>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin_get_article_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getWeixinArticleDetailV1` on `/api/weixin/get-article-detail/v1`.
- Echo the required lookup scope (`articleUrl`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get WeChat Official Accounts article Details data, including body content, for article archiving, research, and content analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
