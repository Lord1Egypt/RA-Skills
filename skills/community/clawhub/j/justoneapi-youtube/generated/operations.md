# YouTube operations

Generated from JustOneAPI OpenAPI for platform key `youtube`.

## `getChannelVideosV1`

- Method: `GET`
- Path: `/api/youtube/get-channel-videos/v1`
- Summary: Channel Videos
- Description: Retrieve a list of videos from a specific YouTube channel, providing detailed insights into content performance and upload history.
- Tags: `YouTube`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `channelId` | `query` | yes | `string` | n/a | The unique identifier for a YouTube channel. |
| `cursor` | `query` | no | `string` | n/a | The cursor for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

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
