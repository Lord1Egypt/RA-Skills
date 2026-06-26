---
name: Xiaohongshu Creator Marketplace (Pugongying) Note Details API
description: Call GET /api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Details through JustOneAPI with noteId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_api_solar_note_note_id_detail"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Note Details

Use this focused JustOneAPI skill for note Details in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1`. Required non-token inputs are `noteId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) note Details data, including media and engagement signals, for content analysis, archiving, and campaign review.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `api/solar/note/noteId/detail`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-api-solar-note-note-id-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `apiSolarNoteNoteIdDetailV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1` | Note Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `noteId` | `query` | all | n/a | `string` | Note's unique ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `apiSolarNoteNoteIdDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `apiSolarNoteNoteIdDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "apiSolarNoteNoteIdDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"noteId":"<noteId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_note_note_id_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_note_note_id_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `apiSolarNoteNoteIdDetailV1` on `/api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1`.
- Echo the required lookup scope (`noteId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) note Details data, including media and engagement signals, for content analysis, archiving, and campaign review.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
