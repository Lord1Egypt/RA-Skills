# Toutiao User Profile operations

Generated from JustOneAPI OpenAPI for platform key `toutiao`.

Endpoint group: `get-user-detail`.

## `getToutiaoUserDetailV1`

- Method: `GET`
- Path: `/api/toutiao/get-user-detail/v1`
- Summary: User Profile
- Description: Get Toutiao user Profile data, including user ID, nickname, and avatar, for influencer profiling and audience analysis and monitoring creator performance and growth.
- Tags: `Toutiao`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token required to access the API. |
| `userId` | `query` | yes | `string` | n/a | The unique identifier of the Toutiao user. |

### Request body

No request body.

### Responses

- `200`: OK
