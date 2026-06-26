# Douyin Creator Marketplace (Xingtu) Audience Touchpoint Distribution operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/author_touch_distribution`.

## `gwApiDataSpAuthorTouchDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_touch_distribution/v1`
- Summary: Audience Touchpoint Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) audience Touchpoint Distribution data, including segment breakdowns, audience composition, and distribution signals, for creator evaluation, campaign planning, and marketplace research.
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

### Request body

No request body.

### Responses

- `200`: OK
