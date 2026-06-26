# Twitter User Published Posts operations

Generated from JustOneAPI OpenAPI for platform key `twitter`.

Endpoint group: `get-user-posts`.

## `getTwitterUserPostsV1`

- Method: `GET`
- Path: `/api/twitter/get-user-posts/v1`
- Summary: User Published Posts
- Description: Get Twitter user Published Posts data, including post content, timestamps, and engagement data, for account monitoring and content analysis.
- Tags: `Twitter`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required for API access. |
| `restId` | `query` | yes | `string` | n/a | The unique numeric identifier (Rest ID) for the X user. |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor for navigating through long timelines. |

### Request body

No request body.

### Responses

- `200`: OK
