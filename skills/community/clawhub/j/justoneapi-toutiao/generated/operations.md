# Toutiao operations

Generated from JustOneAPI OpenAPI for platform key `toutiao`.

## `getToutiaoArticleDetailV1`

- Method: `GET`
- Path: `/api/toutiao/get-article-detail/v1`
- Summary: Article Details
- Description: Get Toutiao article Details data, including article ID, title, and author information, for content performance analysis and media monitoring and verifying article authenticity and metadata retrieval.
- Tags: `Toutiao`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required to access the API. |
| `id` | `query` | yes | `string` | n/a | The unique identifier of the Toutiao article. |

### Request body

No request body.

### Responses

- `200`: OK

## `getToutiaoUserDetailV1`

- Method: `GET`
- Path: `/api/toutiao/get-user-detail/v1`
- Summary: User Profile
- Description: Get Toutiao user Profile data, including user ID, nickname, and avatar, for influencer profiling and audience analysis and monitoring creator performance and growth.
- Tags: `Toutiao`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required to access the API. |
| `userId` | `query` | yes | `string` | n/a | The unique identifier of the Toutiao user. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchToutiaoV1`

- Method: `GET`
- Path: `/api/toutiao/search/v1`
- Summary: App Keyword Search
- Description: Get Toutiao app Keyword Search data, including matching articles, videos, and authors, for topic discovery and monitoring.
- Tags: `Toutiao`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required to access the API. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword or query. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |
| `searchId` | `query` | no | `string` | n/a | Search session ID for consistent pagination (not required for the first page). |

### Request body

No request body.

### Responses

- `200`: OK

## `searchV2`

- Method: `GET`
- Path: `/api/toutiao/search/v2`
- Summary: Web Keyword Search
- Description: Get Toutiao web Keyword Search data, including this is the PC version of the search API. Note that it currently only supports retrieving the first page of results, for first-page discovery of articles, videos, and authors for trend research and monitoring.
- Tags: `Toutiao`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required to access the API. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword or query. |

### Request body

No request body.

### Responses

- `200`: OK
