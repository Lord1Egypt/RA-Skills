# Google SERP Autocomplete operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `autocomplete`.

## `autocomplete`

- Method: `GET`
- Path: `/api/v1/google/autocomplete`
- Summary: Autocomplete Suggestions
- Description: Get Google autocomplete Suggestions data, including real-time suggestion data, country and language targeting, and structured suggestion lists, for keyword expansion and search intent research.
- Tags: `Google`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query to get autocomplete suggestions for. As you type, Google provides real-time predictions based on popular searches. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
