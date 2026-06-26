# Kuaishou Video Details operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `get-video-detail`.

## `getVideoDetailsV2`

- Method: `GET`
- Path: `/api/kuaishou/get-video-detail/v2`
- Summary: Video Details
- Description: Get Kuaishou video Details data, including video URL, caption, and author info, for in-depth content performance analysis and building databases of viral videos.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `videoId` | `query` | yes | `string` | n/a | The unique ID of the Kuaishou video, e.g. `3xg9avuebhtfcku` |

### Request body

No request body.

### Responses

- `200`: OK
