# Douyin Creator Marketplace (Xingtu) Creator Link Structure operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/data_sp/author_link_struct`.

## `gwApiDataSpAuthorLinkStructV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/data_sp/author_link_struct/v1`
- Summary: Creator Link Structure
- Description: Get Douyin Creator Marketplace (Xingtu) creator Link Structure data, including engagement and conversion metrics, for creator performance analysis.
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
