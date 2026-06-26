# Douyin (TikTok China) operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

## `getUserDetailV3`

- Method: `GET`
- Path: `/api/douyin/get-user-detail/v3`
- Summary: User Profile
- Description: Get Douyin (TikTok China) user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `secUid` | `query` | yes | `string` | n/a | The unique user ID (sec_uid) on Douyin. |

### Request body

No request body.

### Responses

- `200`: OK

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

## `searchDouyinUserV2`

- Method: `GET`
- Path: `/api/douyin/search-user/v2`
- Summary: User Search
- Description: Get Douyin (TikTok China) user Search data, including profile metadata and follower signals, for creator discovery and account research.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number (starting from 1). |
| `userType` | `query` | no | `string` | n/a | Filter by user type.

Available Values:
- `common_user`: Common User
- `enterprise_user`: Enterprise User
- `personal_user`: Verified Individual User |
| enum | values | no | n/a | n/a | `common_user`, `enterprise_user`, `personal_user` |

### Request body

No request body.

### Responses

- `200`: OK

## `searchVideoV4`

- Method: `GET`
- Path: `/api/douyin/search-video/v4`
- Summary: Video Search
- Description: Get Douyin (TikTok China) video Search data, including metadata and engagement signals, for content discovery, trend research, and competitive monitoring.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword. |
| `sortType` | `query` | no | `string` | `_0` | Sorting criteria for search results.

Available Values:
- `_0`: General
- `_1`: More likes
- `_2`: Newest |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2` |
| `publishTime` | `query` | no | `string` | `_0` | Filter by video publish time range.

Available Values:
- `_0`: No Limit
- `_1`: Last 24 Hours
- `_7`: Last 7 Days
- `_180`: Last 6 Months |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_7`, `_180` |
| `duration` | `query` | no | `string` | `_0` | Filter by video duration.

Available Values:
- `_0`: No Limit
- `_1`: Under 1 Minute
- `_2`: 1-5 Minutes
- `_3`: Over 5 Minutes |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2`, `_3` |
| `page` | `query` | no | `integer` | `1` | Page number (starting from 1). |
| `searchId` | `query` | no | `string` | n/a | Search ID; required for pages > 1 (use the search_id value returned by the last response). |

### Request body

No request body.

### Responses

- `200`: OK

## `shareDouyinUrlTransferV1`

- Method: `GET`
- Path: `/api/douyin/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Douyin (TikTok China) share Link Resolution data, including helping extract canonical IDs, for downstream video and comment workflows.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shareUrl` | `query` | yes | `string` | n/a | The Douyin short share URL. |

### Request body

No request body.

### Responses

- `200`: OK
