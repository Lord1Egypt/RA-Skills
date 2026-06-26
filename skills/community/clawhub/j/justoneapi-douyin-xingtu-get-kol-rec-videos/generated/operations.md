# Douyin Creator Marketplace (Xingtu) Recommended Videos operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-rec-videos`.

## `getKolRecVideosV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-rec-videos/v1`
- Summary: Recommended Videos
- Description: Get Douyin Creator Marketplace (Xingtu) recommended videos data, including video performance metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
