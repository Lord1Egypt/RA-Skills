# Bilibili Share Link Resolution operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `share-url-transfer`.

## `shareBilibiliUrlTransferV1`

- Method: `GET`
- Path: `/api/bilibili/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Bilibili share Link Resolution data, including resolved video and page identifier, for converting shortened mobile share links to standard bvid/metadata and automating content extraction from shared social media links.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `shareUrl` | `query` | yes | `string` | n/a | Bilibili share URL (must start with https://b23.tv/). |

### Request body

No request body.

### Responses

- `200`: OK
