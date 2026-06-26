---
name: Xiaohongshu (RedNote) Comment Replies API
description: Call GET /api/xiaohongshu/get-note-sub-comment/v2 for Xiaohongshu (RedNote) Comment Replies through JustOneAPI with commentId and noteId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_get_note_sub_comment"}}
---

# Xiaohongshu (RedNote) Comment Replies

Use this focused JustOneAPI skill for comment Replies in Xiaohongshu (RedNote). It targets `GET /api/xiaohongshu/get-note-sub-comment/v2`. Required non-token inputs are `commentId` and `noteId`. OpenAPI describes it as: Get Xiaohongshu (RedNote) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `get-note-sub-comment`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-get-note-sub-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getNoteSubCommentV2` | `v2` | `GET` | `/api/xiaohongshu/get-note-sub-comment/v2` | Comment Replies |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `commentId` | `query` | all | n/a | `string` | Unique comment identifier on Xiaohongshu |
| `lastCursor` | `query` | n/a | all | `string` | Pagination cursor from the previous page (use the cursor value returned by the last response) |
| `noteId` | `query` | all | n/a | `string` | Unique note identifier on Xiaohongshu |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getNoteSubCommentV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getNoteSubCommentV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getNoteSubCommentV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"noteId":"<noteId>","commentId":"<commentId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_sub_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_sub_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getNoteSubCommentV2` on `/api/xiaohongshu/get-note-sub-comment/v2`.
- Echo the required lookup scope (`commentId` and `noteId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
