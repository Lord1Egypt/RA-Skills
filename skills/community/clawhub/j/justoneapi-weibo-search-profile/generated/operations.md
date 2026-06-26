# Weibo Search User Published Posts operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `search-profile`.

## `searchProfileV1`

- Method: `GET`
- Path: `/api/weibo/search-profile/v1`
- Summary: Search User Published Posts
- Description: Get Weibo search User Published Posts data, including matched results, metadata, and ranking signals, for author research and historical content discovery.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `q` | `query` | yes | `string` | n/a | Search Keywords. |
| `startDay` | `query` | no | `string` | n/a | Start Day (yyyy-MM-dd). |
| `endDay` | `query` | no | `string` | n/a | End Day (yyyy-MM-dd). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK
