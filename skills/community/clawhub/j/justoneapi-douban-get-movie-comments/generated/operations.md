# Douban Movie Comments operations

Generated from JustOneAPI OpenAPI for platform key `douban`.

Endpoint group: `get-movie-comments`.

## `getMovieCommentsV1`

- Method: `GET`
- Path: `/api/douban/get-movie-comments/v1`
- Summary: Comments
- Description: Get Douban movie Comments data, including ratings, snippets, and interaction counts, for quick sentiment sampling and review monitoring.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `subjectId` | `query` | yes | `string` | n/a | The unique ID for a movie or TV subject on Douban. |
| `sort` | `query` | no | `string` | `time` | Sort order for the result set.

Available Values:
- `time`: Time
- `new_score`: New Score |
| enum | values | no | n/a | n/a | `time`, `new_score` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
