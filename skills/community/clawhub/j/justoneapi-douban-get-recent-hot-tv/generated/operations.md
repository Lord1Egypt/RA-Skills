# Douban Movie Recent Hot Tv operations

Generated from JustOneAPI OpenAPI for platform key `douban`.

Endpoint group: `get-recent-hot-tv`.

## `getRecentHotTvV1`

- Method: `GET`
- Path: `/api/douban/get-recent-hot-tv/v1`
- Summary: Recent Hot Tv
- Description: Get Douban recent Hot Tv data, including ratings, posters, and subject metadata, for series discovery and trend monitoring.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
