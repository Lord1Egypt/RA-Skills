# Toutiao Article Details operations

Generated from JustOneAPI OpenAPI for platform key `toutiao`.

Endpoint group: `get-article-detail`.

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
