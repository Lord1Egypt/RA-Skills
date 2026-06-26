# Douyin (TikTok China) Video Details operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `get-video-detail`.

## `getDouyinVideoDetailV2`

- Method: `GET`
- Path: `/api/douyin/get-video-detail/v2`
- Summary: Video Details
- Description: Get Douyin (TikTok China) video Details data, including author details, publish time, and engagement counts, for video research, archiving, and performance analysis.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `videoId` | `query` | yes | `string` | n/a | The unique video identifier (aweme_id or model_id). |

### Request body

No request body.

### Responses

- `200`: OK
