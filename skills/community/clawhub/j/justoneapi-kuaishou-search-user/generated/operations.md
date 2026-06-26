# Kuaishou User Search operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `search-user`.

## `searchKuaishouUserV2`

- Method: `GET`
- Path: `/api/kuaishou/search-user/v2`
- Summary: User Search
- Description: Get Kuaishou user Search data, including profile names, avatars, and follower counts, for creator discovery and account research.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword to find users. |
| `page` | `query` | no | `integer` | `1` | Page number for results, starting from 1. |

### Request body

No request body.

### Responses

- `200`: OK
