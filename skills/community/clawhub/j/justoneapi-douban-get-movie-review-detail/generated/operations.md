# Douban Movie Review Details operations

Generated from JustOneAPI OpenAPI for platform key `douban`.

Endpoint group: `get-movie-review-detail`.

## `getMovieReviewDetailsV1`

- Method: `GET`
- Path: `/api/douban/get-movie-review-detail/v1`
- Summary: Review Details
- Description: Get Douban movie Review Details data, including metadata, content fields, and engagement signals, for review archiving and detailed opinion analysis.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `reviewId` | `query` | yes | `string` | n/a | The unique ID for a specific review on Douban. |

### Request body

No request body.

### Responses

- `200`: OK
