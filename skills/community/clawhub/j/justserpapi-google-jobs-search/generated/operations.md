# Google SERP Jobs Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `jobs/search`.

## `jobsSearch`

- Method: `GET`
- Path: `/api/v1/google/jobs/search`
- Summary: Search
- Description: Get Google jobs Search data, including titles, companies, and locations, for aggregating job board results, analyzing hiring trends, and monitoring recruitment activity.
- Tags: `Google Jobs`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The job search query (e.g., 'software engineer', 'data scientist London'). |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `next_page_token` | `query` | no | `string` | n/a | Token for retrieving the next page of job results. Found in 'next_page_token' of a previous response. |
| `chips` | `query` | no | `string` | n/a | Additional search filters (chips) such as job type, date posted, etc. Use values returned in previous responses. |
| `lrad` | `query` | no | `string` | n/a | Search radius in miles around the specified location. |
| `ltype` | `query` | no | `string` | n/a | Filter by job location type. Set to '1' for work-from-home (remote) jobs. |
| `uds` | `query` | no | `string` | n/a | Advanced Google-provided filter string for job results. |
| `uule` | `query` | no | `string` | n/a | Encoded location string (UULE) to localize job results to a specific geographic area. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
