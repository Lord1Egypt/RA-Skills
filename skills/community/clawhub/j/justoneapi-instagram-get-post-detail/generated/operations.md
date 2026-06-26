# Instagram Post Details operations

Generated from JustOneAPI OpenAPI for platform key `instagram`.

Endpoint group: `get-post-detail`.

## `getInstagramPostDetailV1`

- Method: `GET`
- Path: `/api/instagram/get-post-detail/v1`
- Summary: Post Details
- Description: Get Instagram post Details data, including post caption, media content (images/videos), and publish time, for analyzing engagement metrics (likes/comments) for a specific post and archiving post content and media assets for content analysis.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `code` | `query` | yes | `string` | n/a | The unique shortcode (slug) for the Instagram post (e.g., 'DRhvwVLAHAG'). |

### Request body

No request body.

### Responses

- `200`: OK
