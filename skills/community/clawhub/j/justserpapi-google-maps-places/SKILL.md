---
name: Google SERP Maps Places API
description: Call GET /api/v1/google/maps/places for Google SERP Maps Places through Just Serp API.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_maps_places"}}
---

# Google SERP Maps Places

Use this focused Just Serp API skill for Google SERP Maps Places. It targets `GET /api/v1/google/maps/places`. It has no required request parameters. OpenAPI describes it as: Get Google maps Place Details data, including contact details and business information, for enrich business directories, look up place details, and sync local app data.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `maps/places`
- Group family: Google SERP
- Skill slug: `justserpapi-google-maps-places`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `mapsPlaces` | `v1` | `GET` | `/api/v1/google/maps/places` | Place Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `country` | `query` | n/a | all | `string` | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a> |
| `data_id` | `query` | n/a | all | `string` | The unique Google Maps location data ID. Use this or 'place_id' |
| `place_id` | `query` | n/a | all | `string` | The unique Google Place ID. Obtainable via the Google Maps Search API. Use this or 'data_id' |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `mapsPlaces` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `mapsPlaces`.

```bash
node {baseDir}/bin/run.mjs --operation "mapsPlaces" --api-key "$JUST_SERP_API_KEY" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_maps_places&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `mapsPlaces` on `/api/v1/google/maps/places`.
- Prioritize fields that support this endpoint purpose: Get Google maps Place Details data, including contact details and business information, for enrich business directories, look up place details, and sync local app data.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
