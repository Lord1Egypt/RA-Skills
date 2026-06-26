# Kuaishou operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

## `getUserProfileV1`

- Method: `GET`
- Path: `/api/kuaishou/get-user-detail/v1`
- Summary: User Profile
- Description: Get Kuaishou user Profile data, including account metadata, audience metrics, and verification-related fields, for creator research and building creator profiles and monitoring audience growth and account status.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | The unique user ID on Kuaishou. |

### Request body

No request body.

### Responses

- `200`: OK

## `getKuaishouUserVideoListV2`

- Method: `GET`
- Path: `/api/kuaishou/get-user-video-list/v2`
- Summary: User Published Videos
- Description: Get Kuaishou user Published Videos data, including covers, publish times, and engagement metrics, for creator monitoring and content performance analysis.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | The unique user ID on Kuaishou. |
| `pcursor` | `query` | no | `string` | n/a | Pagination cursor for subsequent pages. |

### Request body

No request body.

### Responses

- `200`: OK

## `getVideoCommentsV1`

- Method: `GET`
- Path: `/api/kuaishou/get-video-comment/v1`
- Summary: Video Comments
- Description: Retrieves public comments of a Kuaishou video, including comment content,
author info, like count, and reply count.

Typical use cases:
- Sentiment analysis and community feedback monitoring
- Gathering engagement data for specific videos
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `videoId` | `query` | yes | `string` | n/a | The unique ID of the Kuaishou video, e.g. `3xbknvct79h46h9` or refer_photo_id `177012131237` |
| `pcursor` | `query` | no | `string` | n/a | Pagination cursor for subsequent pages. |

### Request body

No request body.

### Responses

- `200`: OK

## `getVideoDetailsV2`

- Method: `GET`
- Path: `/api/kuaishou/get-video-detail/v2`
- Summary: Video Details
- Description: Get Kuaishou video Details data, including video URL, caption, and author info, for in-depth content performance analysis and building databases of viral videos.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `videoId` | `query` | yes | `string` | n/a | The unique ID of the Kuaishou video, e.g. `3xg9avuebhtfcku` |

### Request body

No request body.

### Responses

- `200`: OK

## `searchKuaishouUserV2`

- Method: `GET`
- Path: `/api/kuaishou/search-user/v2`
- Summary: User Search
- Description: Get Kuaishou user Search data, including profile names, avatars, and follower counts, for creator discovery and account research.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword to find users. |
| `page` | `query` | no | `integer` | `1` | Page number for results, starting from 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchKuaishouVideoV2`

- Method: `GET`
- Path: `/api/kuaishou/search-video/v2`
- Summary: Video Search
- Description: Get Kuaishou video Search data, including video ID, cover image, and description, for competitive analysis and market trends and keywords monitoring and brand tracking.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword to find videos. |
| `page` | `query` | no | `integer` | `1` | Page number for results, starting from 1. |

### Request body

No request body.

### Responses

- `200`: OK

## `shareLinkResolutionV1`

- Method: `GET`
- Path: `/api/kuaishou/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Kuaishou share Link Resolution data, including resolved content identifier and target object data, for resolving shared links for automated content processing.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shareUrl` | `query` | yes | `string` | n/a | Kuaishou share URL (must start with 'https://v.kuaishou.com/'). |

### Request body

No request body.

### Responses

- `200`: OK
