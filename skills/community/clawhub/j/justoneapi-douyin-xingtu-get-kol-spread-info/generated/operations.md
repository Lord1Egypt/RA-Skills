# Douyin Creator Marketplace (Xingtu) Spread Metrics operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-spread-info`.

## `getKolSpreadInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-spread-info/v1`
- Summary: Spread Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) spread metrics data, including audience, content performance, and commercial indicators, for quick evaluation.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `type` | `query` | no | `string` | `_1` | Spread info type.

Available Values:
- `_1`: Personal Video
- `_2`: Xingtu Video |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `range` | `query` | no | `string` | `_2` | Time range.

Available Values:
- `_2`: Last 30 days
- `_3`: Last 90 days |
| enum | values | no | n/a | n/a | `_2`, `_3` |
| `flowType` | `query` | no | `string` | `1` | Flow type. |
| `onlyAssign` | `query` | no | `boolean` | `false` | Only assigned notes. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
