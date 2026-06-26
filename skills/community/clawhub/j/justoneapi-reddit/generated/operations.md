# Reddit operations

Generated from JustOneAPI OpenAPI for platform key `reddit`.

## `getRedditPostCommentsV1`

- Method: `GET`
- Path: `/api/reddit/get-post-comments/v1`
- Summary: Post Comments
- Description: Get Reddit post Comments data, including text, authors, and timestamps, for discussion analysis and moderation research.
- Tags: `Reddit`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `postId` | `query` | yes | `string` | n/a | The unique identifier of the Reddit post. |
| `cursor` | `query` | no | `string` | n/a | Pagination token for the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK

## `getRedditPostDetailV1`

- Method: `GET`
- Path: `/api/reddit/get-post-detail/v1`
- Summary: Post Details
- Description: Get Reddit post Details data, including author details, subreddit info, and engagement counts, for content analysis, moderation research, and monitoring.
- Tags: `Reddit`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `postId` | `query` | yes | `string` | n/a | The unique identifier of the Reddit post (e.g., 't3_1q4aqti'). |

### Request body

No request body.

### Responses

- `200`: OK

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
