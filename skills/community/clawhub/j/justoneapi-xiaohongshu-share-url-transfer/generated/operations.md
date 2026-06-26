# Xiaohongshu (RedNote) Share Link Resolution operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `share-url-transfer`.

## `shareXiaohongshuUrlTransferV1`

- Method: `GET`
- Path: `/api/xiaohongshu/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Xiaohongshu (RedNote) share Link Resolution data, including helping extract note IDs, for downstream note and comment workflows.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shareUrl` | `query` | yes | `string` | n/a | RedNote share link URL to be resolved (short link or shared URL). |

### Request body

No request body.

### Responses

- `200`: OK
