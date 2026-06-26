# Douyin Creator Marketplace (Xingtu) KOL Comment Keyword Analysis operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-author-hot-comment-tokens`.

## `getAuthorHotCommentTokensV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-author-hot-comment-tokens/v1`
- Summary: KOL Comment Keyword Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) kOL Comment Keyword Analysis data, including core metrics, trend signals, and performance indicators, for audience language analysis and comment-topic research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
