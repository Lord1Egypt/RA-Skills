# Weibo User Published Posts operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-user-post`.

## `getUserPublishedPostsV1`

- Method: `GET`
- Path: `/api/weibo/get-user-post/v1`
- Summary: User Published Posts
- Description: Get Weibo user Published Posts data, including text, media, and publish times, for account monitoring.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |
| `sinceId` | `query` | no | `string` | n/a | Pagination cursor (since_id). Required if page > 1. |

### Request body

No request body.

### Responses

- `200`: OK
