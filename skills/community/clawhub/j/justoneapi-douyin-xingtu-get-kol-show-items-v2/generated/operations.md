# Douyin Creator Marketplace (Xingtu) Showcase Items operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-show-items-v2`.

## `getKolShowItemsV2V1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-show-items-v2/v1`
- Summary: Showcase Items
- Description: Get Douyin Creator Marketplace (Xingtu) showcase items data, including core metrics, trend signals, and performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `onlyAssign` | `query` | no | `boolean` | `false` | Whether true is Xingtu video, false is personal video. |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
