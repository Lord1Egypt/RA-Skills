# Amazon Best Sellers operations

Generated from JustOneAPI OpenAPI for platform key `amazon`.

Endpoint group: `get-best-sellers`.

## `getBestSellersV1`

- Method: `GET`
- Path: `/api/amazon/get-best-sellers/v1`
- Summary: Best Sellers
- Description: Get Amazon best Sellers data, including rank positions, product metadata, and pricing, for identifying trending products in specific categories, market share analysis and category research, and tracking sales rank and popularity over time.
- Tags: `Amazon`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `category` | `query` | yes | `string` | n/a | Best sellers category to return products for (e.g. 'baby-products' or 'baby-products/166777011'). The value is derived from the URL path of the Amazon Best Sellers page, such as: https://www.amazon.com/Best-Sellers-Baby-Baby-Toddler-Feeding-Supplies/zgbs/baby-products/166777011 |
| `country` | `query` | no | `string` | `US` | Country code for the Amazon product.

Available Values:
- `US`: United States
- `AU`: Australia
- `BR`: Brazil
- `CA`: Canada
- `CN`: China
- `FR`: France
- `DE`: Germany
- `IN`: India
- `IT`: Italy
- `MX`: Mexico
- `NL`: Netherlands
- `SG`: Singapore
- `ES`: Spain
- `TR`: Turkey
- `AE`: United Arab Emirates
- `GB`: United Kingdom
- `JP`: Japan
- `SA`: Saudi Arabia
- `PL`: Poland
- `SE`: Sweden
- `BE`: Belgium
- `EG`: Egypt
- `ZA`: South Africa
- `IE`: Ireland |
| enum | values | no | n/a | n/a | `US`, `AU`, `BR`, `CA`, `CN`, `FR`, `DE`, `IN`, `IT`, `MX`, `NL`, `SG`, `ES`, `TR`, `AE`, `GB`, `JP`, `SA`, `PL`, `SE`, `BE`, `EG`, `ZA`, `IE` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
