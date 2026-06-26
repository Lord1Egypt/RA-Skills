# TikTok Shop Product Details operations

Generated from JustOneAPI OpenAPI for platform key `tiktok-shop`.

Endpoint group: `get-product-detail`.

## `getTiktokShopProductDetailV1`

- Method: `GET`
- Path: `/api/tiktok-shop/get-product-detail/v1`
- Summary: Product Details
- Description: Get TikTok Shop product Details data, including title, description, and price, for building product catalogs, price and stock monitoring, and in-depth product analysis.
- Tags: `TikTok Shop`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `productId` | `query` | yes | `string` | n/a | TikTok Shop Product ID. |
| `region` | `query` | no | `string` | `US` | Target region for product detail.

Available Values:
- `US`: United States
- `GB`: United Kingdom
- `SG`: Singapore
- `MY`: Malaysia
- `PH`: Philippines
- `TH`: Thailand
- `VN`: Vietnam
- `ID`: Indonesia |
| enum | values | no | n/a | n/a | `US`, `GB`, `SG`, `MY`, `PH`, `TH`, `VN`, `ID` |

### Request body

No request body.

### Responses

- `200`: OK
