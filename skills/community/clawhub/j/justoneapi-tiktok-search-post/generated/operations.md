# TikTok Post Search operations

Generated from JustOneAPI OpenAPI for platform key `tiktok`.

Endpoint group: `search-post`.

## `searchPostV1`

- Method: `GET`
- Path: `/api/tiktok/search-post/v1`
- Summary: Post Search
- Description: Get TikTok post Search data, including key details such as video ID, description, and author information, for trend monitoring and content discovery and keyword-based market analysis and sentiment tracking.
- Tags: `TikTok`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Security token for API access. |
| `keyword` | `query` | yes | `string` | n/a | Search keywords (e.g., 'deepseek'). |
| `offset` | `query` | no | `integer` | `0` | Pagination offset, starting from 0 and stepping by 20. |
| `sortType` | `query` | no | `string` | `RELEVANCE` | Sorting criteria for search results.

Available Values:
- `RELEVANCE`: Relevance (Default)
- `MOST_LIKED`: Most Liked |
| enum | values | no | n/a | n/a | `RELEVANCE`, `MOST_LIKED` |
| `publishTime` | `query` | no | `string` | `ALL` | Filter posts by publishing time.

Available Values:
- `ALL`: All Time
- `ONE_DAY`: Last 24 Hours
- `ONE_WEEK`: Last 7 Days
- `ONE_MONTH`: Last 30 Days
- `THREE_MONTHS`: Last 90 Days
- `HALF_YEAR`: Last 180 Days |
| enum | values | no | n/a | n/a | `ALL`, `ONE_DAY`, `ONE_WEEK`, `ONE_MONTH`, `THREE_MONTHS`, `HALF_YEAR` |
| `region` | `query` | no | `string` | `US` | ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB'). |

### Request body

No request body.

### Responses

- `200`: OK
