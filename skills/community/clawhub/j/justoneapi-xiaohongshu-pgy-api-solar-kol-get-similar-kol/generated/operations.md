# Xiaohongshu Creator Marketplace (Pugongying) Similar Creators operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/get_similar_kol`.

## `apiSolarKolGetSimilarKolV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1`
- Summary: Similar Creators
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) similar Creators data, including audience signals, for creator discovery, benchmarking, and shortlist building.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |
| `pageNum` | `query` | no | `integer` | `1` | Page number for results. |

### Request body

No request body.

### Responses

- `200`: OK
