# Google SERP Lens operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `lens`.

## `lens`

- Method: `GET`
- Path: `/api/v1/google/lens`
- Summary: Search
- Description: Get Google lens Search data, including visual matches, product matches, and related links, for visual search analysis and product matching workflows.
- Tags: `Google Lens`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | yes | `string` | n/a | The URL of the image you want to analyze with Google Lens. Must be a publicly accessible image URL. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `product` | `query` | no | `boolean` | n/a | If set to true, the API will specifically look for product matches and shopping results. |
| `visual_matches` | `query` | no | `boolean` | n/a | If set to true, the API will return visually similar images and matches. |
| `exact_matches` | `query` | no | `boolean` | n/a | If set to true, the API will search for exact duplicates of the provided image. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
