# Xiaohongshu (RedNote) operations

Generated from JustOneAPI OpenAPI for platform key `xiaohongshu`.

## `getNoteCommentV2`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-comment/v2`
- Summary: Note Comments
- Description: Get Xiaohongshu (RedNote) note Comments data, including text, authors, and timestamps, for feedback analysis.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (use the cursor value returned by the last response). |
| `sort` | `query` | no | `string` | `latest` | Sort order for the result set.

Available Values:
- `normal`: Normal
- `latest`: Latest |
| enum | values | no | n/a | n/a | `normal`, `latest` |

### Request body

No request body.

### Responses

- `200`: OK

## `getNoteCommentV4`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-comment/v4`
- Summary: Note Comments
- Description: Get Xiaohongshu (RedNote) note Comments data, including comment text, author profiles, and interaction data, for sentiment analysis and community monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK

## `getXiaohongshuNoteDetailV1`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-detail/v1`
- Summary: Note Details
- Description: Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK

## `getNoteDetailV3`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-detail/v3`
- Summary: Note Details
- Description: Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK

## `getNoteDetailV7`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-detail/v7`
- Summary: Note Details
- Description: Get Xiaohongshu (RedNote) note Details data, including media and engagement metrics, for content analysis, archiving, and campaign research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK

## `getNoteSubCommentV2`

- Method: `GET`
- Path: `/api/xiaohongshu/get-note-sub-comment/v2`
- Summary: Comment Replies
- Description: Get Xiaohongshu (RedNote) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `noteId` | `query` | yes | `string` | n/a | Unique note identifier on Xiaohongshu. |
| `commentId` | `query` | yes | `string` | n/a | Unique comment identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (use the cursor value returned by the last response). |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserNoteListV2`

- Method: `GET`
- Path: `/api/xiaohongshu/get-user-note-list/v2`
- Summary: User Published Notes
- Description: Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Unique user identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (the last note's cursor value). |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserNoteListV4`

- Method: `GET`
- Path: `/api/xiaohongshu/get-user-note-list/v4`
- Summary: User Published Notes
- Description: Get Xiaohongshu (RedNote) user Published Notes data, including note metadata, covers, and publish times, for account monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Unique user identifier on Xiaohongshu. |
| `lastCursor` | `query` | no | `string` | n/a | Pagination cursor from the previous page (the last note's cursor value). |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserV3`

- Method: `GET`
- Path: `/api/xiaohongshu/get-user/v3`
- Summary: User Profile
- Description: Get Xiaohongshu (RedNote) user Profile data, including follower counts and bio details, for creator research, account analysis, and competitor monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Unique user identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK

## `getUserV4`

- Method: `GET`
- Path: `/api/xiaohongshu/get-user/v4`
- Summary: User Profile
- Description: Get Xiaohongshu (RedNote) user Profile data, including follower counts and bio details, for creator research, account analysis, and competitor monitoring.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | Unique user identifier on Xiaohongshu. |

### Request body

No request body.

### Responses

- `200`: OK

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

## `searchRecommendV1`

- Method: `GET`
- Path: `/api/xiaohongshu/search-recommend/v1`
- Summary: Keyword Suggestions
- Description: Get Xiaohongshu (RedNote) keyword Suggestions data, including suggested queries, keyword variants, and query metadata, for expanding keyword sets for content research and seo/pseo workflows and improving search coverage by using platform-recommended terms.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |

### Request body

No request body.

### Responses

- `200`: OK

## `getSearchUserV2`

- Method: `GET`
- Path: `/api/xiaohongshu/search-user/v2`
- Summary: User Search
- Description: Get Xiaohongshu (RedNote) user Search data, including profile metadata and public signals, for creator discovery and account research.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `keyword` | `query` | yes | `string` | n/a | Search keyword. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

## `shareXiaohongshuUrlTransferV1`

- Method: `GET`
- Path: `/api/xiaohongshu/share-url-transfer/v1`
- Summary: Share Link Resolution
- Description: Get Xiaohongshu (RedNote) share Link Resolution data, including helping extract note IDs, for downstream note and comment workflows.
- Tags: `Xiaohongshu (RedNote)`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `shareUrl` | `query` | yes | `string` | n/a | RedNote share link URL to be resolved (short link or shared URL). |

### Request body

No request body.

### Responses

- `200`: OK
