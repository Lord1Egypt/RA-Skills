# Douyin (TikTok China) User Published Videos operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `get-user-video-list`.

## `getUserVideoListV3`

- Method: `GET`
- Path: `/api/douyin/get-user-video-list/v3`
- Summary: User Published Videos
- Description: Get Douyin (TikTok China) user Published Videos data, including captions, covers, and publish times, for account monitoring.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `secUid` | `query` | yes | `string` | n/a | The unique user ID (sec_uid) on Douyin. |
| `maxCursor` | `query` | no | `integer` | `0` | Pagination cursor; use 0 for the first page, and the `max_cursor` from the previous response for subsequent pages. |

### Request body

No request body.

### Responses

- `200`: OK
