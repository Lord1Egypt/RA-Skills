# Xiaohongshu Creator Marketplace (Pugongying) Note Details operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `get-note-detail`.

## `getXiaohongshuPgyNoteDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/get-note-detail/v1`
- Summary: Note Details
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) note Details data, including media and engagement signals, for content analysis, archiving, and campaign review.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `noteId` | `query` | yes | `string` | n/a | Note ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
