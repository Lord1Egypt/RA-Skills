# Kuaishou User Profile operations

Generated from JustOneAPI OpenAPI for platform key `kuaishou`.

Endpoint group: `get-user-detail`.

## `getUserProfileV1`

- Method: `GET`
- Path: `/api/kuaishou/get-user-detail/v1`
- Summary: User Profile
- Description: Get Kuaishou user Profile data, including account metadata, audience metrics, and verification-related fields, for creator research and building creator profiles and monitoring audience growth and account status.
- Tags: `Kuaishou`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `userId` | `query` | yes | `string` | n/a | The unique user ID on Kuaishou. |

### Request body

No request body.

### Responses

- `200`: OK
