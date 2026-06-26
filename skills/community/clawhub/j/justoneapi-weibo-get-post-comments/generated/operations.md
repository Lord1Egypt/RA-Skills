# Weibo Post Comments operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-post-comments`.

## `getWeiboPostCommentsV1`

- Method: `GET`
- Path: `/api/weibo/get-post-comments/v1`
- Summary: Post Comments
- Description: Get Weibo post Comments data, including text, authors, and timestamps, for feedback analysis.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `mid` | `query` | yes | `string` | n/a | Weibo post mid. |
| `sort` | `query` | no | `string` | `TIME` | Sort order for the result set.

Available Values:
- `TIME`: Time
- `HOT`: Hot |
| enum | values | no | n/a | n/a | `TIME`, `HOT` |
| `maxId` | `query` | no | `string` | n/a | Pagination cursor returned by the previous response. |

### Request body

No request body.

### Responses

- `200`: OK
