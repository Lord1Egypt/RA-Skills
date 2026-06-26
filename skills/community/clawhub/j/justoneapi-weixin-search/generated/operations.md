# WeChat Official Accounts Keyword Search operations

Generated from JustOneAPI OpenAPI for platform key `weixin`.

Endpoint group: `search`.

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
