# TikTok Comment Replies operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `get-post-sub-comment`.

## `getPostSubCommentV1`

- Method: `GET`
- Path: `/api/tiktok/get-post-sub-comment/v1`
- Summary: Comment Replies
- Description: Get TikTok comment Replies data, including reply ID, user information, and text content, for understanding detailed user interactions and threaded discussions and identifying influencers or active participants within a comment section.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `awemeId` | `query` | yes | `string` | n/a | The unique ID of the TikTok post. |
| `commentId` | `query` | yes | `string` | n/a | The unique ID of the comment to retrieve replies for. |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Start with '0'. |

### Request body

No request body.

### Responses

- `200`: OK
