---
name: Google SERP Trends Autocomplete API
description: Call GET /api/v1/google/trends/autocomplete for Google SERP Trends Autocomplete through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_trends_autocomplete"}}
---

# Google SERP Trends Autocomplete

Use this focused Just Serp API skill for Google SERP Trends Autocomplete. It targets `GET /api/v1/google/trends/autocomplete`. Required inputs are `query`. OpenAPI describes it as: Get Google trends Autocomplete data, including topic IDs, for trend discovery and topic expansion.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `trends/autocomplete`
- Group family: Google SERP
- Skill slug: `justserpapi-google-trends-autocomplete`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `TrendsAutocomplete` | `v1` | `GET` | `/api/v1/google/trends/autocomplete` | Autocomplete |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `query` | `query` | all | n/a | `string` | The search query to get trending autocomplete suggestions for (e.g., 'artificial') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `TrendsAutocomplete` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `TrendsAutocomplete`.

```bash
node {baseDir}/bin/run.mjs --operation "TrendsAutocomplete" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_autocomplete&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `TrendsAutocomplete` on `/api/v1/google/trends/autocomplete`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google trends Autocomplete data, including topic IDs, for trend discovery and topic expansion.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
