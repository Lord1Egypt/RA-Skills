# Xiaohongshu Creator Marketplace (Pugongying) Follower Summary operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/dataV3/fansSummary`.

## `apiSolarKolDataV3FansSummaryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV3/fansSummary/v1`
- Summary: Follower Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower Summary data, including growth and engagement metrics, for audience analysis and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK
