# Douyin (TikTok China) User Search operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `search-user`.

## `searchDouyinUserV2`

- Method: `GET`
- Path: `/api/douyin/search-user/v2`
- Summary: User Search
- Description: Get Douyin (TikTok China) user Search data, including profile metadata and follower signals, for creator discovery and account research.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number (starting from 1). |
| `userType` | `query` | no | `string` | n/a | Filter by user type.

Available Values:
- `common_user`: Common User
- `enterprise_user`: Enterprise User
- `personal_user`: Verified Individual User |
| enum | values | no | n/a | n/a | `common_user`, `enterprise_user`, `personal_user` |

### Request body

No request body.

### Responses

- `200`: OK
