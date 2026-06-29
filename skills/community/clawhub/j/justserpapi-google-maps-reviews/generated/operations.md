# Google SERP Maps Reviews operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `maps/reviews`.

## `mapsReviews`

- Method: `GET`
- Path: `/api/v1/google/maps/reviews`
- Summary: Reviews
- Description: Get Google maps Reviews data, including ratings and reviewer metadata, for reputation analysis and review monitoring.
- Tags: `Google Maps`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `data_id` | `query` | yes | `string` | n/a | The unique Google Maps location ID (feature ID). You can get this from our Google Maps Search API. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `sort_by` | `query` | no | `string` | n/a | Sorting order for reviews. Supported values: 'qualityScore' (Relevance), 'newestFirst' (Newest), 'ratingHigh' (Highest rating), 'ratingLow' (Lowest rating). |
| `topic_id` | `query` | no | `string` | n/a | Filter reviews by a specific topic ID. Topic IDs are obtained from previous Maps Reviews API responses. |
| `next_page_token` | `query` | no | `string` | n/a | Token for retrieving the next page of reviews. |
| `results` | `query` | no | `integer` | n/a | The maximum number of reviews to return per page (range: 1-20). |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
