# Facebook operations

Generated from JustOneAPI OpenAPI for platform key `facebook`.

## `getProfileIdV1`

- Method: `GET`
- Path: `/api/facebook/get-profile-id/v1`
- Summary: Get Profile ID
- Description: Retrieve the unique Facebook profile ID from a given profile URL.
- Tags: `Facebook`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User security token for API access authentication. |
| `url` | `query` | yes | `string` | n/a | The path part of the Facebook profile URL. Do not include `https://www.facebook.com`. Example: `/people/To-Bite/pfbid021XLeDjjZjsoWse1H43VEgb3i1uCLTpBvXSvrnL2n118YPtMF5AZkBrZobhWWdHTHl/` |

### Request body

No request body.

### Responses

- `200`: OK

## `getProfilePostsV1`

- Method: `GET`
- Path: `/api/facebook/get-profile-posts/v1`
- Summary: Get Profile Posts
- Description: Get public posts from a specific Facebook profile using its profile ID.
- Tags: `Facebook`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User security token for API access authentication. |
| `profileId` | `query` | yes | `string` | n/a | The unique Facebook profile ID. |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor for fetching the next set of results. |

### Request body

No request body.

### Responses

- `200`: OK

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
