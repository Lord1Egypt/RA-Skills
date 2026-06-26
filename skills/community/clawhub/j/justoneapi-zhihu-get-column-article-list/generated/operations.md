# Zhihu Column Article List operations

Generated from JustOneAPI OpenAPI for platform key `zhihu`.

Endpoint group: `get-column-article-list`.

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
