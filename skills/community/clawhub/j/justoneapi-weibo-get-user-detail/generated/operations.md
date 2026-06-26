# Weibo User Profile operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-user-detail`.

## `getUserProfileV3`

- Method: `GET`
- Path: `/api/weibo/get-user-detail/v3`
- Summary: User Profile
- Description: Get Weibo user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |

### Request body

No request body.

### Responses

- `200`: OK
