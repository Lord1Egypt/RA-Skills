# Bilibili operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

## `getUserDetailV2`

- Method: `GET`
- Path: `/api/bilibili/get-user-detail/v2`
- Summary: User Profile
- Description: Get Bilibili user Profile data, including account metadata, audience metrics, and verification-related fields, for analyzing creator's profile, level, and verification status and verifying user identity and social presence on bilibili.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `uid` | `query` | yes | `string` | n/a | Bilibili User ID (UID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserRelationStat`

- Method: `GET`
- Path: `/api/bilibili/get-user-relation-stat/v1`
- Summary: User Relation Stats
- Description: Get Bilibili user Relation Stats data, including following counts, for creator benchmarking and audience growth tracking.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `wmid` | `query` | yes | `string` | n/a | Bilibili User ID (WMID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getBilibiliUserVideoListV2`

- Method: `GET`
- Path: `/api/bilibili/get-user-video-list/v2`
- Summary: User Published Videos
- Description: Get Bilibili user Published Videos data, including titles, covers, and publish times, for creator monitoring and content performance analysis.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `uid` | `query` | yes | `string` | n/a | Bilibili User ID (UID). |
| `param` | `query` | no | `string` | n/a | Pagination parameter from previous response. |

### Request body

No request body.

### Responses

- `200`: OK

## `getVideoCaptionV1`

- Method: `GET`
- Path: `/api/bilibili/get-video-caption/v2`
- Summary: Video Captions
- Description: Get Bilibili video Captions data, including caption data, for transcript extraction and multilingual content analysis.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `bvid` | `query` | yes | `string` | n/a | Bilibili Video ID (BVID). |
| `aid` | `query` | yes | `string` | n/a | Bilibili AID. |
| `cid` | `query` | yes | `string` | n/a | Bilibili CID. |

### Request body

No request body.

### Responses

- `200`: OK

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

## `getVideoDanmuV2`

- Method: `GET`
- Path: `/api/bilibili/get-video-danmu/v2`
- Summary: Video Danmaku
- Description: Get Bilibili video Danmaku data, including timeline positions and comment text, for audience reaction analysis and subtitle-style comment review.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `aid` | `query` | yes | `string` | n/a | Bilibili Archive ID (AID). |
| `cid` | `query` | yes | `string` | n/a | Bilibili Chat ID (CID). |
| `page` | `query` | no | `string` | n/a | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

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

## `searchBilibiliVideoV2`

- Method: `GET`
- Path: `/api/bilibili/search-video/v2`
- Summary: Video Search
- Description: Get Bilibili video Search data, including matched videos, creators, and engagement metrics, for topic research and content discovery.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `page` | `query` | no | `string` | n/a | Page number for pagination. |
| `order` | `query` | no | `string` | `general` | Sorting criteria for search results.

Available Values:
- `general`: General
- `click`: Most Played
- `pubdate`: Latest
- `dm`: Most Danmaku
- `stow`: Most Favorite |
| enum | values | no | n/a | n/a | `general`, `click`, `pubdate`, `dm`, `stow` |

### Request body

No request body.

### Responses

- `200`: OK

## `shareBilibiliUrlTransferV1`

- Method: `GET`
- Path: `/api/bilibili/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Bilibili share Link Resolution data, including resolved video and page identifier, for converting shortened mobile share links to standard bvid/metadata and automating content extraction from shared social media links.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `shareUrl` | `query` | yes | `string` | n/a | Bilibili share URL (must start with https://b23.tv/). |

### Request body

No request body.

### Responses

- `200`: OK
