# Bilibili Video Search operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `search-video`.

## `searchBilibiliVideoV2`

- Method: `GET`
- Path: `/api/bilibili/search-video/v2`
- Summary: Video Search
- Description: Get Bilibili video Search data, including matched videos, creators, and engagement metrics, for topic research and content discovery.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `page` | `query` | no | `string` | n/a | Page number for pagination. |
| `order` | `query` | no | `string` | `general` | Sorting criteria for search results.

Available Values:
- `general`: General
- `click`: Most Played
- `pubdate`: Latest
- `dm`: Most Danmaku
- `stow`: Most Favorite |
| enum | values | no | n/a | n/a | `general`, `click`, `pubdate`, `dm`, `stow` |

### Request body

No request body.

### Responses

- `200`: OK
