# TikTok Post Details operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `get-post-detail`.

## `getTiktokPostDetailV1`

- Method: `GET`
- Path: `/api/tiktok/get-post-detail/v1`
- Summary: Post Details
- Description: Get TikTok post Details data, including video ID, author information, and description text, for content performance analysis and metadata extraction and influencer evaluation via specific post metrics.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `postId` | `query` | yes | `string` | n/a | The unique ID of the TikTok post. |

### Request body

No request body.

### Responses

- `200`: OK
