# Douyin Creator Marketplace (Xingtu) Audience Touchpoint Distribution operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-touch-distribution`.

## `getKolTouchDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-touch-distribution/v1`
- Summary: Audience Touchpoint Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) audience touchpoint distribution data, including segment breakdowns, audience composition, and distribution signals, for traffic analysis and existing integration compatibility.
- Tags: `Douyin Creator Marketplace (Xingtu)`

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
