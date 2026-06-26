# Xiaohongshu (RedNote) User Search operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `search-user`.

## `getSearchUserV2`

- Method: `GET`
- Path: `/api/xiaohongshu/search-user/v2`
- Summary: User Search
- Description: Get Xiaohongshu (RedNote) user Search data, including profile metadata and public signals, for creator discovery and account research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
