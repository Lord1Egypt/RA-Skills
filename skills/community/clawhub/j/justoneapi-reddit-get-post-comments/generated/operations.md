# Reddit Post Comments operations

Generated from JustOneAPI OpenAPI for platform key `reddit`.

Endpoint group: `get-post-comments`.

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
