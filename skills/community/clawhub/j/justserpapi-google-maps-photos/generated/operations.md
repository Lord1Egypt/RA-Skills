# Google SERP Maps Photos operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `maps/photos`.

## `mapsPhotos`

- Method: `GET`
- Path: `/api/v1/google/maps/photos`
- Summary: Photos
- Description: Get Google maps Photos data, including related metadata, for visual location research and listing QA.
- Tags: `Google Maps`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `data_id` | `query` | yes | `string` | n/a | The unique Google Maps location ID (feature ID). You can get this from our Google Maps Search API. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `category_id` | `query` | no | `string` | n/a | The unique ID for a photo category (e.g., 'Interior', 'Exterior'). Found in previous Maps Photos API responses. |
| `next_page_token` | `query` | no | `string` | n/a | Token for retrieving the next page of photo results. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
