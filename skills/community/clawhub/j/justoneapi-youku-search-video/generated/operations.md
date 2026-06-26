# YOUKU Video Search operations

Generated from JustOneAPI OpenAPI for platform key `youku`.

Endpoint group: `search-video`.

## `searchVideoV1`

- Method: `GET`
- Path: `/api/youku/search-video/v1`
- Summary: Video Search
- Description: Get YOUKU video Search data, including video ID, title, and cover image, for keyword-based video discovery, monitoring specific topics or trends on youku, and analyzing search results for market research.
- Tags: `YOUKU`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `keyword` | `query` | yes | `string` | n/a | Keyword to search for. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination, starting from 1. |

### Request body

No request body.

### Responses

- `200`: OK
