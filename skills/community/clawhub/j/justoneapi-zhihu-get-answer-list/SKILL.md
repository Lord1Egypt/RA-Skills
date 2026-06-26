---
name: Zhihu Answer List API
description: Call GET /api/zhihu/get-answer-list/v1 for Zhihu Answer List through JustOneAPI with questionId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_zhihu_get_answer_list"}}
---

# Zhihu Answer List

Use this focused JustOneAPI skill for answer List in Zhihu. It targets `GET /api/zhihu/get-answer-list/v1`. Required non-token inputs are `questionId`. OpenAPI describes it as: Get Zhihu answer List data, including answer content, author profiles, and interaction metrics, for question analysis and answer research.

## Endpoint Scope

- Platform key: `zhihu`
- Endpoint key: `get-answer-list`
- Platform family: Zhihu
- Skill slug: `justoneapi-zhihu-get-answer-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getAnswerListV1` | `v1` | `GET` | `/api/zhihu/get-answer-list/v1` | Answer List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor from previous result |
| `offset` | `query` | n/a | all | `integer` | Start offset, begins with 0 |
| `order` | `query` | n/a | all | `string` | Sorting criteria for answers. Available Values: - `_default`: Default sorting. - `_updated`: Sorted by updated time |
| `order` enum | values | n/a | n/a | n/a | `_default`, `_updated` |
| `questionId` | `query` | all | n/a | `string` | Question ID |
| `sessionId` | `query` | n/a | all | `string` | Session ID from previous result |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getAnswerListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getAnswerListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getAnswerListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"questionId":"<questionId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_answer_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu_get_answer_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getAnswerListV1` on `/api/zhihu/get-answer-list/v1`.
- Echo the required lookup scope (`questionId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Zhihu answer List data, including answer content, author profiles, and interaction metrics, for question analysis and answer research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
