# Douyin (TikTok China) User Profile operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `get-user-detail`.

## `getUserDetailV3`

- Method: `GET`
- Path: `/api/douyin/get-user-detail/v3`
- Summary: User Profile
- Description: Get Douyin (TikTok China) user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `secUid` | `query` | yes | `string` | n/a | The unique user ID (sec_uid) on Douyin. |

### Request body

No request body.

### Responses

- `200`: OK
