# Zhihu Answer List operations

Generated from JustOneAPI OpenAPI for platform key `zhihu`.

Endpoint group: `get-answer-list`.

## `getAnswerListV1`

- Method: `GET`
- Path: `/api/zhihu/get-answer-list/v1`
- Summary: Answer List
- Description: Get Zhihu answer List data, including answer content, author profiles, and interaction metrics, for question analysis and answer research.
- Tags: `Zhihu`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `questionId` | `query` | yes | `string` | n/a | Question ID |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor from previous result. |
| `offset` | `query` | no | `integer` | `0` | Start offset, begins with 0. |
| `order` | `query` | no | `string` | `_updated` | Sorting criteria for answers.

Available Values:
- `_default`: Default sorting.
- `_updated`: Sorted by updated time. |
| enum | values | no | n/a | n/a | `_default`, `_updated` |
| `sessionId` | `query` | no | `string` | n/a | Session ID from previous result. |

### Request body

No request body.

### Responses

- `200`: OK
