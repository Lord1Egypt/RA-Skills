# Weibo operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

## `getFansV1`

- Method: `GET`
- Path: `/api/weibo/get-fans/v1`
- Summary: User Fans
- Description: Get Weibo user Fans data, including profile metadata and verification signals, for audience analysis and influencer research.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `getFollowersV1`

- Method: `GET`
- Path: `/api/weibo/get-followers/v1`
- Summary: User Followers
- Description: Get Weibo user Followers data, including profile metadata and verification signals, for network analysis and creator research.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `getWeiboPostCommentsV1`

- Method: `GET`
- Path: `/api/weibo/get-post-comments/v1`
- Summary: Post Comments
- Description: Get Weibo post Comments data, including text, authors, and timestamps, for feedback analysis.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `mid` | `query` | yes | `string` | n/a | Weibo post mid. |
| `sort` | `query` | no | `string` | `TIME` | Sort order for the result set.

Available Values:
- `TIME`: Time
- `HOT`: Hot |
| enum | values | no | n/a | n/a | `TIME`, `HOT` |
| `maxId` | `query` | no | `string` | n/a | Pagination cursor returned by the previous response. |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserProfileV3`

- Method: `GET`
- Path: `/api/weibo/get-user-detail/v3`
- Summary: User Profile
- Description: Get Weibo user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserPublishedPostsV1`

- Method: `GET`
- Path: `/api/weibo/get-user-post/v1`
- Summary: User Published Posts
- Description: Get Weibo user Published Posts data, including text, media, and publish times, for account monitoring.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |
| `sinceId` | `query` | no | `string` | n/a | Pagination cursor (since_id). Required if page > 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `getWeiboUserVideoListV1`

- Method: `GET`
- Path: `/api/weibo/get-user-video-list/v1`
- Summary: User Video List
- Description: Get Weibo user Video list data (waterfall), including pagination cursor for next page.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor returned by the previous response. |

### Request body

No request body.

### Responses

- `200`: OK

## `getWeiboDetailsV1`

- Method: `GET`
- Path: `/api/weibo/get-weibo-detail/v1`
- Summary: Post Details
- Description: Get Weibo post Details data, including media, author metadata, and engagement counts, for post analysis, archiving, and campaign monitoring.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `id` | `query` | yes | `string` | n/a | Weibo post ID. |

### Request body

No request body.

### Responses

- `200`: OK

## `hotSearchV1`

- Method: `GET`
- Path: `/api/weibo/hot-search/v1`
- Summary: Hot Search
- Description: Get Weibo hot Search data, including ranking data, for trend monitoring, newsroom workflows, and topic discovery.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchAllV2`

- Method: `GET`
- Path: `/api/weibo/search-all/v2`
- Summary: Keyword Search
- Description: Get Weibo keyword Search data, including authors, publish times, and engagement signals, for trend monitoring.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `q` | `query` | yes | `string` | n/a | Search Keywords. |
| `startDay` | `query` | yes | `string` | n/a | Start Day (yyyy-MM-dd). |
| `startHour` | `query` | yes | `integer` | n/a | Start Hour (0-23). |
| `endDay` | `query` | yes | `string` | n/a | End Day (yyyy-MM-dd). |
| `endHour` | `query` | yes | `integer` | n/a | End Hour (0-23). |
| `hotSort` | `query` | no | `boolean` | `false` | Hot sort, true for hot sort, false for time sort. Default is false. |
| `contains` | `query` | no | `string` | `ALL` | Contains filter for the result set.

Available Values:
- `ALL`: All
- `PICTURE`: Has Picture
- `VIDEO`: Has Video
- `MUSIC`: Has Music
- `LINK`: Has Link |
| enum | values | no | n/a | n/a | `ALL`, `PICTURE`, `VIDEO`, `MUSIC`, `LINK` |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchProfileV1`

- Method: `GET`
- Path: `/api/weibo/search-profile/v1`
- Summary: Search User Published Posts
- Description: Get Weibo search User Published Posts data, including matched results, metadata, and ranking signals, for author research and historical content discovery.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `q` | `query` | yes | `string` | n/a | Search Keywords. |
| `startDay` | `query` | no | `string` | n/a | Start Day (yyyy-MM-dd). |
| `endDay` | `query` | no | `string` | n/a | End Day (yyyy-MM-dd). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `tvComponentV1`

- Method: `GET`
- Path: `/api/weibo/tv-component/v1`
- Summary: TV Video Details
- Description: Get Weibo tV Video Details data, including media URLs, author details, and engagement counts, for video research, archiving, and performance analysis.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `oid` | `query` | yes | `string` | n/a | Weibo video/object ID. |

### Request body

No request body.

### Responses

- `200`: OK
