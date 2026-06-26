# Zhihu Column Article Details operations

Generated from JustOneAPI OpenAPI for platform key `zhihu`.

Endpoint group: `get-column-article-detail`.

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
