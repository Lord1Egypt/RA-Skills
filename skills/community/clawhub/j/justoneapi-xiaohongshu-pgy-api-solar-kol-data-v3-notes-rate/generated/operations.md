# Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/dataV3/notesRate`.

## `apiSolarKolDataV3NotesRateV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1`
- Summary: Note Performance Metrics
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.
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
| `noteType` | `query` | no | `string` | `PHOTO_TEXT_AND_VIDEO` | Type of note.

Available Values:
- `PHOTO_TEXT_AND_VIDEO`: Photo and Video
- `PHOTO_TEXT`: Photo and Text
- `VIDEO`: Video only |
| enum | values | no | n/a | n/a | `PHOTO_TEXT_AND_VIDEO`, `PHOTO_TEXT`, `VIDEO` |
| `dateType` | `query` | no | `string` | `DAY_30` | Time range for data.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `advertiseSwitch` | `query` | no | `string` | `ALL` | Advertisement filter.

Available Values:
- `ALL`: All notes
- `ORGANIC_ONLY`: Organic notes only |
| enum | values | no | n/a | n/a | `ALL`, `ORGANIC_ONLY` |

### Request body

No request body.

### Responses

- `200`: OK
