# Douyin Creator Marketplace (Xingtu) Author Commerce Spread Info operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-author-commerce-spread-info`.

## `getAuthorCommerceSpreadInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-commerce-spread-info/v1`
- Summary: Author Commerce Spread Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Spread Info data, including spread metrics, for creator evaluation for campaign planning and media buying.
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
