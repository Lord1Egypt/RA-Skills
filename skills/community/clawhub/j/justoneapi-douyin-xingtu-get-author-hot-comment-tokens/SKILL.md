---
name: Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis API
description: Call GET /api/douyin-xingtu/get-author-hot-comment-tokens/v1 for Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis through JustOneAPI with kolId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_get_author_hot_comment_tokens"}}
---

# Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis

Use this focused JustOneAPI skill for kOL Comment Keyword Analysis in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/get-author-hot-comment-tokens/v1`. Required non-token inputs are `kolId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `get-author-hot-comment-tokens`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-get-author-hot-comment-tokens`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getAuthorHotCommentTokensV1` | `v1` | `GET` | `/api/douyin-xingtu/get-author-hot-comment-tokens/v1` | KOL Comment Keyword Analysis |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `kolId` | `query` | all | n/a | `string` | KOL ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getAuthorHotCommentTokensV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getAuthorHotCommentTokensV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getAuthorHotCommentTokensV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_hot_comment_tokens&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_author_hot_comment_tokens&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getAuthorHotCommentTokensV1` on `/api/douyin-xingtu/get-author-hot-comment-tokens/v1`.
- Echo the required lookup scope (`kolId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
