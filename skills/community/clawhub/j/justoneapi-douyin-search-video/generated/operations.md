# Douyin (TikTok China) Video Search operations

Generated from JustOneAPI OpenAPI for platform key `douyin`.

Endpoint group: `search-video`.

## `searchVideoV4`

- Method: `GET`
- Path: `/api/douyin/search-video/v4`
- Summary: Video Search
- Description: Get Douyin (TikTok China) video Search data, including metadata and engagement signals, for content discovery, trend research, and competitive monitoring.
- Tags: `Douyin (TikTok China)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword. |
| `sortType` | `query` | no | `string` | `_0` | Sorting criteria for search results.

Available Values:
- `_0`: General
- `_1`: More likes
- `_2`: Newest |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2` |
| `publishTime` | `query` | no | `string` | `_0` | Filter by video publish time range.

Available Values:
- `_0`: No Limit
- `_1`: Last 24 Hours
- `_7`: Last 7 Days
- `_180`: Last 6 Months |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_7`, `_180` |
| `duration` | `query` | no | `string` | `_0` | Filter by video duration.

Available Values:
- `_0`: No Limit
- `_1`: Under 1 Minute
- `_2`: 1-5 Minutes
- `_3`: Over 5 Minutes |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2`, `_3` |
| `page` | `query` | no | `integer` | `1` | Page number (starting from 1). |
| `searchId` | `query` | no | `string` | n/a | Search ID; required for pages > 1 (use the search_id value returned by the last response). |

### Request body

No request body.

### Responses

- `200`: OK
