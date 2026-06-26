# Xiaohongshu Creator Marketplace (Pugongying) Creator Core Metrics operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-core-data`.

## `getKolDataCoreV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-core-data/v1`
- Summary: Creator Core Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Core Metrics data, including engagement and content metrics, for benchmarking, vetting, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `business` | `query` | no | `string` | `_0` | Business type.

Available Values:
- `_0`: Normal notes
- `_1`: Cooperation notes |
| enum | values | no | n/a | n/a | `_0`, `_1` |
| `noteType` | `query` | no | `string` | `_3` | Note type.

Available Values:
- `_1`: Photo and Text
- `_2`: Video
- `_3`: Photo and Video |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `dateType` | `query` | no | `string` | `_1` | Date type.

Available Values:
- `_1`: Last 30 days
- `_2`: Last 90 days |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `adSwitch` | `query` | no | `string` | `_1` | Ad filter.

Available Values:
- `_1`: Full traffic (All notes)
- `_0`: Natural traffic (Organic notes) |
| enum | values | no | n/a | n/a | `_1`, `_0` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
