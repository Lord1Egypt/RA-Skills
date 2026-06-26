# Bilibili User Profile operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-user-detail`.

## `getUserDetailV2`

- Method: `GET`
- Path: `/api/bilibili/get-user-detail/v2`
- Summary: User Profile
- Description: Get Bilibili user Profile data, including account metadata, audience metrics, and verification-related fields, for analyzing creator's profile, level, and verification status and verifying user identity and social presence on bilibili.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `uid` | `query` | yes | `string` | n/a | Bilibili User ID (UID). |

### Request body

No request body.

### Responses

- `200`: OK
