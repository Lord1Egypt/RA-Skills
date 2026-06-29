# Google SERP Immersive Product operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `immersive/product`.

## `immersiveProduct`

- Method: `GET`
- Path: `/api/v1/google/immersive/product`
- Summary: Details
- Description: Get Google immersive Product data, including features, specifications, and seller information, for product research and merchandising analysis.
- Tags: `Google Immersive Product`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `page_token` | `query` | yes | `string` | n/a | The unique token used to retrieve detailed product information in Google's immersive view. This token is typically found in Google Shopping or Search results. |
| `stores` | `query` | no | `boolean` | n/a | If set to true, the API will retrieve a list of more sellers for the product. Use this together with the 'sori' parameter. |
| `sori` | `query` | no | `integer` | n/a | Pagination offset for seller results. Set this to the number of sellers already retrieved to get the next set. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
