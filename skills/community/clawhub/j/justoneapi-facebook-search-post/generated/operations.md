# Facebook Post Search operations

Generated from JustOneAPI OpenAPI for platform key `facebook`.

Endpoint group: `search-post`.

## `searchFacebookPostsV1`

- Method: `GET`
- Path: `/api/facebook/search-post/v1`
- Summary: Post Search
- Description: Get Facebook post Search data, including matched results, metadata, and ranking signals, for discovering relevant public posts for specific keywords and analyzing engagement and reach of public content on facebook.
- Tags: `Facebook`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User security token for API access authentication. |
| `keyword` | `query` | yes | `string` | n/a | Keyword to search for in public posts. Supports basic text matching. |
| `startDate` | `query` | no | `string` | n/a | Start date for the search range (inclusive), formatted as yyyy-MM-dd. |
| `endDate` | `query` | no | `string` | n/a | End date for the search range (inclusive), formatted as yyyy-MM-dd. |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor for fetching the next set of results. |

### Request body

No request body.

### Responses

- `200`: OK
