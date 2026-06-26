# Douyin Creator Marketplace (Xingtu) Marketing Metrics operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-marketing-info`.

## `getKolMarketingInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-marketing-info/v1`
- Summary: Marketing Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) marketing metrics data, including rate card details and commercial service metrics, for creator evaluation, campaign planning, and marketplace research.
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
