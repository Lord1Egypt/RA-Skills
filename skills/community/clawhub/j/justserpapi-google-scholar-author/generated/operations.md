# Google SERP Scholar Author operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `scholar/author`.

## `ScholarAuthor`

- Method: `GET`
- Path: `/api/v1/google/scholar/author`
- Summary: Author
- Description: Get Google scholar Author data, including publications, citation metrics, and research interests, for researcher analysis and academic profiling.
- Tags: `Google Scholar`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `author_id` | `query` | yes | `string` | n/a | The unique Google Scholar ID of the researcher/author (e.g., 'LSs6DR8AAAAJ'). |
| `results` | `query` | no | `integer` | n/a | The number of results to return per page. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `view_op` | `query` | no | `string` | n/a | Specific view operation for the author profile. Use 'list_colleagues' to see co-authors or 'view_citation' for article details. |
| `sort` | `query` | no | `string` | n/a | Sorting criteria for the author's publications. Supported values: 'title', 'pubdate'. |
| `citation_id` | `query` | no | `string` | n/a | The citation ID to view details for (required when 'view_op' is 'view_citation'). |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
