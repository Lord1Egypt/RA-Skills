# Xiaohongshu Creator Marketplace (Pugongying) Creator Profile operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-info`.

## `getXiaohongshuPgyKolInfoV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-info/v1`
- Summary: Creator Profile
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
