# Zhihu Keyword Search operations

Generated from JustOneAPI OpenAPI for platform key `zhihu`.

Endpoint group: `search`.

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
