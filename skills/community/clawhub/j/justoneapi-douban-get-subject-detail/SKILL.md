---
name: Douban Movie Subject Details API
description: Call GET /api/douban/get-subject-detail/v1 for Douban Movie Subject Details through JustOneAPI with subjectId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douban_get_subject_detail"}}
---

# Douban Movie Subject Details

Use this focused JustOneAPI skill for subject Details in Douban Movie. It targets `GET /api/douban/get-subject-detail/v1`. Required non-token inputs are `subjectId`. OpenAPI describes it as: Get Douban subject Details data, including title, rating, and cast, for title enrichment and catalog research.

## Endpoint Scope

- Platform key: `douban`
- Endpoint key: `get-subject-detail`
- Platform family: Douban Movie
- Skill slug: `justoneapi-douban-get-subject-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getSubjectDetailV1` | `v1` | `GET` | `/api/douban/get-subject-detail/v1` | Subject Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `subjectId` | `query` | all | n/a | `string` | The unique ID for a movie or TV subject on Douban |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getSubjectDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getSubjectDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getSubjectDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"subjectId":"<subjectId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_subject_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_subject_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getSubjectDetailV1` on `/api/douban/get-subject-detail/v1`.
- Echo the required lookup scope (`subjectId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douban subject Details data, including title, rating, and cast, for title enrichment and catalog research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
