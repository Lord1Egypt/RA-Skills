# Bilibili Video Comments operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-video-comment`.

## `getVideoCommentV2`

- Method: `GET`
- Path: `/api/bilibili/get-video-comment/v2`
- Summary: Video Comments
- Description: Get Bilibili video Comments data, including commenter profiles, text, and likes, for sentiment analysis and comment moderation workflows.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `aid` | `query` | yes | `string` | n/a | Bilibili Archive ID (AID). |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor. |

### Request body

No request body.

### Responses

- `200`: OK
