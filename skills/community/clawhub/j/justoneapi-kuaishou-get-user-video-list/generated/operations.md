# Kuaishou User Published Videos operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `get-user-video-list`.

## `getKuaishouUserVideoListV2`

- Method: `GET`
- Path: `/api/kuaishou/get-user-video-list/v2`
- Summary: User Published Videos
- Description: Get Kuaishou user Published Videos data, including covers, publish times, and engagement metrics, for creator monitoring and content performance analysis.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | The unique user ID on Kuaishou. |
| `pcursor` | `query` | no | `string` | n/a | Pagination cursor for subsequent pages. |

### Request body

No request body.

### Responses

- `200`: OK
