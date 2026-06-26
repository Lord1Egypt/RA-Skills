# Twitter User Profile operations

Generated from JustOneAPI OpenAPI for platform key `twitter`.

Endpoint group: `get-user-detail`.

## `getTwitterUserDetailV1`

- Method: `GET`
- Path: `/api/twitter/get-user-detail/v1`
- Summary: User Profile
- Description: Get Twitter user Profile data, including account metadata, audience metrics, and verification-related fields, for accessing user profile metadata (e.g., description, location, verification status) and collecting follower and following counts.
- Tags: `Twitter`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required for API access. |
| `restId` | `query` | yes | `string` | n/a | The unique numeric identifier (Rest ID) for the X user. |

### Request body

No request body.

### Responses

- `200`: OK
