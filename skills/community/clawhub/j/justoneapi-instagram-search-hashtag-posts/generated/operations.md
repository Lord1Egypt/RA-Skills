# Instagram Hashtag Posts Search operations

Generated from JustOneAPI OpenAPI for platform key `instagram`.

Endpoint group: `search-hashtag-posts`.

## `searchHashtagPostsV1`

- Method: `GET`
- Path: `/api/instagram/search-hashtag-posts/v1`
- Summary: Hashtag Posts Search
- Description: Get Instagram hashtag Posts Search data, including caption, author profile, and publish time, for competitive analysis of trending topics and hashtags and monitoring community discussions and public opinion on specific tags.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `hashtag` | `query` | yes | `string` | n/a | The hashtag or keyword to search for. |
| `endCursor` | `query` | no | `string` | n/a | Cursor used for retrieving the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK
