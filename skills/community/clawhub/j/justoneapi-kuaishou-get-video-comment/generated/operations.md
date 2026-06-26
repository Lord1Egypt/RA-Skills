# Kuaishou Video Comments operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `get-video-comment`.

## `getVideoCommentsV1`

- Method: `GET`
- Path: `/api/kuaishou/get-video-comment/v1`
- Summary: Video Comments
- Description: Retrieves public comments of a Kuaishou video, including comment content,
author info, like count, and reply count.

Typical use cases:
- Sentiment analysis and community feedback monitoring
- Gathering engagement data for specific videos
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `videoId` | `query` | yes | `string` | n/a | The unique ID of the Kuaishou video, e.g. `3xbknvct79h46h9` or refer_photo_id `177012131237` |
| `pcursor` | `query` | no | `string` | n/a | Pagination cursor for subsequent pages. |

### Request body

No request body.

### Responses

- `200`: OK
