# Xiaohongshu Creator Marketplace (Pugongying) Data Summary operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/dataV3/dataSummary`.

## `apiSolarKolDataV3DataSummaryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV3/dataSummary/v1`
- Summary: Data Summary
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) Summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `business` | `query` | no | `string` | `DAILY_NOTE` | Business type.

Available Values:
- `DAILY_NOTE`: Daily notes
- `COOPERATE_NOTE`: Cooperative notes |
| enum | values | no | n/a | n/a | `DAILY_NOTE`, `COOPERATE_NOTE` |

### Request body

No request body.

### Responses

- `200`: OK
