# Douyin Creator Marketplace (Xingtu) Creator Link Metrics operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-link-info`.

## `getKolLinkInfoV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-link-info/v1`
- Summary: Creator Link Metrics
- Description: Get Douyin Creator Marketplace (Xingtu) creator Link Metrics data, including creator ranking, traffic structure, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `industryTag` | `query` | no | `string` | n/a | Industry Tag. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
