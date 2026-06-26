---
name: Xiaohongshu (RedNote) Note Details API
description: Call 3 get-note-detail versions for Xiaohongshu (RedNote) Note Details through JustOneAPI with noteId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_get_note_detail"}}
---

# Xiaohongshu (RedNote) Note Details

Use this focused JustOneAPI skill for note Details in Xiaohongshu (RedNote). It targets 3 versioned paths under `/api/xiaohongshu/get-note-detail`. Required non-token inputs are `noteId`. OpenAPI describes it as: Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `get-note-detail`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-get-note-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getXiaohongshuNoteDetailV1` | `v1` | `GET` | `/api/xiaohongshu/get-note-detail/v1` | Note Details |
| `getNoteDetailV3` | `v3` | `GET` | `/api/xiaohongshu/get-note-detail/v3` | Note Details |
| `getNoteDetailV7` | `v7` | `GET` | `/api/xiaohongshu/get-note-detail/v7` | Note Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `noteId` | `query` | all | n/a | `string` | Unique note identifier on Xiaohongshu |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 3 endpoint versions because their paths share `get-note-detail` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getXiaohongshuNoteDetailV1` (`v1`): required inputs `noteId`.
- `getNoteDetailV3` (`v3`): required inputs `noteId`.
- `getNoteDetailV7` (`v7`): required inputs `noteId`.

## Run This Endpoint

Supported operation IDs in this skill: `getXiaohongshuNoteDetailV1`, `getNoteDetailV3`, `getNoteDetailV7`.

```bash
node {baseDir}/bin/run.mjs --operation "getXiaohongshuNoteDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"noteId":"<noteId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getXiaohongshuNoteDetailV1` on `/api/xiaohongshu/get-note-detail/v1`.
- Echo the required lookup scope (`noteId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
