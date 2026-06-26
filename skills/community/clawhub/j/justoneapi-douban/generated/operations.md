# Douban Movie operations

Generated from JustOneAPI OpenAPI for platform key `douban`.

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

## `getRecentHotMovieV1`

- Method: `GET`
- Path: `/api/douban/get-recent-hot-movie/v1`
- Summary: Recent Hot Movie
- Description: Get Douban recent Hot Movie data, including ratings, posters, and subject metadata, for movie discovery and trend monitoring.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

## `getRecentHotTvV1`

- Method: `GET`
- Path: `/api/douban/get-recent-hot-tv/v1`
- Summary: Recent Hot Tv
- Description: Get Douban recent Hot Tv data, including ratings, posters, and subject metadata, for series discovery and trend monitoring.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK

## `getSubjectDetailV1`

- Method: `GET`
- Path: `/api/douban/get-subject-detail/v1`
- Summary: Subject Details
- Description: Get Douban subject Details data, including title, rating, and cast, for title enrichment and catalog research.
- Tags: `Douban Movie`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `subjectId` | `query` | yes | `string` | n/a | The unique ID for a movie or TV subject on Douban. |

### Request body

No request body.

### Responses

- `200`: OK
