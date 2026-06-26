# Douyin Creator Marketplace (Xingtu) Follower Distribution operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/get_author_fans_distribution`.

## `gwApiDataSpGetAuthorFansDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_fans_distribution/v1`
- Summary: Follower Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) follower Distribution data, including audience segmentation and location and demographic breakdowns, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `oAuthorId` | `query` | yes | `string` | n/a | Author's unique ID. |
| `authorType` | `query` | no | `string` | `FAN` | Author type filter.

Available Values:
- `FAN`: Fan
- `DIE_HARD_FAN`: Die Hard Fan |
| enum | values | no | n/a | n/a | `FAN`, `DIE_HARD_FAN` |

### Request body

No request body.

### Responses

- `200`: OK
