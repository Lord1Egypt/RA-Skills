# Douyin Creator Marketplace (Xingtu) Conversion Analysis operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-convert-ability`.

## `getKolConvertAbilityV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-convert-ability/v1`
- Summary: Conversion Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Analysis data, including conversion efficiency and commercial performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `range` | `query` | yes | `string` | n/a | Time range.

Available Values:
- `_1`: Last 7 days
- `_2`: Last 30 days
- `_3`: Last 90 days |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
