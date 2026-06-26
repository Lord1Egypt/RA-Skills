# Douyin Creator Marketplace (Xingtu) Follower Distribution operations

Generated from JustOneAPI OpenAPI for platform key `douyin-xingtu`.

Endpoint group: `get-kol-fans-distribution`.

## `getKolFansDistributionV1`

- Method: `GET`
- Path: `/api/douyin-xingtu/get-kol-fans-distribution/v1`
- Summary: Follower Distribution
- Description: Get Douyin Creator Marketplace (Xingtu) follower distribution data, including audience demographics, interests, and distribution metrics, for creator evaluation, campaign planning, and marketplace research.
- Tags: `Douyin Creator Marketplace (Xingtu)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `kolId` | `query` | yes | `string` | n/a | KOL ID. |
| `fansType` | `query` | no | `string` | `_1` | Fans type.

Available Values:
- `_1`: Fans Portrait
- `_2`: Fans Group Portrait
- `_5`: Iron Fans Portrait |
| enum | values | no | n/a | n/a | `_1`, `_2`, `_5` |
| `acceptCache` | `query` | no | `boolean` | `false` | Enable cache. |

### Request body

No request body.

### Responses

- `200`: OK
