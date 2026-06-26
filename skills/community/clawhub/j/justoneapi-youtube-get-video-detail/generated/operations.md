# YouTube Video Details operations

Generated from JustOneAPI OpenAPI for platform key `youtube`.

Endpoint group: `get-video-detail`.

## `getYoutubeVideoDetailV1`

- Method: `GET`
- Path: `/api/youtube/get-video-detail/v1`
- Summary: Video Details
- Description: Get YouTube video Details data, including its title, description, and view counts, for tracking video engagement and statistics, extracting video metadata for content analysis, and verifying video availability and status.
- Tags: `YouTube`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `videoId` | `query` | yes | `string` | n/a | The unique identifier for a YouTube video. |

### Request body

No request body.

### Responses

- `200`: OK
