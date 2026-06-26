# Douyin (TikTok China) Video Comments operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `get-video-comment`.

## `getVideoCommentV1`

- Method: `GET`
- Path: `/api/douyin/get-video-comment/v1`
- Summary: Video Comments
- Description: Get Douyin (TikTok China) video Comments data, including authors, text, and likes, for sentiment analysis and engagement review.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `awemeId` | `query` | yes | `string` | n/a | The unique video identifier (aweme_id). |
| `page` | `query` | no | `integer` | `1` | Page number (starting from 1). |

### Request body

No request body.

### Responses

- `200`: OK
