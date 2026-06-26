# Douyin Creator Marketplace (Xingtu) Conversion Analysis operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/get_author_convert_ability`.

## `gwApiDataSpGetAuthorConvertAbilityV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/get_author_convert_ability/v1`
- Summary: Conversion Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) conversion Analysis data, including conversion efficiency and commercial performance indicators, for creator evaluation, campaign planning, and marketplace research.
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
| `range` | `query` | no | `string` | `DAY_30` | Time range.

Available Values:
- `DAY_30`: Last 30 days
- `DAY_90`: Last 90 days |
| enum | values | no | n/a | n/a | `DAY_30`, `DAY_90` |

### Request body

No request body.

### Responses

- `200`: OK
