# Facebook Get Profile Posts operations

Generated from JustOneAPI OpenAPI for platform key `facebook`.

Endpoint group: `get-profile-posts`.

## `getProfilePostsV1`

- Method: `GET`
- Path: `/api/facebook/get-profile-posts/v1`
- Summary: Get Profile Posts
- Description: Get public posts from a specific Facebook profile using its profile ID.
- Tags: `Facebook`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User security token for API access authentication. |
| `profileId` | `query` | yes | `string` | n/a | The unique Facebook profile ID. |
| `cursor` | `query` | no | `string` | n/a | Pagination cursor for fetching the next set of results. |

### Request body

No request body.

### Responses

- `200`: OK
