# TikTok User Search operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `search-user`.

## `searchUserV1`

- Method: `GET`
- Path: `/api/tiktok/search-user/v1`
- Summary: User Search
- Description: Get TikTok user Search data, including basic profile information such as user ID, nickname, and unique handle, for discovering influencers in specific niches via keywords and identifying target audiences and conducting competitor research.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `keyword` | `query` | yes | `string` | n/a | Search keywords (e.g., 'deepseek'). |
| `cursor` | `query` | no | `string` | `0` | Pagination cursor. Start with '0'. |
| `searchId` | `query` | no | `string` | n/a | The 'logid' returned from the previous request for consistent search results. |

### Request body

No request body.

### Responses

- `200`: OK
