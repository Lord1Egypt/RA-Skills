# Douyin Creator Marketplace (Xingtu) Creator Profile operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/author/get_author_base_info`.

## `gwApiAuthorGetAuthorBaseInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/author/get_author_base_info/v1`
- Summary: Creator Profile
- Description: Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
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
