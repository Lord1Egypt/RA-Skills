# Xiaohongshu Creator Marketplace (Pugongying) User Published Notes operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/dataV2/notesDetail`.

## `apiSolarKolDataV2NotesDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV2/notesDetail/v1`
- Summary: User Published Notes
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) user Published Notes data, including note metadata and engagement signals, for creator monitoring and campaign research.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `advertiseSwitch` | `query` | no | `string` | `ALL` | Advertisement filter.

Available Values:
- `ALL`: All notes
- `ORGANIC_ONLY`: Organic notes only |
| enum | values | no | n/a | n/a | `ALL`, `ORGANIC_ONLY` |
| `orderType` | `query` | no | `string` | `LATEST` | Sorting order.

Available Values:
- `LATEST`: Latest
- `MOST_READ`: Most read
- `MOST_INTERACT`: Most interactions |
| enum | values | no | n/a | n/a | `LATEST`, `MOST_READ`, `MOST_INTERACT` |
| `noteType` | `query` | no | `string` | `ALL` | Type of note.

Available Values:
- `ALL`: All types
- `COOPERATION`: Cooperation notes
- `PHOTO_TEXT`: Photo and Text
- `VIDEO`: Video only |
| enum | values | no | n/a | n/a | `ALL`, `COOPERATION`, `PHOTO_TEXT`, `VIDEO` |
| `isThirdPlatform` | `query` | no | `string` | `NO` | Whether from third-party platform.

Available Values:
- `NO`: No
- `YES`: Yes |
| enum | values | no | n/a | n/a | `NO`, `YES` |
| `pageNumber` | `query` | no | `integer` | `1` | Page number. |

### Request body

No request body.

### Responses

- `200`: OK
