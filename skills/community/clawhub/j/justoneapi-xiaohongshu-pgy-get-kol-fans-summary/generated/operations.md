# Xiaohongshu Creator Marketplace (Pugongying) Follower Summary operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-fans-summary`.

## `getKolFansSummaryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-fans-summary/v1`
- Summary: Follower Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower summary data, including core metrics, trend signals, and performance indicators, for creator evaluation, campaign planning, and creator benchmarking.
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
