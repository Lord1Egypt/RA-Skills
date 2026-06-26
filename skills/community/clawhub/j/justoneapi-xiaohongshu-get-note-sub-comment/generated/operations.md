# Xiaohongshu (RedNote) Comment Replies operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `get-note-sub-comment`.

## `getNoteSubCommentV2`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-sub-comment/v2`
- Summary: Comment Replies
- Description: Get Xiaohongshu (RedNote) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |
| `commentId` | `query` | yes | `string` | n/a | Unique comment identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (use the cursor value returned by the last response). |

### Request body

No request body.

### Responses

- `200`: OK
