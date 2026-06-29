---
name: Google SERP Maps Search API
description: Call GET /api/v1/google/maps/search for Google SERP Maps Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_maps_search"}}
---

# Google SERP Maps Search

Use this focused Just Serp API skill for Google SERP Maps Search. It targets `GET /api/v1/google/maps/search`. Required inputs are `query`. OpenAPI describes it as: Get Google maps Search data, including business listings, ratings and contact data, and coordinate and location targeting, for local market research and lead discovery.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `maps/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-maps-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `mapsSearch` | `v1` | `GET` | `/api/v1/google/maps/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `data` | `query` | n/a | all | `string` | Advanced Google Maps data parameter used for certain map/place-specific result filters and views. It can be copied from a Google Maps URL after applying filters, or constructed for specific place searches. This parameter is commonly used when type = "place". If you’re not familiar with it, you can leave it empty |
| `domain` | `query` | n/a | all | `string` | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a> |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `ll` | `query` | n/a | all | `string` | GPS coordinates for the search origin. Format: '@<latitude>,<longitude>,<zoom>'. Required for precise localization and pagination |
| `page` | `query` | n/a | all | `integer` | The results pagination offset. Start at 0 and increment by 20 for each subsequent page |
| `place_id` | `query` | n/a | all | `string` | The unique Google Place ID to directly retrieve information for a specific location |
| `query` | `query` | all | n/a | `string` | The search query for Google Maps (e.g., 'restaurants', 'hospitals in New York') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `mapsSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `mapsSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "mapsSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `mapsSearch` on `/api/v1/google/maps/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google maps Search data, including business listings, ratings and contact data, and coordinate and location targeting, for local market research and lead discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
