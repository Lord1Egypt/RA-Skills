---
name: Google SERP Autocomplete API
description: Call GET /api/v1/google/autocomplete for Google SERP Autocomplete through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_autocomplete"}}
---

# Google SERP Autocomplete

Use this focused Just Serp API skill for Google SERP Autocomplete. It targets `GET /api/v1/google/autocomplete`. Required inputs are `query`. OpenAPI describes it as: Get Google autocomplete Suggestions data, including real-time suggestion data, country and language targeting, and structured suggestion lists, for keyword expansion and search intent research.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `autocomplete`
- Group family: Google SERP
- Skill slug: `justserpapi-google-autocomplete`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `autocomplete` | `v1` | `GET` | `/api/v1/google/autocomplete` | Autocomplete Suggestions |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `query` | `query` | all | n/a | `string` | The search query to get autocomplete suggestions for. As you type, Google provides real-time predictions based on popular searches |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `autocomplete` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `autocomplete`.

```bash
node {baseDir}/bin/run.mjs --operation "autocomplete" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_autocomplete&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `autocomplete` on `/api/v1/google/autocomplete`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google autocomplete Suggestions data, including real-time suggestion data, country and language targeting, and structured suggestion lists, for keyword expansion and search intent research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
