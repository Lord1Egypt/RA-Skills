# WeChat Official Accounts User Published Posts operations

Generated from JustOneAPI OpenAPI for platform key `weixin`.

Endpoint group: `get-user-post`.

## `getUserPost`

- Method: `GET`
- Path: `/api/weixin/get-user-post/v1`
- Summary: User Published Posts
- Description: Get WeChat Official Accounts user Published Posts data, including titles, publish times, and summaries, for account monitoring.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `wxid` | `query` | yes | `string` | n/a | The ID of the Weixin Official Account (e.g., 'rmrbwx'). |

### Request body

No request body.

### Responses

- `200`: OK
