# Weibo Post Details operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-weibo-detail`.

## `getWeiboDetailsV1`

- Method: `GET`
- Path: `/api/weibo/get-weibo-detail/v1`
- Summary: Post Details
- Description: Get Weibo post Details data, including media, author metadata, and engagement counts, for post analysis, archiving, and campaign monitoring.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `id` | `query` | yes | `string` | n/a | Weibo post ID. |

### Request body

No request body.

### Responses

- `200`: OK
