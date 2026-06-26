# JD.com Product Details operations

Generated from JustOneAPI OpenAPI for platform key `jd`.

Endpoint group: `get-item-detail`.

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
