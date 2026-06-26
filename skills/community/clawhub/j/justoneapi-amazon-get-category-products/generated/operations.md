# Amazon Products By Category operations

Generated from JustOneAPI OpenAPI for platform key `amazon`.

Endpoint group: `get-category-products`.

## `getProductsByCategoryV1`

- Method: `GET`
- Path: `/api/amazon/get-category-products/v1`
- Summary: Products By Category
- Description: Get Amazon products By Category data, including title, price, and rating, for category-based product discovery and returns product information such as title, price, and rating.
- Tags: `Amazon`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `categoryId` | `query` | yes | `string` | n/a | For example: https://amazon.com/s?node=172282 - the Amazon Category ID is 172282 |
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
| `sortBy` | `query` | no | `string` | `RELEVANCE` | Sort by.

Available Values:
- `RELEVANCE`: Relevance
- `LOWEST_PRICE`: Lowest Price
- `HIGHEST_PRICE`: Highest Price
- `REVIEWS`: Reviews
- `NEWEST`: Newest
- `BEST_SELLERS`: Best Sellers |
| enum | values | no | n/a | n/a | `RELEVANCE`, `LOWEST_PRICE`, `HIGHEST_PRICE`, `REVIEWS`, `NEWEST`, `BEST_SELLERS` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
