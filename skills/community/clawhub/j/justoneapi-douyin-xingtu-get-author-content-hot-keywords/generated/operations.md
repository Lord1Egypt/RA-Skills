# Douyin Creator Marketplace (Xingtu) KOL Content Keyword Analysis operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-author-content-hot-keywords`.

## `getAuthorContentHotKeywordsV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-content-hot-keywords/v1`
- Summary: KOL Content Keyword Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Content Keyword Analysis data, including core metrics, trend signals, and performance indicators, for content theme analysis and creator positioning research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `keywordType` | `query` | no | `string` | `0` | Type of keywords. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
