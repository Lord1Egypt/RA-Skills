# Social Media operations

Generated from JustOneAPI OpenAPI for platform key `search`.

## `searchCrossPlatformV1`

- Method: `GET`
- Path: `/api/search/v1`
- Summary: Cross-Platform Search
- Description: Get cross-platform social media search data, including Xiaohongshu, Douyin, Kuaishou, WeChat, Bilibili, Weibo and Zhihu results, for trend research and monitoring.
- Tags: `Social Media`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | no | `string` | n/a | Search query string. Supports:
- Multiple keywords (AND): keyword1 keyword2
- Multiple keywords (OR): keyword1~keyword2
- Excluded keywords (NOT): required_keyword -excluded_keyword |
| `source` | `query` | no | `string` | `ALL` | Target social media platform for search filtering.

Available Values:
- `ALL`: All platforms
- `NEWS`: News
- `WEIBO`: Sina Weibo
- `WEIXIN`: Weixin (WeChat)
- `ZHIHU`: Zhihu
- `DOUYIN`: Douyin (TikTok China)
- `XIAOHONGSHU`: Xiaohongshu (Little Red Book)
- `BILIBILI`: Bilibili
- `KUAISHOU`: Kuaishou |
| enum | values | no | n/a | n/a | `ALL`, `NEWS`, `WEIBO`, `WEIXIN`, `ZHIHU`, `DOUYIN`, `XIAOHONGSHU`, `BILIBILI`, `KUAISHOU` |
| `start` | `query` | no | `string` | n/a | Start time of the search period (yyyy-MM-dd HH:mm:ss). Required for initial request. |
| `end` | `query` | no | `string` | n/a | End time of the search period (yyyy-MM-dd HH:mm:ss). Required for initial request. |
| `nextCursor` | `query` | no | `string` | n/a | Pagination cursor provided by the 'nextCursor' field in the previous response. |

### Request body

No request body.

### Responses

- `200`: OK
