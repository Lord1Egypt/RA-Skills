# Xiaohongshu Creator Marketplace (Pugongying) Creator Note List operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-kol-note-list`.

## `getKolNoteListV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-kol-note-list/v1`
- Summary: Creator Note List
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Note List data, including content metadata, publish time, and engagement indicators, for content analysis.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `page` | `query` | no | `integer` | `1` | Page number. |
| `adSwitch` | `query` | yes | `string` | n/a | Ad filter.

Available Values:
- `_1`: Full traffic (All notes)
- `_0`: Natural traffic (Organic notes) |
| enum | values | no | n/a | n/a | `_1`, `_0` |
| `orderType` | `query` | yes | `string` | n/a | Sorting order.

Available Values:
- `_1`: Latest
- `_2`: Most read
- `_3`: Most interactions |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `noteType` | `query` | no | `string` | `_4` | Note type.

Available Values:
- `_1`: Photo and Text notes
- `_2`: Video notes
- `_3`: Cooperation notes
- `_4`: All types |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3`, `_4` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
