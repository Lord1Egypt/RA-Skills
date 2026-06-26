# Reddit Keyword Search operations

Generated from JustOneAPI OpenAPI for platform key `reddit`.

Endpoint group: `search`.

## `searchRedditV1`

- Method: `GET`
- Path: `/api/reddit/search/v1`
- Summary: Keyword Search
- Description: Get Reddit keyword Search data, including titles, authors, and subreddit context, for topic discovery and monitoring.
- Tags: `Reddit`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search query keywords. |
| `after` | `query` | no | `string` | n/a | Pagination token to retrieve the next set of results. |

### Request body

No request body.

### Responses

- `200`: OK
