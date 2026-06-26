# Xiaohongshu Creator Marketplace (Pugongying) Cost Effectiveness Analysis operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-cost-effective`.

## `getKolCostEffectiveV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-cost-effective/v1`
- Summary: Cost Effectiveness Analysis
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) cost Effectiveness Analysis data, including pricing, reach, and engagement efficiency indicators, for campaign evaluation.
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
