# Xiaohongshu (RedNote) Keyword Suggestions operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `search-recommend`.

## `searchRecommendV1`

- Method: `GET`
- Path: `/api/xiaohongshu/search-recommend/v1`
- Summary: Keyword Suggestions
- Description: Get Xiaohongshu (RedNote) keyword Suggestions data, including suggested queries, keyword variants, and query metadata, for expanding keyword sets for content research and seo/pseo workflows and improving search coverage by using platform-recommended terms.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |

### Request body

No request body.

### Responses

- `200`: OK
