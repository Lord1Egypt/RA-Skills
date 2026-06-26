# YOUKU operations

Generated from JustOneAPI OpenAPI for platform key `youku`.

## `getYoukuUserDetailV1`

- Method: `GET`
- Path: `/api/youku/get-user-detail/v1`
- Summary: User Profile
- Description: Get YOUKU user Profile data, including user ID, username, and avatar, for analyzing creator influence and audience size, monitoring account growth and verification status, and fetching basic user info for social crm.
- Tags: `YOUKU`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `uid` | `query` | yes | `string` | n/a | The unique identifier for the user. |

### Request body

No request body.

### Responses

- `200`: OK

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

## `searchVideoV1`

- Method: `GET`
- Path: `/api/youku/search-video/v1`
- Summary: Video Search
- Description: Get YOUKU video Search data, including video ID, title, and cover image, for keyword-based video discovery, monitoring specific topics or trends on youku, and analyzing search results for market research.
- Tags: `YOUKU`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `keyword` | `query` | yes | `string` | n/a | Keyword to search for. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination, starting from 1. |

### Request body

No request body.

### Responses

- `200`: OK
