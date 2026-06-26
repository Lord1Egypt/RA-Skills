# Douyin Creator Marketplace (Xingtu) Video Details operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-video-detail`.

## `getDouyinXingtuVideoDetailV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-video-detail/v1`
- Summary: Video Details
- Description: Get Douyin Creator Marketplace (Xingtu) video Details data, including performance fields from the legacy Douyin Xingtu endpoint, for content review and integration compatibility.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `detailId` | `query` | yes | `string` | n/a | Video detail ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
