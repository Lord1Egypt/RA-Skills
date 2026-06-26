---
name: Xiaohongshu (RedNote) Note Search API
description: Call 2 search-note versions for Xiaohongshu (RedNote) Note Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_search_note"}}
---

# Xiaohongshu (RedNote) Note Search

Use this focused JustOneAPI skill for note Search in Xiaohongshu (RedNote). It targets 2 versioned paths under `/api/xiaohongshu/search-note`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Xiaohongshu (RedNote) note Search data, including snippets, authors, and media, for topic discovery.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `search-note`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-search-note`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getSearchNoteV2` | `v2` | `GET` | `/api/xiaohongshu/search-note/v2` | Note Search |
| `getSearchNoteV3` | `v3` | `GET` | `/api/xiaohongshu/search-note/v3` | Note Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keyword |
| `noteTime` | `query` | n/a | `getSearchNoteV2` | `string` | Note publish time filter. This parameter is for reference only and does not have much effect. Available Values: - `一天内`: Within one day - `一周内`: Within a week - `半年内`: Within half a year |
| `noteTime` enum | values | n/a | n/a | n/a | `一周内`, `一天内`, `半年内` |
| `noteType` | `query` | n/a | all | `string` | Note type filter. Available Values: - `_0`: General - `_1`: Video - `_2`: Normal |
| `noteType` enum | values | n/a | n/a | n/a | `_0`, `_1`, `_2` |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `sort` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `general`: General - `popularity_descending`: Popularity Descending - `time_descending`: Time Descending - `comment_descending`: Comment Descending - `collect_descending`: Collect Descending |
| `sort` enum | values | n/a | n/a | n/a | `collect_descending`, `comment_descending`, `general`, `popularity_descending`, `time_descending` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 2 endpoint versions because their paths share `search-note` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getSearchNoteV2` (`v2`): required inputs `keyword`.
- `getSearchNoteV3` (`v3`): required inputs `keyword`.

## Run This Endpoint

Supported operation IDs in this skill: `getSearchNoteV2`, `getSearchNoteV3`.

```bash
node {baseDir}/bin/run.mjs --operation "getSearchNoteV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_note&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_note&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getSearchNoteV2` on `/api/xiaohongshu/search-note/v2`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) note Search data, including snippets, authors, and media, for topic discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
