# TikTok Post Comments operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `get-post-comment`.

## `getPostCommentV1`

- Method: `GET`
- Path: `/api/tiktok/get-post-comment/v1`
- Summary: Post Comments
- Description: Get TikTok post Comments data, including comment ID, user information, and text content, for sentiment analysis of the audience's reaction to specific content and engagement measurement via comment volume and quality.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `awemeId` | `query` | yes | `string` | n/a | The unique ID of the TikTok post (awemeId). |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Start with '0'. |

### Request body

No request body.

### Responses

- `200`: OK
