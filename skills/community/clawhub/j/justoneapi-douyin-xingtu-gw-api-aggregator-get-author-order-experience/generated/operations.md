# Douyin Creator Marketplace (Xingtu) Creator Order Experience operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/aggregator/get_author_order_experience`.

## `gwApiAggregatorGetAuthorOrderExperienceV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/aggregator/get_author_order_experience/v1`
- Summary: Creator Order Experience
- Description: Get Douyin Creator Marketplace (Xingtu) creator Order Experience data, including commercial history and transaction-related indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `period` | `query` | no | `string` | `DAY_30` | Time period.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |

### Request body

No request body.

### Responses

- `200`: OK
