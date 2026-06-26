# Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-fans-trend`.

## `getKolFansTrendV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-fans-trend/v1`
- Summary: Follower Growth History
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower growth history data, including historical audience changes over time, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `dateType` | `query` | yes | `string` | n/a | Date type.

Available Values:
- `_1`: Last 30 days
- `_2`: Last 60 days |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `increaseType` | `query` | yes | `string` | n/a | Increase type.

Available Values:
- `_1`: Total fans
- `_2`: New fans increase |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
