# Xiaohongshu (RedNote) Note Comments operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `get-note-comment`.

## `getNoteCommentV2`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-comment/v2`
- Summary: Note Comments
- Description: Get Xiaohongshu (RedNote) note Comments data, including text, authors, and timestamps, for feedback analysis.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (use the cursor value returned by the last response). |
| `sort` | `query` | no | `string` | `latest` | Sort order for the result set.

Available Values:
- `normal`: Normal
- `latest`: Latest |
| enum | values | no | n/a | n/a | `normal`, `latest` |

### Request body

No request body.

### Responses

- `200`: OK

## `getNoteCommentV4`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-comment/v4`
- Summary: Note Comments
- Description: Get Xiaohongshu (RedNote) note Comments data, including comment text, author profiles, and interaction data, for sentiment analysis and community monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK
