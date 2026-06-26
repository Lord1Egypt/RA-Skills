# Douyin Creator Marketplace (Xingtu) KOL Keyword Search operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `search-kol-simple`.

## `searchKolSimpleV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/search-kol-simple/v1`
- Summary: KOL Keyword Search
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Keyword Search data, including matching creators and discovery data, for creator sourcing and shortlist building.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `keyword` | `query` | yes | `string` | n/a | Search keywords. |
| `platformSource` | `query` | yes | `string` | n/a | Platform source.

Available Values:
- `_1`: Douyin
- `_2`: Toutiao
- `_3`: Xigua |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_3` |
| `page` | `query` | yes | `integer` | n/a | Page number. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
