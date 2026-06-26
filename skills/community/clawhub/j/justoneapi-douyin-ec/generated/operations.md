# Douyin E-commerce operations

Generated from JustOneAPI OpenAPI for platform key `douyin-ec`.

## `getDouyinEcItemDetailV1`

- Method: `GET`
- Path: `/api/douyin-ec/get-item-detail/v1`
- Summary: Item Details
- Description: Get Douyin E-commerce item details, including price, title, and stock, for product monitoring and competitive analysis.
- Tags: `Douyin E-commerce`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | The unique ID of the item on Douyin E-commerce. |

### Request body

No request body.

### Responses

- `200`: OK
