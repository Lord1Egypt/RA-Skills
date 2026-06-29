# Google SERP Search Light operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `search/light`.

## `searchLight`

- Method: `GET`
- Path: `/api/v1/google/search/light`
- Summary: Light Search
- Description: Get Google light Search SERP data, including essential result data, for high-volume monitoring and fast rank checks.
- Tags: `Google`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for Google Search (e.g., 'coffee shops', 'how to bake a cake'). |
| `page` | `query` | no | `integer` | n/a | The results page number. Use 0 for the first page, 1 for the second, and so on. |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `lr` | `query` | no | `string` | n/a | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a>. |
| `domain` | `query` | no | `string` | n/a | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a>. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `cr` | `query` | no | `string` | n/a | Limits results to search results from specific countries. Format: 'countryXX'. See <a href="/reference/google-cr-countries">Google CR Countries</a>. |
| `uule` | `query` | no | `string` | n/a | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it. |
| `location` | `query` | no | `string` | n/a | The textual location name (e.g., 'New York, NY') to localize the search results. |
| `ludocid` | `query` | no | `string` | n/a | Google local business CID (place identifier). Used to target a specific Google Business Profile / local listing. Advanced parameter — if you don’t know it, you can omit it. |
| `lsig` | `query` | no | `string` | n/a | Signature parameter (lsig) sometimes required for certain Knowledge Graph / local map view features. This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty. |
| `kgmid` | `query` | no | `string` | n/a | Knowledge Graph entity/listing ID (KGMID) used to retrieve details for a specific entity. This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty. |
| `si` | `query` | no | `string` | n/a | Cached search context parameter (si) used to reproduce specific Google search result views/context (e.g. some Knowledge Graph tabs). This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty. |
| `ibp` | `query` | no | `string` | n/a | Parameter (ibp) used to control certain Google UI expansions or rendering modes (commonly in local/business result views). This is an advanced technical parameter — if you’re not familiar with it, you can leave it empty. |
| `uds` | `query` | no | `string` | n/a | Advanced filter token (uds) used for specific Google search sub-filters. This is an advanced technical parameter, usually provided by Google in filter options/results — if you’re not familiar with it, you can leave it empty. |
| `tbs` | `query` | no | `string` | n/a | Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty. |
| `safe` | `query` | no | `string` | n/a | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it. |
| `nfpr` | `query` | no | `string` | n/a | Controls Google's auto-correction. Set to '1' to exclude corrected results, '0' to include them. |
| `filter` | `query` | no | `string` | n/a | Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
