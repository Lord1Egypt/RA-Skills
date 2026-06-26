# Xiaohongshu Creator Marketplace (Pugongying) Data Summary operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-data-summary`.

## `getKolDataSummaryV2`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-data-summary/v2`
- Summary: Data Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `business` | `query` | yes | `string` | n/a | Business type.

Available Values:
- `_0`: Normal notes
- `_1`: Cooperation notes |
| enum | values | no | n/a | n/a | `_0`, `_1` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
