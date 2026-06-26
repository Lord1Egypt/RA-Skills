# TikTok operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

## `getPostCommentV1`

- Method: `GET`
- Path: `/api/tiktok/get-post-comment/v1`
- Summary: Post Comments
- Description: Get TikTok post Comments data, including comment ID, user information, and text content, for sentiment analysis of the audience's reaction to specific content and engagement measurement via comment volume and quality.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `awemeId` | `query` | yes | `string` | n/a | The unique ID of the TikTok post (awemeId). |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Start with '0'. |

### Request body

No request body.

### Responses

- `200`: OK

## `getTiktokPostDetailV1`

- Method: `GET`
- Path: `/api/tiktok/get-post-detail/v1`
- Summary: Post Details
- Description: Get TikTok post Details data, including video ID, author information, and description text, for content performance analysis and metadata extraction and influencer evaluation via specific post metrics.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `postId` | `query` | yes | `string` | n/a | The unique ID of the TikTok post. |

### Request body

No request body.

### Responses

- `200`: OK

## `getPostSubCommentV1`

- Method: `GET`
- Path: `/api/tiktok/get-post-sub-comment/v1`
- Summary: Comment Replies
- Description: Get TikTok comment Replies data, including reply ID, user information, and text content, for understanding detailed user interactions and threaded discussions and identifying influencers or active participants within a comment section.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `awemeId` | `query` | yes | `string` | n/a | The unique ID of the TikTok post. |
| `commentId` | `query` | yes | `string` | n/a | The unique ID of the comment to retrieve replies for. |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Start with '0'. |

### Request body

No request body.

### Responses

- `200`: OK

## `getTiktokUserDetailV1`

- Method: `GET`
- Path: `/api/tiktok/get-user-detail/v1`
- Summary: User Profile
- Description: Get TikTok user Profile data, including nickname, unique ID, and avatar, for influencer profiling and audience analysis, account performance tracking and growth monitoring, and identifying verified status and official accounts.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `uniqueId` | `query` | no | `string` | n/a | The unique handle/username of the user (e.g., 'tiktok'). |
| `secUid` | `query` | no | `string` | n/a | The unique security ID of the user. |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserPostV1`

- Method: `GET`
- Path: `/api/tiktok/get-user-post/v1`
- Summary: User Published Posts
- Description: Get TikTok user Published Posts data, including video ID, description, and publish time, for user activity analysis and posting frequency tracking, influencer performance evaluation, and content trend monitoring for specific creators.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `secUid` | `query` | yes | `string` | n/a | The unique security ID of the TikTok user (e.g., MS4wLjABAAAAonP2...). |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Use '0' for the first page, then use the 'cursor' value returned in the previous response. |
| `sort` | `query` | no | `string` | `_0` | Sorting criteria for the user's posts.

Available Values:
- `_0`: Default (Mixed)
- `_1`: Highest Liked
- `_2`: Latest Published |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2` |

### Request body

No request body.

### Responses

- `200`: OK

## `searchPostV1`

- Method: `GET`
- Path: `/api/tiktok/search-post/v1`
- Summary: Post Search
- Description: Get TikTok post Search data, including key details such as video ID, description, and author information, for trend monitoring and content discovery and keyword-based market analysis and sentiment tracking.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `keyword` | `query` | yes | `string` | n/a | Search keywords (e.g., 'deepseek'). |
| `offset` | `query` | no | `integer` | `0` | Pagination offset, starting from 0 and stepping by 20. |
| `sortType` | `query` | no | `string` | `RELEVANCE` | Sorting criteria for search results.

Available Values:
- `RELEVANCE`: Relevance (Default)
- `MOST_LIKED`: Most Liked |
| enum | values | no | n/a | n/a | `RELEVANCE`, `MOST_LIKED` |
| `publishTime` | `query` | no | `string` | `ALL` | Filter posts by publishing time.

Available Values:
- `ALL`: All Time
- `ONE_DAY`: Last 24 Hours
- `ONE_WEEK`: Last 7 Days
- `ONE_MONTH`: Last 30 Days
- `THREE_MONTHS`: Last 90 Days
- `HALF_YEAR`: Last 180 Days |
| enum | values | no | n/a | n/a | `ALL`, `ONE_DAY`, `ONE_WEEK`, `ONE_MONTH`, `THREE_MONTHS`, `HALF_YEAR` |
| `region` | `query` | no | `string` | `US` | ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB'). |

### Request body

No request body.

### Responses

- `200`: OK

## `searchUserV1`

- Method: `GET`
- Path: `/api/tiktok/search-user/v1`
- Summary: User Search
- Description: Get TikTok user Search data, including basic profile information such as user ID, nickname, and unique handle, for discovering influencers in specific niches via keywords and identifying target audiences and conducting competitor research.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `keyword` | `query` | yes | `string` | n/a | Search keywords (e.g., 'deepseek'). |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Start with '0'. |
| `searchId` | `query` | no | `string` | n/a | The 'logid' returned from the previous request for consistent search results. |

### Request body

No request body.

### Responses

- `200`: OK
