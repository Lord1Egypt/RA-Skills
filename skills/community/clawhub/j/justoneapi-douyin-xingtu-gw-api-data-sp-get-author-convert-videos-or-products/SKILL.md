---
name: Douyin Creator Marketplace (Xingtu) Conversion Resources API
description: Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with oAuthorId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products"}}
---

# Douyin Creator Marketplace (Xingtu) Conversion Resources

Use this focused JustOneAPI skill for conversion Resources in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1`. Required non-token inputs are `oAuthorId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/data_sp/get_author_convert_videos_or_products`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-data-sp-get-author-convert-videos-or-products`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiDataSpGetAuthorConvertVideosOrProductsV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1` | Conversion Resources |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `detailType` | `query` | n/a | all | `string` | Resource type. Available Values: - `VIDEO`: Video - `PRODUCT`: Product |
| `detailType` enum | values | n/a | n/a | n/a | `PRODUCT`, `VIDEO` |
| `industryId` | `query` | n/a | all | `string` | Industry category. Available Values: - `ALL`: All - `ELECTRONICS_AND_APPLIANCES`: Electronics and Appliances - `FOOD_AND_BEVERAGE`: Food and Beverage - `CLOTHING_AND_ACCESSORIES`: Clothing and Accessories - `HEALTHCARE_AND_MEDICAL`: Healthcare and Medical - `BUSINESS_SERVICES`: Business Services - `LOCAL_SERVICES`: Local Services - `REAL_ESTATE`: Real Estate - `HOME_AND_BUILDING_MATERIALS`: Home and Building Materials - `EDUCATION_AND_TRAINING`: Education and Training - `TRAVEL_AND_TOURISM`: Travel and Tourism - `PUBLIC_SERVICES`: Public Services - `GAMES`: Games - `RETAIL`: Retail - `TRANSPORTATION_EQUIPMENT`: Transportation Equipment - `AUTOMOTIVE`: Automotive - `AGRICULTURE_FORESTRY_FISHERY`: Agriculture Forestry Fishery - `CHEMICAL_AND_ENERGY`: Chemical and Energy - `ELECTRONICS_AND_ELECTRICAL`: Electronics and Electrical - `MACHINERY_EQUIPMENT`: Machinery Equipment - `CULTURE_SPORTS_ENTERTAINMENT`: Culture Sports Entertainment - `MEDIA_AND_INFORMATION`: Media and Information - `LOGISTICS`: Logistics - `TELECOMMUNICATIONS`: Telecommunications - `FINANCIAL_SERVICES`: Financial Services - `CATERING_SERVICES`: Catering Services - `SOFTWARE_TOOLS`: Software Tools - `FRANCHISING_AND_INVESTMENT`: Franchising and Investment - `BEAUTY_AND_COSMETICS`: Beauty and Cosmetics - `MOTHER_BABY_AND_PET`: Mother Baby and Pet - `DAILY_CHEMICALS`: Daily Chemicals - `PHYSICAL_BOOKS`: Physical Books - `SOCIAL_AND_COMMUNICATION`: Social and Communication - `MEDICAL_INSTITUTIONS`: Medical Institutions |
| `industryId` enum | values | n/a | n/a | n/a | `AGRICULTURE_FORESTRY_FISHERY`, `ALL`, `AUTOMOTIVE`, `BEAUTY_AND_COSMETICS`, `BUSINESS_SERVICES`, `CATERING_SERVICES`, `CHEMICAL_AND_ENERGY`, `CLOTHING_AND_ACCESSORIES`, `CULTURE_SPORTS_ENTERTAINMENT`, `DAILY_CHEMICALS`, `EDUCATION_AND_TRAINING`, `ELECTRONICS_AND_APPLIANCES`, `ELECTRONICS_AND_ELECTRICAL`, `FINANCIAL_SERVICES`, `FOOD_AND_BEVERAGE`, `FRANCHISING_AND_INVESTMENT`, `GAMES`, `HEALTHCARE_AND_MEDICAL`, `HOME_AND_BUILDING_MATERIALS`, `LOCAL_SERVICES`, `LOGISTICS`, `MACHINERY_EQUIPMENT`, `MEDIA_AND_INFORMATION`, `MEDICAL_INSTITUTIONS`, `MOTHER_BABY_AND_PET`, `PHYSICAL_BOOKS`, `PUBLIC_SERVICES`, `REAL_ESTATE`, `RETAIL`, `SOCIAL_AND_COMMUNICATION`, `SOFTWARE_TOOLS`, `TELECOMMUNICATIONS`, `TRANSPORTATION_EQUIPMENT`, `TRAVEL_AND_TOURISM` |
| `oAuthorId` | `query` | all | n/a | `string` | Author's unique ID |
| `page` | `query` | n/a | all | `integer` | Page number |
| `platform` | `query` | n/a | all | `string` | Platform type. Available Values: - `SHORT_VIDEO`: Short video - `LIVE_STREAMING`: Live streaming - `PICTURE_TEXT`: Picture and text - `SHORT_DRAMA`: Short drama |
| `platform` enum | values | n/a | n/a | n/a | `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA`, `SHORT_VIDEO` |
| `range` | `query` | n/a | all | `string` | Time range. Available Values: - `DAY_30`: Last 30 days - `DAY_90`: Last 90 days |
| `range` enum | values | n/a | n/a | n/a | `DAY_30`, `DAY_90` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiDataSpGetAuthorConvertVideosOrProductsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiDataSpGetAuthorConvertVideosOrProductsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiDataSpGetAuthorConvertVideosOrProductsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oAuthorId":"<oAuthorId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_convert_videos_or_products&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiDataSpGetAuthorConvertVideosOrProductsV1` on `/api/douyin-xingtu/gw/api/data_sp/get_author_convert_videos_or_products/v1`.
- Echo the required lookup scope (`oAuthorId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
