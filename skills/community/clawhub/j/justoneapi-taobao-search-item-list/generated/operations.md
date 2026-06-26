# Taobao and Tmall Product Search operations

Generated from JustOneAPI OpenAPI for platform key `taobao`.

Endpoint group: `search-item-list`.

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
