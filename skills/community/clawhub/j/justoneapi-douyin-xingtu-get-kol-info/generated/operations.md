# Douyin Creator Marketplace (Xingtu) Creator Profile operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-info`.

## `getDouyinXingtuKolInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-info/v1`
- Summary: Creator Profile
- Description: Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `platformChannel` | `query` | no | `string` | `_1` | Platform channel.

Available Values:
- `_1`: Short Video
- `_10`: Live Streaming |
| enum | values | no | n/a | n/a | `_1`, `_10` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
