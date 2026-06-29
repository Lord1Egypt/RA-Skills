# Google SERP Shorts Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `shorts/search`.

## `shortsSearch`

- Method: `GET`
- Path: `/api/v1/google/shorts/search`
- Summary: Search
- Description: Get Google shorts Search data, including video metadata and rankings, for short-form content tracking and trend analysis.
- Tags: `Google Shorts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for Google Shorts (e.g., 'cooking tips', 'travel hacks'). |
| `start` | `query` | no | `integer` | n/a | The result offset to skip a specific number of entries (e.g., set to 12 to skip the first 12 results). |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `domain` | `query` | no | `string` | n/a | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `lr` | `query` | no | `string` | n/a | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a>. |
| `uule` | `query` | no | `string` | n/a | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it. |
| `tbs` | `query` | no | `string` | n/a | Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty. |
| `safe` | `query` | no | `string` | n/a | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it. |
| `nfpr` | `query` | no | `string` | n/a | Controls Google's auto-correction. Set to '1' to exclude corrected results, '0' to include them. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
