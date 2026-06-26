# Douyin Creator Marketplace (Xingtu) Item Report Trends operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/item_report_trend`.

## `gwApiDataSpItemReportTrendV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/item_report_trend/v1`
- Summary: Item Report Trends
- Description: Get Douyin Creator Marketplace (Xingtu) item Report Trend data, including time-based changes in item performance metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `itemId` | `query` | yes | `string` | n/a | Item's unique ID. |

### Request body

No request body.

### Responses

- `200`: OK
