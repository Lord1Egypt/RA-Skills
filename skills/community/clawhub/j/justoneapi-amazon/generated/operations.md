# Amazon operations

Generated from JustOneAPI OpenAPI for platform key `amazon`.

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

## `getAmazonProductDetailV1`

- Method: `GET`
- Path: `/api/amazon/get-product-detail/v1`
- Summary: Product Details
- Description: Get Amazon product Details data, including title, brand, and price, for building product catalogs and enriching item content (e.g., images), price monitoring and availability tracking, and e-commerce analytics and competitor tracking.
- Tags: `Amazon`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `asin` | `query` | yes | `string` | n/a | ASIN (Amazon Standard Identification Number). |
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

### Request body

No request body.

### Responses

- `200`: OK

## `getProductTopReviewsV1`

- Method: `GET`
- Path: `/api/amazon/get-product-top-reviews/v1`
- Summary: Product Top Reviews
- Description: Get Amazon product Top Reviews data, including most helpful) public reviews, for sentiment analysis and consumer feedback tracking, product research and quality assessment, and monitoring competitor customer experience.
- Tags: `Amazon`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `asin` | `query` | yes | `string` | n/a | ASIN (Amazon Standard Identification Number). |
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

### Request body

No request body.

### Responses

- `200`: OK
