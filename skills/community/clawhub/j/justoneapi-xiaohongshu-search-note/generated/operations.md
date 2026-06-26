# Xiaohongshu (RedNote) Note Search operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

Endpoint group: `search-note`.

## `getSearchNoteV2`

- Method: `GET`
- Path: `/api/xiaohongshu/search-note/v2`
- Summary: Note Search
- Description: Get Xiaohongshu (RedNote) note Search data, including snippets, authors, and media, for topic discovery.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |
| `sort` | `query` | no | `string` | `general` | Sort order for the result set.

Available Values:
- `general`: General
- `popularity_descending`: Popularity Descending
- `time_descending`: Time Descending
- `comment_descending`: Comment Descending
- `collect_descending`: Collect Descending |
| enum | values | no | n/a | n/a | `general`, `popularity_descending`, `time_descending`, `comment_descending`, `collect_descending` |
| `noteType` | `query` | no | `string` | `_0` | Note type filter.

Available Values:
- `_0`: General
- `_1`: Video
- `_2`: Normal |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2` |
| `noteTime` | `query` | no | `string` | n/a | Note publish time filter. This parameter is for reference only and does not have much effect.

Available Values:
- `一天内`: Within one day
- `一周内`: Within a week
- `半年内`: Within half a year |
| enum | values | no | n/a | n/a | `一天内`, `一周内`, `半年内` |

### Request body

No request body.

### Responses

- `200`: OK

## `getSearchNoteV3`

- Method: `GET`
- Path: `/api/xiaohongshu/search-note/v3`
- Summary: Note Search
- Description: Get Xiaohongshu (RedNote) note Search data, including snippets, authors, and media, for topic discovery.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |
| `sort` | `query` | no | `string` | `general` | Sort order for the result set.

Available Values:
- `general`: General
- `popularity_descending`: Hot
- `time_descending`: New |
| enum | values | no | n/a | n/a | `general`, `popularity_descending`, `time_descending` |
| `noteType` | `query` | no | `string` | `_0` | Note type filter.

Available Values:
- `_0`: General
- `_1`: Video
- `_2`: Normal |
| enum | values | no | n/a | n/a | `_0`, `_1`, `_2` |

### Request body

No request body.

### Responses

- `200`: OK
