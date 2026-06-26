---
name: Xiaohongshu (RedNote) User Published Notes API
description: Call 2 get-user-note-list versions for Xiaohongshu (RedNote) User Published Notes through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_get_user_note_list"}}
---

# Xiaohongshu (RedNote) User Published Notes

Use this focused JustOneAPI skill for user Published Notes in Xiaohongshu (RedNote). It targets 2 versioned paths under `/api/xiaohongshu/get-user-note-list`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `get-user-note-list`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-get-user-note-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserNoteListV2` | `v2` | `GET` | `/api/xiaohongshu/get-user-note-list/v2` | User Published Notes |
| `getUserNoteListV4` | `v4` | `GET` | `/api/xiaohongshu/get-user-note-list/v4` | User Published Notes |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `lastCursor` | `query` | n/a | all | `string` | Pagination cursor from the previous page (the last note's cursor value) |
| `userId` | `query` | all | n/a | `string` | Unique user identifier on Xiaohongshu |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 2 endpoint versions because their paths share `get-user-note-list` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getUserNoteListV2` (`v2`): required inputs `userId`.
- `getUserNoteListV4` (`v4`): required inputs `userId`.

## Run This Endpoint

Supported operation IDs in this skill: `getUserNoteListV2`, `getUserNoteListV4`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserNoteListV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user_note_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user_note_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserNoteListV2` on `/api/xiaohongshu/get-user-note-list/v2`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
