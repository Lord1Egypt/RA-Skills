# Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/data/userId/fans_overall_new_history`.

## `apiSolarKolDataUserIdFansOverallNewHistoryV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1`
- Summary: Follower Growth History
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower Growth History data, including historical points, trend signals, and growth metrics, for trend tracking, audience analysis, and creator performance monitoring.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `dateType` | `query` | no | `string` | `DAY_30` | Time range for data.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `increaseType` | `query` | no | `string` | `FANS_TOTAL` | Type of growth data.

Available Values:
- `FANS_TOTAL`: Total fans
- `FANS_INCREASE`: New fans increase |
| enum | values | no | n/a | n/a | `FANS_TOTAL`, `FANS_INCREASE` |

### Request body

No request body.

### Responses

- `200`: OK
