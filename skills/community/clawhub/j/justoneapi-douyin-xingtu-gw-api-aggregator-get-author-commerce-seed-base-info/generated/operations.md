# Douyin Creator Marketplace (Xingtu) Author Commerce Seeding Base Info operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/aggregator/get_author_commerce_seed_base_info`.

## `gwApiAggregatorGetAuthorCommerceSeedBaseInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/aggregator/get_author_commerce_seed_base_info/v1`
- Summary: Author Commerce Seeding Base Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Seeding Base Info data, including baseline metrics, commercial signals, and seeding indicators, for product seeding analysis, creator vetting, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `range` | `query` | no | `string` | `DAY_90` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |

### Request body

No request body.

### Responses

- `200`: OK
