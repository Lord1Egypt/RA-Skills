# YOUKU User Profile operations

Generated from JustOneAPI OpenAPI for platform key `youku`.

Endpoint group: `get-user-detail`.

## `getYoukuUserDetailV1`

- Method: `GET`
- Path: `/api/youku/get-user-detail/v1`
- Summary: User Profile
- Description: Get YOUKU user Profile data, including user ID, username, and avatar, for analyzing creator influence and audience size, monitoring account growth and verification status, and fetching basic user info for social crm.
- Tags: `YOUKU`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | TOKEN |
| `uid` | `query` | yes | `string` | n/a | The unique identifier for the user. |

### Request body

No request body.

### Responses

- `200`: OK
