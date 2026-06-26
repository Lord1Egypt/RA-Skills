# Kuaishou Share Link Resolution operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `share-url-transfer`.

## `shareLinkResolutionV1`

- Method: `GET`
- Path: `/api/kuaishou/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Kuaishou share Link Resolution data, including resolved content identifier and target object data, for resolving shared links for automated content processing.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shareUrl` | `query` | yes | `string` | n/a | Kuaishou share URL (must start with 'https://v.kuaishou.com/'). |

### Request body

No request body.

### Responses

- `200`: OK
