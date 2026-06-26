# Kuaishou Video Search operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `search-video`.

## `searchKuaishouVideoV2`

- Method: `GET`
- Path: `/api/kuaishou/search-video/v2`
- Summary: Video Search
- Description: Get Kuaishou video Search data, including video ID, cover image, and description, for competitive analysis and market trends and keywords monitoring and brand tracking.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword to find videos. |
| `page` | `query` | no | `integer` | `1` | Page number for results, starting from 1. |

### Request body

No request body.

### Responses

- `200`: OK
