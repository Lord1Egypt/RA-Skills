# YOUKU Video Details operations

Generated from JustOneAPI OpenAPI for platform key `youku`.

Endpoint group: `get-video-detail`.

## `getYoukuVideoDetailV1`

- Method: `GET`
- Path: `/api/youku/get-video-detail/v1`
- Summary: Video Details
- Description: Get YOUKU video Details data, including video ID, title, and description, for fetching comprehensive metadata for a single video, tracking engagement metrics like play counts and likes, and integrating detailed video info into third-party dashboards.
- Tags: `YOUKU`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `videoId` | `query` | yes | `string` | n/a | The unique identifier for the video. |

### Request body

No request body.

### Responses

- `200`: OK
