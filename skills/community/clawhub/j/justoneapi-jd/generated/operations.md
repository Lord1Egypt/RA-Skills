# JD.com operations

Generated from JustOneAPI OpenAPI for platform key `jd`.

## `getItemCommentsV1`

- Method: `GET`
- Path: `/api/jd/get-item-comments/v1`
- Summary: Product Comments
- Description: Get JD.com product Comments data, including ratings, timestamps, and reviewer signals, for customer feedback analysis and product research.
- Tags: `JD.com`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | A unique product identifier on JD.com (item ID). |
| `page` | `query` | no | `string` | n/a | Page number for paginated comments. |

### Request body

No request body.

### Responses

- `200`: OK

## `getJdItemDetailV1`

- Method: `GET`
- Path: `/api/jd/get-item-detail/v1`
- Summary: Product Details
- Description: Get JD.com product Details data, including pricing, images, and shop information, for catalog analysis, product monitoring, and ecommerce research.
- Tags: `JD.com`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | A unique product identifier on JD.com (item ID). |

### Request body

No request body.

### Responses

- `200`: OK

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
