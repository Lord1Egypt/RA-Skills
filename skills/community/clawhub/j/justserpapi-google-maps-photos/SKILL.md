---
name: Google SERP Maps Photos API
description: Call GET /api/v1/google/maps/photos for Google SERP Maps Photos through Just Serp API with data_id.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_photos&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_photos&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_maps_photos"}}
---

# Google SERP Maps Photos

Use this focused Just Serp API skill for Google SERP Maps Photos. It targets `GET /api/v1/google/maps/photos`. Required inputs are `data_id`. OpenAPI describes it as: Get Google maps Photos data, including related metadata, for visual location research and listing QA.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `maps/photos`
- Group family: Google SERP
- Skill slug: `justserpapi-google-maps-photos`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `mapsPhotos` | `v1` | `GET` | `/api/v1/google/maps/photos` | Photos |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `category_id` | `query` | n/a | all | `string` | The unique ID for a photo category (e.g., 'Interior', 'Exterior'). Found in previous Maps Photos API responses |
| `data_id` | `query` | all | n/a | `string` | The unique Google Maps location ID (feature ID). You can get this from our Google Maps Search API |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `next_page_token` | `query` | n/a | all | `string` | Token for retrieving the next page of photo results |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `mapsPhotos` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `mapsPhotos`.

```bash
node {baseDir}/bin/run.mjs --operation "mapsPhotos" --api-key "$JUST_SERP_API_KEY" --params-json '{"data_id":"<data_id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_photos&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_photos&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `mapsPhotos` on `/api/v1/google/maps/photos`.
- Echo the required lookup scope (`data_id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google maps Photos data, including related metadata, for visual location research and listing QA.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
