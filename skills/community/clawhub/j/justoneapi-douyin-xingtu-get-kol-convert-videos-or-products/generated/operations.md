# Douyin Creator Marketplace (Xingtu) Conversion Resources operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-convert-videos-or-products`.

## `getKolConvertVideosOrProductsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-convert-videos-or-products/v1`
- Summary: Conversion Resources
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `detailType` | `query` | yes | `string` | n/a | Resource type.

Available Values:
- `_1`: Video Data
- `_2`: Product Data |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `page` | `query` | yes | `integer` | n/a | Page number. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
