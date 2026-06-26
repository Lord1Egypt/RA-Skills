# Instagram User Profile operations

Generated from JustOneAPI OpenAPI for platform key `instagram`.

Endpoint group: `get-user-detail`.

## `getInstagramUserDetailV1`

- Method: `GET`
- Path: `/api/instagram/get-user-detail/v1`
- Summary: User Profile
- Description: Get Instagram user Profile data, including follower count, following count, and post count, for obtaining basic account metadata for influencer vetting, tracking follower growth and audience reach over time, and mapping user handles to specific profile stats.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `username` | `query` | yes | `string` | n/a | The Instagram username whose profile details are to be retrieved. |

### Request body

No request body.

### Responses

- `200`: OK
