# Xiaohongshu (RedNote) User Published Notes operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `get-user-note-list`.

## `getUserNoteListV2`

- Method: `GET`
- Path: `/api/xiaohongshu/get-user-note-list/v2`
- Summary: User Published Notes
- Description: Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Unique user identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (the last note's cursor value). |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserNoteListV4`

- Method: `GET`
- Path: `/api/xiaohongshu/get-user-note-list/v4`
- Summary: User Published Notes
- Description: Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Unique user identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (the last note's cursor value). |

### Request body

No request body.

### Responses

- `200`: OK
