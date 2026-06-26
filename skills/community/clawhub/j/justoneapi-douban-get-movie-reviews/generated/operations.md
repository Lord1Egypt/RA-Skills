# Douban Movie Movie Reviews operations

Generated from JustOneAPI OpenAPI for platform key `douban`.

Endpoint group: `get-movie-reviews`.

## `getMovieReviewsV1`

- Method: `GET`
- Path: `/api/douban/get-movie-reviews/v1`
- Summary: Movie Reviews
- Description: Get Douban movie Reviews data, including review titles, ratings, and snippets, for audience sentiment analysis and review research.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `subjectId` | `query` | yes | `string` | n/a | The unique ID for a movie or TV subject on Douban. |
| `sort` | `query` | no | `string` | `time` | Sort order for the result set.

Available Values:
- `time`: Time
- `hotest`: Hotest |
| enum | values | no | n/a | n/a | `time`, `hotest` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
