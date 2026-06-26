# Weibo User Fans operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `get-fans`.

## `getFansV1`

- Method: `GET`
- Path: `/api/weibo/get-fans/v1`
- Summary: User Fans
- Description: Get Weibo user Fans data, including profile metadata and verification signals, for audience analysis and influencer research.
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
