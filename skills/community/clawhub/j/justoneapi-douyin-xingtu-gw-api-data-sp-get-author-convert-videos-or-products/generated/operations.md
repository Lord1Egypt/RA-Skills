# Douyin Creator Marketplace (Xingtu) Conversion Resources operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/get_author_convert_videos_or_products`.

## `gwApiDataSpGetAuthorConvertVideosOrProductsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1`
- Summary: Conversion Resources
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `platform` | `query` | no | `string` | `SHORT_VIDEO` | Platform type.

Available Values:
- `SHORT_VIDEO`: Short video
- `LIVE_STREAMING`: Live streaming
- `PICTURE_TEXT`: Picture and text
- `SHORT_DRAMA`: Short drama |
| enum | values | no | n/a | n/a | `SHORT_VIDEO`, `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA` |
| `industryId` | `query` | no | `string` | `ALL` | Industry category.

Available Values:
- `ALL`: All
- `ELECTRONICS_AND_APPLIANCES`: Electronics and Appliances
- `FOOD_AND_BEVERAGE`: Food and Beverage
- `CLOTHING_AND_ACCESSORIES`: Clothing and Accessories
- `HEALTHCARE_AND_MEDICAL`: Healthcare and Medical
- `BUSINESS_SERVICES`: Business Services
- `LOCAL_SERVICES`: Local Services
- `REAL_ESTATE`: Real Estate
- `HOME_AND_BUILDING_MATERIALS`: Home and Building Materials
- `EDUCATION_AND_TRAINING`: Education and Training
- `TRAVEL_AND_TOURISM`: Travel and Tourism
- `PUBLIC_SERVICES`: Public Services
- `GAMES`: Games
- `RETAIL`: Retail
- `TRANSPORTATION_EQUIPMENT`: Transportation Equipment
- `AUTOMOTIVE`: Automotive
- `AGRICULTURE_FORESTRY_FISHERY`: Agriculture Forestry Fishery
- `CHEMICAL_AND_ENERGY`: Chemical and Energy
- `ELECTRONICS_AND_ELECTRICAL`: Electronics and Electrical
- `MACHINERY_EQUIPMENT`: Machinery Equipment
- `CULTURE_SPORTS_ENTERTAINMENT`: Culture Sports Entertainment
- `MEDIA_AND_INFORMATION`: Media and Information
- `LOGISTICS`: Logistics
- `TELECOMMUNICATIONS`: Telecommunications
- `FINANCIAL_SERVICES`: Financial Services
- `CATERING_SERVICES`: Catering Services
- `SOFTWARE_TOOLS`: Software Tools
- `FRANCHISING_AND_INVESTMENT`: Franchising and Investment
- `BEAUTY_AND_COSMETICS`: Beauty and Cosmetics
- `MOTHER_BABY_AND_PET`: Mother Baby and Pet
- `DAILY_CHEMICALS`: Daily Chemicals
- `PHYSICAL_BOOKS`: Physical Books
- `SOCIAL_AND_COMMUNICATION`: Social and Communication
- `MEDICAL_INSTITUTIONS`: Medical Institutions |
| enum | values | no | n/a | n/a | `ALL`, `ELECTRONICS_AND_APPLIANCES`, `FOOD_AND_BEVERAGE`, `CLOTHING_AND_ACCESSORIES`, `HEALTHCARE_AND_MEDICAL`, `BUSINESS_SERVICES`, `LOCAL_SERVICES`, `REAL_ESTATE`, `HOME_AND_BUILDING_MATERIALS`, `EDUCATION_AND_TRAINING`, `TRAVEL_AND_TOURISM`, `PUBLIC_SERVICES`, `GAMES`, `RETAIL`, `TRANSPORTATION_EQUIPMENT`, `AUTOMOTIVE`, `AGRICULTURE_FORESTRY_FISHERY`, `CHEMICAL_AND_ENERGY`, `ELECTRONICS_AND_ELECTRICAL`, `MACHINERY_EQUIPMENT`, `CULTURE_SPORTS_ENTERTAINMENT`, `MEDIA_AND_INFORMATION`, `LOGISTICS`, `TELECOMMUNICATIONS`, `FINANCIAL_SERVICES`, `CATERING_SERVICES`, `SOFTWARE_TOOLS`, `FRANCHISING_AND_INVESTMENT`, `BEAUTY_AND_COSMETICS`, `MOTHER_BABY_AND_PET`, `DAILY_CHEMICALS`, `PHYSICAL_BOOKS`, `SOCIAL_AND_COMMUNICATION`, `MEDICAL_INSTITUTIONS` |
| `range` | `query` | no | `string` | `DAY_30` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |
| `detailType` | `query` | no | `string` | `VIDEO` | Resource type.

Available Values:
- `VIDEO`: Video
- `PRODUCT`: Product |
| enum | values | no | n/a | n/a | `VIDEO`, `PRODUCT` |
| `page` | `query` | no | `integer` | `1` | Page number. |

### Request body

No request body.

### Responses

- `200`: OK
