# Amazon Product Top Reviews operations

Generated from JustOneAPI OpenAPI for platform key `amazon`.

Endpoint group: `get-product-top-reviews`.

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
