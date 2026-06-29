# Google SERP Maps Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `maps/search`.

## `mapsSearch`

- Method: `GET`
- Path: `/api/v1/google/maps/search`
- Summary: Search
- Description: Get Google maps Search data, including business listings, ratings and contact data, and coordinate and location targeting, for local market research and lead discovery.
- Tags: `Google Maps`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for Google Maps (e.g., 'restaurants', 'hospitals in New York'). |
| `ll` | `query` | no | `string` | n/a | GPS coordinates for the search origin. Format: '@<latitude>,<longitude>,<zoom>'. Required for precise localization and pagination. |
| `domain` | `query` | no | `string` | n/a | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `data` | `query` | no | `string` | n/a | Advanced Google Maps data parameter used for certain map/place-specific result filters and views. It can be copied from a Google Maps URL after applying filters, or constructed for specific place searches. This parameter is commonly used when type = "place". If you’re not familiar with it, you can leave it empty. |
| `place_id` | `query` | no | `string` | n/a | The unique Google Place ID to directly retrieve information for a specific location. |
| `page` | `query` | no | `integer` | n/a | The results pagination offset. Start at 0 and increment by 20 for each subsequent page. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
