# Google SERP Scholar Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `scholar/search`.

## `ScholarSearch`

- Method: `GET`
- Path: `/api/v1/google/scholar/search`
- Summary: Search
- Description: Get Google scholar Search data, including papers, patents, and legal docs, citation and year filters, and versions and cited-by links, for literature review and academic result monitoring.
- Tags: `Google Scholar`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The academic search query (e.g., 'machine learning', 'CRISPR gene editing'). Supports advanced operators like 'author:'. |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google Scholar search page. |
| `cites` | `query` | no | `string` | n/a | Return articles that cite the article with the specified ID. |
| `as_ylo` | `query` | no | `string` | n/a | Minimum publication year filter (e.g., '2020'). |
| `as_yhi` | `query` | no | `string` | n/a | Maximum publication year filter (e.g., '2024'). |
| `scisbd` | `query` | no | `string` | n/a | Controls whether to return only abstract results (1) or all results (0). |
| `cluster` | `query` | no | `string` | n/a | The unique ID of an article cluster to retrieve all versions of a specific work. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `lr` | `query` | no | `string` | n/a | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a>. |
| `page` | `query` | no | `integer` | n/a | The results page number. Use 0 for the first page, 1 for the second, and so on. |
| `results` | `query` | no | `integer` | n/a | The number of search results to return per page. |
| `as_sdt` | `query` | no | `string` | n/a | Advanced filter for specific document types or legal jurisdictions. E.g., '7' to include patents. |
| `safe` | `query` | no | `string` | n/a | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it. |
| `filter` | `query` | no | `string` | n/a | Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable. |
| `as_vis` | `query` | no | `string` | n/a | Controls whether citations are included in the results: 1 = exclude, 0 (default) = include. |
| `as_rr` | `query` | no | `string` | n/a | Controls whether to show only review articles (topic overviews or discussions of the searched works/authors). Set to 1 to enable the filter, or 0 (default) to return all results. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
