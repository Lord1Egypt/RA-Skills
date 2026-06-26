# Taobao and Tmall operations

Generated from JustOneAPI OpenAPI for platform key `taobao`.

## `getItemCommentV3`

- Method: `GET`
- Path: `/api/taobao/get-item-comment/v3`
- Summary: Product Reviews
- Description: Get Taobao and Tmall product Reviews data, including ratings, timestamps, and reviewer signals, for feedback analysis and product research.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |
| `orderType` | `query` | no | `string` | `feedbackdate` | Sort order for the result set.

Available Values:
- `feedbackdate`: Sort by feedback date
- `general`: General sorting |
| enum | values | no | n/a | n/a | `feedbackdate`, `general` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

## `getTaobaoItemDetailV1`

- Method: `GET`
- Path: `/api/taobao/get-item-detail/v1`
- Summary: Product Details
- Description: Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getItemDetailV2`

- Method: `GET`
- Path: `/api/taobao/get-item-detail/v2`
- Summary: Product Details
- Description: Get Taobao and Tmall product Details data through the task-backed v2 flow. If data is not ready within a short wait, the response returns a pending task status.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getItemDetailV4`

- Method: `GET`
- Path: `/api/taobao/get-item-detail/v4`
- Summary: Product Details
- Description: Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getItemDetailV5`

- Method: `GET`
- Path: `/api/taobao/get-item-detail/v5`
- Summary: Product Details
- Description: Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |

### Request body

No request body.

### Responses

- `200`: OK

## `getItemDetailV9`

- Method: `GET`
- Path: `/api/taobao/get-item-detail/v9`
- Summary: Product Details
- Description: Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |

### Request body

No request body.

### Responses

- `200`: OK

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

## `searchItemListV1`

- Method: `GET`
- Path: `/api/taobao/search-item-list/v1`
- Summary: Product Search
- Description: Get Taobao and Tmall product Search data, including titles, prices, and images, for product discovery.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `sort` | `query` | no | `string` | `_sale` | Sort order for the result set.

Available Values:
- `_sale`: Sales
- `_bid`: Price: High to Low
- `bid`: Price: Low to High
- `_coefp`: General |
| enum | values | no | n/a | n/a | `_sale`, `_bid`, `bid`, `_coefp` |
| `tmall` | `query` | no | `boolean` | `false` | Whether to filter results to Tmall only. |
| `startPrice` | `query` | no | `string` | n/a | Minimum price filter (inclusive). |
| `endPrice` | `query` | no | `string` | n/a | Maximum price filter (inclusive). |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
