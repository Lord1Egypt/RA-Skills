# TikTok User Profile operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `get-user-detail`.

## `getTiktokUserDetailV1`

- Method: `GET`
- Path: `/api/tiktok/get-user-detail/v1`
- Summary: User Profile
- Description: Get TikTok user Profile data, including nickname, unique ID, and avatar, for influencer profiling and audience analysis, account performance tracking and growth monitoring, and identifying verified status and official accounts.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `uniqueId` | `query` | no | `string` | n/a | The unique handle/username of the user (e.g., 'tiktok'). |
| `secUid` | `query` | no | `string` | n/a | The unique security ID of the user. |

### Request body

No request body.

### Responses

- `200`: OK
