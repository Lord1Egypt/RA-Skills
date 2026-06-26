# Bilibili Video Details operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-video-detail`.

## `getBilibiliVideoDetailV2`

- Method: `GET`
- Path: `/api/bilibili/get-video-detail/v2`
- Summary: Video Details
- Description: Get Bilibili video Details data, including metadata (title, tags, and publishing time), for tracking video performance and engagement metrics and analyzing content metadata and uploader information.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `bvid` | `query` | yes | `string` | n/a | Bilibili Video ID (BVID). |

### Request body

No request body.

### Responses

- `200`: OK
