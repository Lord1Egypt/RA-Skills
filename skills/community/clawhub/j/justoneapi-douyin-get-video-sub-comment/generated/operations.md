# Douyin (TikTok China) Comment Replies operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `get-video-sub-comment`.

## `getVideoSubCommentV1`

- Method: `GET`
- Path: `/api/douyin/get-video-sub-comment/v1`
- Summary: Comment Replies
- Description: Get Douyin (TikTok China) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `commentId` | `query` | yes | `string` | n/a | The unique identifier of the top-level comment. |
| `page` | `query` | no | `integer` | `1` | Page number (starting from 1). |

### Request body

No request body.

### Responses

- `200`: OK
