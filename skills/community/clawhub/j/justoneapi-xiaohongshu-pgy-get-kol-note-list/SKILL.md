---
name: Xiaohongshu Creator Marketplace (Pugongying) Creator Note List API
description: Call GET /api/xiaohongshu-pgy/get-kol-note-list/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Note List through JustOneAPI with adSwitch, kolId, and orderType.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_get_kol_note_list"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Creator Note List

Use this focused JustOneAPI skill for creator Note List in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/get-kol-note-list/v1`. Required non-token inputs are `adSwitch`, `kolId`, and `orderType`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) creator Note List data, including content metadata, publish time, and engagement indicators, for content analysis.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `get-kol-note-list`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-get-kol-note-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolNoteListV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/get-kol-note-list/v1` | Creator Note List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `adSwitch` | `query` | all | n/a | `string` | Ad filter. Available Values: - `_1`: Full traffic (All notes) - `_0`: Natural traffic (Organic notes) |
| `adSwitch` enum | values | n/a | n/a | n/a | `_0`, `_1` |
| `kolId` | `query` | all | n/a | `string` | KOL ID |
| `noteType` | `query` | n/a | all | `string` | Note type. Available Values: - `_1`: Photo and Text notes - `_2`: Video notes - `_3`: Cooperation notes - `_4`: All types |
| `noteType` enum | values | n/a | n/a | n/a | `_1`, `_2`, `_3`, `_4` |
| `orderType` | `query` | all | n/a | `string` | Sorting order. Available Values: - `_1`: Latest - `_2`: Most read - `_3`: Most interactions |
| `orderType` enum | values | n/a | n/a | n/a | `_1`, `_2`, `_3` |
| `page` | `query` | n/a | all | `integer` | Page number |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolNoteListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolNoteListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolNoteListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>","adSwitch":"_1","orderType":"_1"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolNoteListV1` on `/api/xiaohongshu-pgy/get-kol-note-list/v1`.
- Echo the required lookup scope (`adSwitch`, `kolId`, and `orderType`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) creator Note List data, including content metadata, publish time, and engagement indicators, for content analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
