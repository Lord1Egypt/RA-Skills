# Reddit Post Details operations

Generated from JustOneAPI OpenAPI for platform key `reddit`.

Endpoint group: `get-post-detail`.

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
