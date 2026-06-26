# Douyin Creator Marketplace (Xingtu) Follower Growth Trend operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/get_author_daily_fans`.

## `gwApiDataSpGetAuthorDailyFansV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_daily_fans/v1`
- Summary: Follower Growth Trend
- Description: Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `startDate` | `query` | yes | `string` | n/a | Start Date (yyyy-MM-dd). |
| `endDate` | `query` | yes | `string` | n/a | End Date (yyyy-MM-dd). |

### Request body

No request body.

### Responses

- `200`: OK
