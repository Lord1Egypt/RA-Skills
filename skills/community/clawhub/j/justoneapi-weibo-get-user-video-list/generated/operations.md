# Weibo User Video List operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-user-video-list`.

## `getWeiboUserVideoListV1`

- Method: `GET`
- Path: `/api/weibo/get-user-video-list/v1`
- Summary: User Video List
- Description: Get Weibo user Video list data (waterfall), including pagination cursor for next page.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor returned by the previous response. |

### Request body

No request body.

### Responses

- `200`: OK
