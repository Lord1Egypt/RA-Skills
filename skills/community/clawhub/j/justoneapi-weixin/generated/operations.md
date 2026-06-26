# WeChat Official Accounts operations

Generated from JustOneAPI OpenAPI for platform key `weixin`.

## `getArticleComment`

- Method: `GET`
- Path: `/api/weixin/get-article-comment/v1`
- Summary: Article Comments
- Description: Get WeChat Official Accounts article Comments data, including commenter details, comment text, and timestamps, for feedback analysis.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `articleUrl` | `query` | yes | `string` | n/a | The URL of the Weixin article. |

### Request body

No request body.

### Responses

- `200`: OK

## `getWeixinArticleDetailV1`

- Method: `GET`
- Path: `/api/weixin/get-article-detail/v1`
- Summary: Article Details
- Description: Get WeChat Official Accounts article Details data, including body content, for article archiving, research, and content analysis.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `articleUrl` | `query` | yes | `string` | n/a | The URL of the Weixin article. |

### Request body

No request body.

### Responses

- `200`: OK

## `getArticleFeedback`

- Method: `GET`
- Path: `/api/weixin/get-article-feedback/v1`
- Summary: Article Engagement Metrics
- Description: Get WeChat Official Accounts article Engagement Metrics data, including like, share, and comment metrics, for article performance tracking and benchmarking.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `articleUrl` | `query` | yes | `string` | n/a | The URL of the Weixin article. |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserPost`

- Method: `GET`
- Path: `/api/weixin/get-user-post/v1`
- Summary: User Published Posts
- Description: Get WeChat Official Accounts user Published Posts data, including titles, publish times, and summaries, for account monitoring.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `wxid` | `query` | yes | `string` | n/a | The ID of the Weixin Official Account (e.g., 'rmrbwx'). |

### Request body

No request body.

### Responses

- `200`: OK

## `searchWeixinV1`

- Method: `GET`
- Path: `/api/weixin/search/v1`
- Summary: Keyword Search
- Description: Get WeChat Official Accounts keyword Search data, including account names, titles, and publish times, for content discovery.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword. |
| `offset` | `query` | no | `integer` | `0` | Pagination offset (starts with 0, increment by 20). |
| `searchType` | `query` | no | `string` | `_0` | Type of search results (accounts, articles, etc.).

Available Values:
- `_0`: All
- `_1`: WeChat Official Account
- `_2`: Article
- `_7`: WeChat Channel
- `_262208`: Wechat Mini Program
- `_384`: Emoji
- `_16777728`: Encyclopedia
- `_9`: Live
- `_1024`: Book
- `_512`: Music
- `_16384`: News
- `_8192`: Wechat Index
- `_8`: Moments |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2`, `_7`, `_262208`, `_384`, `_16777728`, `_9`, `_1024`, `_512`, `_16384`, `_8192`, `_8` |
| `sortType` | `query` | no | `string` | `_0` | Sorting criteria for search results.

Available Values:
- `_0`: Default
- `_2`: Latest
- `_4`: Hot |
| enum | values | no | n/a | n/a | `_0`, `_2`, `_4` |

### Request body

No request body.

### Responses

- `200`: OK
