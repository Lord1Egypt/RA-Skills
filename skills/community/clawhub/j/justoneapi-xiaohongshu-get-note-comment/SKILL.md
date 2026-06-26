---
name: Xiaohongshu (RedNote) Note Comments API
description: Call 2 get-note-comment versions for Xiaohongshu (RedNote) Note Comments through JustOneAPI with noteId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_get_note_comment"}}
---

# Xiaohongshu (RedNote) Note Comments

Use this focused JustOneAPI skill for note Comments in Xiaohongshu (RedNote). It targets 2 versioned paths under `/api/xiaohongshu/get-note-comment`. Required non-token inputs are `noteId`. OpenAPI describes it as: Get Xiaohongshu (RedNote) note Comments data, including text, authors, and timestamps, for feedback analysis.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `get-note-comment`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-get-note-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getNoteCommentV2` | `v2` | `GET` | `/api/xiaohongshu/get-note-comment/v2` | Note Comments |
| `getNoteCommentV4` | `v4` | `GET` | `/api/xiaohongshu/get-note-comment/v4` | Note Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `lastCursor` | `query` | n/a | `getNoteCommentV2` | `string` | Pagination cursor from the previous page (use the cursor value returned by the last response) |
| `noteId` | `query` | all | n/a | `string` | Unique note identifier on Xiaohongshu |
| `sort` | `query` | n/a | `getNoteCommentV2` | `string` | Sort order for the result set. Available Values: - `normal`: Normal - `latest`: Latest |
| `sort` enum | values | n/a | n/a | n/a | `latest`, `normal` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 2 endpoint versions because their paths share `get-note-comment` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getNoteCommentV2` (`v2`): required inputs `noteId`.
- `getNoteCommentV4` (`v4`): required inputs `noteId`.

## Run This Endpoint

Supported operation IDs in this skill: `getNoteCommentV2`, `getNoteCommentV4`.

```bash
node {baseDir}/bin/run.mjs --operation "getNoteCommentV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"noteId":"<noteId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getNoteCommentV2` on `/api/xiaohongshu/get-note-comment/v2`.
- Echo the required lookup scope (`noteId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) note Comments data, including text, authors, and timestamps, for feedback analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
