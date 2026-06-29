# Google SERP Maps Places operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `maps/places`.

## `mapsPlaces`

- Method: `GET`
- Path: `/api/v1/google/maps/places`
- Summary: Place Details
- Description: Get Google maps Place Details data, including contact details and business information, for enrich business directories, look up place details, and sync local app data.
- Tags: `Google Maps`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `place_id` | `query` | no | `string` | n/a | The unique Google Place ID. Obtainable via the Google Maps Search API. Use this or 'data_id'. |
| `data_id` | `query` | no | `string` | n/a | The unique Google Maps location data ID. Use this or 'place_id'. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
