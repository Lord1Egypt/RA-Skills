# Google SERP Patents Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `patents/search`.

## `patentSearch`

- Method: `GET`
- Path: `/api/v1/google/patents/search`
- Summary: Search
- Description: Get Google patent Search data, including filters, for patent discovery and portfolio monitoring.
- Tags: `Google Patent`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for patents (e.g., 'autonomous vehicles', 'blockchain security'). |
| `page` | `query` | no | `integer` | n/a | The results page number. Use 0 for the first page, 1 for the second, and so on. |
| `num` | `query` | no | `integer` | n/a | The number of results to return per page (range: 1-100). |
| `sort` | `query` | no | `string` | n/a | Sorting order for patent results. Supported values: 'new' (Newest), 'old' (Oldest). |
| `clustered` | `query` | no | `boolean` | n/a | If set to true, results will be grouped by classification. |
| `dups` | `query` | no | `string` | n/a | Deduplication method. Supported values: 'language' (by Publication). |
| `patents` | `query` | no | `boolean` | n/a | Whether to include Google Patents results. |
| `scholar` | `query` | no | `boolean` | n/a | Whether to include Google Scholar results. |
| `before` | `query` | no | `string` | n/a | Latest date to include. Format: 'type:YYYYMMDD' (e.g., 'publication:20230101'). |
| `after` | `query` | no | `string` | n/a | Earliest date to include. Format: 'type:YYYYMMDD' (e.g., 'filing:20200101'). |
| `inventor` | `query` | no | `string` | n/a | Filter by patent inventor(s). Multiple values can be comma-separated. |
| `assignee` | `query` | no | `string` | n/a | Filter by patent assignee(s). Multiple values can be comma-separated. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `status` | `query` | no | `string` | n/a | Filter by patent status. Supported values: 'GRANT', 'APPLICATION'. |
| `type` | `query` | no | `string` | n/a | Filter by patent type. Supported values: 'PATENT', 'DESIGN'. |
| `litigation` | `query` | no | `string` | n/a | Filter by litigation status. Supported values: 'YES', 'NO'. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
