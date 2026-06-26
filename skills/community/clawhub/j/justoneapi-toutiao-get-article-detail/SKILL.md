---
name: Toutiao Article Details API
description: Call GET /api/toutiao/get-article-detail/v1 for Toutiao Article Details through JustOneAPI with id.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_toutiao_get_article_detail"}}
---

# Toutiao Article Details

Use this focused JustOneAPI skill for article Details in Toutiao. It targets `GET /api/toutiao/get-article-detail/v1`. Required non-token inputs are `id`. OpenAPI describes it as: Get Toutiao article Details data, including article ID, title, and author information, for content performance analysis and media monitoring and verifying article authenticity and metadata retrieval.

## Endpoint Scope

- Platform key: `toutiao`
- Endpoint key: `get-article-detail`
- Platform family: Toutiao
- Skill slug: `justoneapi-toutiao-get-article-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getToutiaoArticleDetailV1` | `v1` | `GET` | `/api/toutiao/get-article-detail/v1` | Article Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `query` | all | n/a | `string` | The unique identifier of the Toutiao article |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getToutiaoArticleDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getToutiaoArticleDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getToutiaoArticleDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"id":"<id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_article_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_article_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getToutiaoArticleDetailV1` on `/api/toutiao/get-article-detail/v1`.
- Echo the required lookup scope (`id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Toutiao article Details data, including article ID, title, and author information, for content performance analysis and media monitoring and verifying article authenticity and metadata retrieval.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
