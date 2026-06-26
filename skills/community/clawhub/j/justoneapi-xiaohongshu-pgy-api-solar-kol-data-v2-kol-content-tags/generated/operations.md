# Xiaohongshu Creator Marketplace (Pugongying) Creator Content Tags operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu-pgy`.

Endpoint group: `api/solar/kol/dataV2/kolContentTags`.

## `apiSolarKolDataV2KolContentTagsV1`

- Method: `GET`
- Path: `/api/xiaohongshu-pgy/api/solar/kol/dataV2/kolContentTags/v1`
- Summary: Creator Content Tags
- Description: Get Xiaohongshu Creator Marketplace (Pugongying) creator Content Tags data, including topic labels that describe publishing themes and content focus, for creator evaluation, campaign planning, and creator benchmarking.
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
