# Xiaohongshu Creator Marketplace (Pugongying) Follower Distribution operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/data/userId/fans_profile`.

## `apiSolarKolDataUserIdFansProfileV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_profile/v1`
- Summary: Follower Distribution
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) follower distribution data, including audience demographics, interests, and distribution metrics, for creator evaluation, campaign planning, and creator benchmarking.
- Tags: `Xiaohongshu Creator Marketplace (Pugongying)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `userId` | `query` | yes | `string` | n/a | KOL's user ID. |

### Request body

No request body.

### Responses

- `200`: OK
