# Instagram operations

Generated from JustOneAPI OpenAPI for platform key `instagram`.

## `getInstagramPostDetailV1`

- Method: `GET`
- Path: `/api/instagram/get-post-detail/v1`
- Summary: Post Details
- Description: Get Instagram post Details data, including post caption, media content (images/videos), and publish time, for analyzing engagement metrics (likes/comments) for a specific post and archiving post content and media assets for content analysis.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `code` | `query` | yes | `string` | n/a | The unique shortcode (slug) for the Instagram post (e.g., 'DRhvwVLAHAG'). |

### Request body

No request body.

### Responses

- `200`: OK

## `getInstagramUserDetailV1`

- Method: `GET`
- Path: `/api/instagram/get-user-detail/v1`
- Summary: User Profile
- Description: Get Instagram user Profile data, including follower count, following count, and post count, for obtaining basic account metadata for influencer vetting, tracking follower growth and audience reach over time, and mapping user handles to specific profile stats.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `username` | `query` | yes | `string` | n/a | The Instagram username whose profile details are to be retrieved. |

### Request body

No request body.

### Responses

- `200`: OK

## `getInstagramUserPostsV1`

- Method: `GET`
- Path: `/api/instagram/get-user-posts/v1`
- Summary: User Published Posts
- Description: Get Instagram user Published Posts data, including post code, caption, and media type, for monitoring recent publishing activity of a specific user and building a historical record of content for auditing or analysis.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `username` | `query` | yes | `string` | n/a | The Instagram username whose published posts are to be retrieved. |
| `paginationToken` | `query` | no | `string` | n/a | Token used for retrieving the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchHashtagPostsV1`

- Method: `GET`
- Path: `/api/instagram/search-hashtag-posts/v1`
- Summary: Hashtag Posts Search
- Description: Get Instagram hashtag Posts Search data, including caption, author profile, and publish time, for competitive analysis of trending topics and hashtags and monitoring community discussions and public opinion on specific tags.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `hashtag` | `query` | yes | `string` | n/a | The hashtag or keyword to search for. |
| `endCursor` | `query` | no | `string` | n/a | Cursor used for retrieving the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchReelsV1`

- Method: `GET`
- Path: `/api/instagram/search-reels/v1`
- Summary: Reels Search
- Description: Get Instagram reels Search data, including post ID, caption, and author profile, for tracking trends and viral content via specific keywords or hashtags and discovering high-engagement reels within a particular niche.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword or hashtag to filter Reels. |
| `paginationToken` | `query` | no | `string` | n/a | Token used for retrieving the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK
