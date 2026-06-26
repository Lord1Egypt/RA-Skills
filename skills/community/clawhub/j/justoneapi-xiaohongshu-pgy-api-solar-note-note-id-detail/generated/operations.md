# Xiaohongshu Creator Marketplace (Pugongying) Note Details operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/note/noteId/detail`.

## `apiSolarNoteNoteIdDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/note/noteId/detail/v1`
- Summary: Note Details
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note Details data, including media and engagement signals, for content analysis, archiving, and campaign review.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `noteId` | `query` | yes | `string` | n/a | Note's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK
