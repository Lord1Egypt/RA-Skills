# Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-note-rate`.

## `getKolNoteRateV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-note-rate/v1`
- Summary: Note Performance Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `dateType` | `query` | no | `string` | `_1` | Date type.

Available Values:
- `_1`: Last 30 days
- `_2`: Last 90 days |
| enum | values | no | n/a | n/a | `_1`, `_2` |
| `noteType` | `query` | no | `string` | `_3` | Note type.

Available Values:
- `_1`: Photo and Text
- `_2`: Video
- `_3`: Photo and Video |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `adSwitch` | `query` | no | `string` | `_1` | Ad filter.

Available Values:
- `_1`: Full traffic (All notes)
- `_0`: Natural traffic (Organic notes) |
| enum | values | no | n/a | n/a | `_1`, `_0` |
| `business` | `query` | no | `string` | `_0` | Business type.

Available Values:
- `_0`: Normal notes
- `_1`: Cooperation notes |
| enum | values | no | n/a | n/a | `_0`, `_1` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
