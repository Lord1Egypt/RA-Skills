# Douyin Creator Marketplace (Xingtu) Video Distribution operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/author_video_distribution`.

## `gwApiDataSpAuthorVideoDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_video_distribution/v1`
- Summary: Video Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) video Distribution data, including content performance breakdowns across published videos, for creator evaluation, campaign planning, and marketplace research.
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
