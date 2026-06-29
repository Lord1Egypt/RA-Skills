# Google SERP Ai Mode operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `ai-mode`.

## `aiMode`

- Method: `GET`
- Path: `/api/v1/google/ai-mode`
- Summary: Mode
- Description: Get Google aI Mode data, including generated answers, follow-up prompts, and cited links, for AI search experience monitoring.
- Tags: `Google AI`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for Google Search (e.g., 'coffee shops', 'how to bake a cake'). |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `uule` | `query` | no | `string` | n/a | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it. |
| `location` | `query` | no | `string` | n/a | The textual location name (e.g., 'New York, NY') to localize the search results. |
| `safe` | `query` | no | `string` | n/a | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
