# Douyin (TikTok China) Share Link Resolution operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `share-url-transfer`.

## `shareDouyinUrlTransferV1`

- Method: `GET`
- Path: `/api/douyin/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Douyin (TikTok China) share Link Resolution data, including helping extract canonical IDs, for downstream video and comment workflows.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shareUrl` | `query` | yes | `string` | n/a | The Douyin short share URL. |

### Request body

No request body.

### Responses

- `200`: OK
