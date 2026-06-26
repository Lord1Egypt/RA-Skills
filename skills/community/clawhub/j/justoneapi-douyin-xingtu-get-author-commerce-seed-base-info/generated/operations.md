# Douyin Creator Marketplace (Xingtu) Author Commerce Seeding Base Info operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-author-commerce-seed-base-info`.

## `getAuthorCommerceSeedingBaseInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-commerce-seed-base-info/v1`
- Summary: Author Commerce Seeding Base Info
- Description: Get Douyin Creator Marketplace (Xingtu) author Commerce Seeding Base Info data, including baseline metrics, commercial signals, and seeding indicators, for product seeding analysis, creator vetting, and campaign planning.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `range` | `query` | yes | `string` | n/a | Time range. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
