# Bilibili User Published Videos operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-user-video-list`.

## `getBilibiliUserVideoListV2`

- Method: `GET`
- Path: `/api/bilibili/get-user-video-list/v2`
- Summary: User Published Videos
- Description: Get Bilibili user Published Videos data, including titles, covers, and publish times, for creator monitoring and content performance analysis.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `uid` | `query` | yes | `string` | n/a | Bilibili User ID (UID). |
| `param` | `query` | no | `string` | n/a | Pagination parameter from previous response. |

### Request body

No request body.

### Responses

- `200`: OK
