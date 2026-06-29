# Google SERP Trends Autocomplete operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `trends/autocomplete`.

## `TrendsAutocomplete`

- Method: `GET`
- Path: `/api/v1/google/trends/autocomplete`
- Summary: Autocomplete
- Description: Get Google trends Autocomplete data, including topic IDs, for trend discovery and topic expansion.
- Tags: `Google Trends`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query to get trending autocomplete suggestions for (e.g., 'artificial'). |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
