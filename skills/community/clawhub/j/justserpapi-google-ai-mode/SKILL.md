---
name: Google SERP Ai Mode API
description: Call GET /api/v1/google/ai-mode for Google SERP Ai Mode through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_ai_mode"}}
---

# Google SERP Ai Mode

Use this focused Just Serp API skill for Google SERP Ai Mode. It targets `GET /api/v1/google/ai-mode`. Required inputs are `query`. OpenAPI describes it as: Get Google aI Mode data, including generated answers, follow-up prompts, and cited links, for AI search experience monitoring.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `ai-mode`
- Group family: Google SERP
- Skill slug: `justserpapi-google-ai-mode`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `aiMode` | `v1` | `GET` | `/api/v1/google/ai-mode` | Mode |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `html` | `query` | n/a | all | `boolean` | Set to true to return the raw HTML of the Google search results page alongside the structured data |
| `location` | `query` | n/a | all | `string` | The textual location name (e.g., 'New York, NY') to localize the search results |
| `query` | `query` | all | n/a | `string` | The search query for Google Search (e.g., 'coffee shops', 'how to bake a cake') |
| `safe` | `query` | n/a | all | `string` | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it |
| `uule` | `query` | n/a | all | `string` | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `aiMode` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `aiMode`.

```bash
node {baseDir}/bin/run.mjs --operation "aiMode" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_ai_mode&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `aiMode` on `/api/v1/google/ai-mode`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google aI Mode data, including generated answers, follow-up prompts, and cited links, for AI search experience monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
