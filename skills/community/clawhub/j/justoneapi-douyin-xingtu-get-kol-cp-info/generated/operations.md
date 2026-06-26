# Douyin Creator Marketplace (Xingtu) Cost Performance Analysis operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-cp-info`.

## `getKolCpInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-cp-info/v1`
- Summary: Cost Performance Analysis
- Description: Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.
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
