# Google SERP Maps Posts operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `maps/posts`.

## `mapsPosts`

- Method: `GET`
- Path: `/api/v1/google/maps/posts`
- Summary: Posts
- Description: Get Google maps Posts data, including business post content, post dates and images, and profile-specific feeds, for local business monitoring and promotion tracking.
- Tags: `Google Maps`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `data_id` | `query` | yes | `string` | n/a | The unique Google Maps location ID (feature ID). You can get this from our Google Maps Search API. |
| `next_page_token` | `query` | no | `string` | n/a | Token used to retrieve the next page of business posts. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
