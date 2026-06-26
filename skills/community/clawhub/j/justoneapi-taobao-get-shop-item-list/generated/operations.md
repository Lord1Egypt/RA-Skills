# Taobao and Tmall Shop Product List operations

Generated from JustOneAPI OpenAPI for platform key `taobao`.

Endpoint group: `get-shop-item-list`.

## `getTaobaoShopItemListV1`

- Method: `GET`
- Path: `/api/taobao/get-shop-item-list/v1`
- Summary: Shop Product List
- Description: Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Shop identifier. Also known as Seller ID or User ID (they refer to the same value). |
| `sort` | `query` | no | `string` | `_sale` | Sort order for the result set.

Available Values:
- `_sale`: Sales
- `_default`: Default |
| enum | values | no | n/a | n/a | `_sale`, `_default` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

## `getShopItemListV2`

- Method: `GET`
- Path: `/api/taobao/get-shop-item-list/v2`
- Summary: Shop Product List
- Description: Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Shop identifier. Also known as Seller ID or User ID (they refer to the same value). |
| `shopId` | `query` | yes | `string` | n/a | Unique shop identifier on Taobao/Tmall (shop ID). |
| `sort` | `query` | no | `string` | `coefp` | Sort order for the result set.

Available Values:
- `coefp`: Comprehensive sorting
- `hotsell`: Hot selling / Sales volume
- `oldstarts`: New arrivals / Old starts
- `bid`: Price: Low to High
- `_bid`: Price: High to Low |
| enum | values | no | n/a | n/a | `coefp`, `hotsell`, `oldstarts`, `bid`, `_bid` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

## `getShopItemListV3`

- Method: `GET`
- Path: `/api/taobao/get-shop-item-list/v3`
- Summary: Shop Product List
- Description: Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Shop identifier. Also known as Seller ID or User ID (they refer to the same value). |
| `shopId` | `query` | yes | `string` | n/a | Unique shop identifier on Taobao/Tmall (shop ID). |
| `sort` | `query` | no | `string` | `coefp` | Sort order for the result set.

Available Values:
- `coefp`: Comprehensive sorting
- `hotsell`: Hot selling / Sales volume
- `oldstarts`: New arrivals / Old starts
- `bid`: Price: Low to High
- `_bid`: Price: High to Low |
| enum | values | no | n/a | n/a | `coefp`, `hotsell`, `oldstarts`, `bid`, `_bid` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
