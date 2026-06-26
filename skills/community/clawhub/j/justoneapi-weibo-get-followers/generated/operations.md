# Weibo User Followers operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-followers`.

## `getFollowersV1`

- Method: `GET`
- Path: `/api/weibo/get-followers/v1`
- Summary: User Followers
- Description: Get Weibo user Followers data, including profile metadata and verification signals, for network analysis and creator research.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `uid` | `query` | yes | `string` | n/a | Weibo User ID (UID). |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK
