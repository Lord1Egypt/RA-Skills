# Zhihu operations

Generated from JustOneAPI OpenAPI for platform key `zhihu`.

## `getAnswerListV1`

- Method: `GET`
- Path: `/api/zhihu/get-answer-list/v1`
- Summary: Answer List
- Description: Get Zhihu answer List data, including answer content, author profiles, and interaction metrics, for question analysis and answer research.
- Tags: `Zhihu`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `questionId` | `query` | yes | `string` | n/a | Question ID |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor from previous result. |
| `offset` | `query` | no | `integer` | `0` | Start offset, begins with 0. |
| `order` | `query` | no | `string` | `_updated` | Sorting criteria for answers.

Available Values:
- `_default`: Default sorting.
- `_updated`: Sorted by updated time. |
| enum | values | no | n/a | n/a | `_default`, `_updated` |
| `sessionId` | `query` | no | `string` | n/a | Session ID from previous result. |

### Request body

No request body.

### Responses

- `200`: OK

## `getColumnArticleDetailV1`

- Method: `GET`
- Path: `/api/zhihu/get-column-article-detail/v1`
- Summary: Column Article Details
- Description: Get Zhihu column Article Details data, including title, author, and content, for article archiving and content research.
- Tags: `Zhihu`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `id` | `query` | yes | `string` | n/a | Article ID |

### Request body

No request body.

### Responses

- `200`: OK

## `getColumnArticleListV1`

- Method: `GET`
- Path: `/api/zhihu/get-column-article-list/v1`
- Summary: Column Article List
- Description: Get Zhihu column Article List data, including article metadata and list ordering, for column monitoring and content collection.
- Tags: `Zhihu`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `columnId` | `query` | yes | `string` | n/a | Column ID |
| `offset` | `query` | no | `integer` | `0` | Start offset, begins with 0. |

### Request body

No request body.

### Responses

- `200`: OK

## `searchZhihuV1`

- Method: `GET`
- Path: `/api/zhihu/search/v1`
- Summary: Keyword Search
- Description: Get Zhihu keyword Search data, including matched results, metadata, and ranking signals, for topic discovery and content research.
- Tags: `Zhihu`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `keyword` | `query` | yes | `string` | n/a | Search keywords. |
| `offset` | `query` | no | `integer` | `0` | Start offset, begins with 0. |

### Request body

No request body.

### Responses

- `200`: OK
