# Douyin Creator Marketplace (Xingtu) Showcase Items operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `gw/api/author/get_author_show_items_v2`.

## `gwApiAuthorGetAuthorShowItemsV2V1`

- Method: `GET`
- Path: `/api/douyin-xingtu/gw/api/author/get_author_show_items_v2/v1`
- Summary: Showcase Items
- Description: Get Douyin Creator Marketplace (Xingtu) showcase Items data, including products and videos associated with the account, for creator evaluation, campaign planning, and marketplace research.
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
| `onlyAssign` | `query` | no | `boolean` | `false` | Whether to only include assigned items. |
| `flowType` | `query` | no | `string` | `EXCLUDE` | Flow type filter.

Available Values:
- `EXCLUDE`: Exclude
- `INCLUDE`: Include |
| enum | values | no | n/a | n/a | `EXCLUDE`, `INCLUDE` |

### Request body

No request body.

### Responses

- `200`: OK
