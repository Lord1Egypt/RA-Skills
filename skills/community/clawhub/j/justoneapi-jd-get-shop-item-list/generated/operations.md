# JD.com Shop Product List operations

Generated from JustOneAPI OpenAPI for platform key `jd`.

Endpoint group: `get-shop-item-list`.

## `getJdShopItemListV1`

- Method: `GET`
- Path: `/api/jd/get-shop-item-list/v1`
- Summary: Shop Product List
- Description: Get JD.com shop Product List data, including item titles, prices, and images, for catalog tracking and seller research.
- Tags: `JD.com`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shopId` | `query` | yes | `string` | n/a | A unique shop identifier on JD.com (Shop ID). |
| `page` | `query` | no | `string` | n/a | Page number for paginated comments. |

### Request body

No request body.

### Responses

- `200`: OK
