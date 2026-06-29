---
name: Google SERP Lens API
description: Call GET /api/v1/google/lens for Google SERP Lens through Just Serp API with url.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_lens"}}
---

# Google SERP Lens

Use this focused Just Serp API skill for Google SERP Lens. It targets `GET /api/v1/google/lens`. Required inputs are `url`. OpenAPI describes it as: Get Google lens Search data, including visual matches, product matches, and related links, for visual search analysis and product matching workflows.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `lens`
- Group family: Google SERP
- Skill slug: `justserpapi-google-lens`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `lens` | `v1` | `GET` | `/api/v1/google/lens` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `exact_matches` | `query` | n/a | all | `boolean` | If set to true, the API will search for exact duplicates of the provided image |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `product` | `query` | n/a | all | `boolean` | If set to true, the API will specifically look for product matches and shopping results |
| `url` | `query` | all | n/a | `string` | The URL of the image you want to analyze with Google Lens. Must be a publicly accessible image URL |
| `visual_matches` | `query` | n/a | all | `boolean` | If set to true, the API will return visually similar images and matches |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `lens` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `lens`.

```bash
node {baseDir}/bin/run.mjs --operation "lens" --api-key "$JUST_SERP_API_KEY" --params-json '{"url":"<url>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_lens&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `lens` on `/api/v1/google/lens`.
- Echo the required lookup scope (`url`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google lens Search data, including visual matches, product matches, and related links, for visual search analysis and product matching workflows.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
