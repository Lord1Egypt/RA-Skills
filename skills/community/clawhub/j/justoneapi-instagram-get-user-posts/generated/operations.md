# Instagram User Published Posts operations

Generated from JustOneAPI OpenAPI for platform key `instagram`.

Endpoint group: `get-user-posts`.

## `getInstagramUserPostsV1`

- Method: `GET`
- Path: `/api/instagram/get-user-posts/v1`
- Summary: User Published Posts
- Description: Get Instagram user Published Posts data, including post code, caption, and media type, for monitoring recent publishing activity of a specific user and building a historical record of content for auditing or analysis.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `username` | `query` | yes | `string` | n/a | The Instagram username whose published posts are to be retrieved. |
| `paginationToken` | `query` | no | `string` | n/a | Token used for retrieving the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK
