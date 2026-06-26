# TikTok User Published Posts operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `get-user-post`.

## `getUserPostV1`

- Method: `GET`
- Path: `/api/tiktok/get-user-post/v1`
- Summary: User Published Posts
- Description: Get TikTok user Published Posts data, including video ID, description, and publish time, for user activity analysis and posting frequency tracking, influencer performance evaluation, and content trend monitoring for specific creators.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `secUid` | `query` | yes | `string` | n/a | The unique security ID of the TikTok user (e.g., MS4wLjABAAAAonP2...). |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Use '0' for the first page, then use the 'cursor' value returned in the previous response. |
| `sort` | `query` | no | `string` | `_0` | Sorting criteria for the user's posts.

Available Values:
- `_0`: Default (Mixed)
- `_1`: Highest Liked
- `_2`: Latest Published |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2` |

### Request body

No request body.

### Responses

- `200`: OK
