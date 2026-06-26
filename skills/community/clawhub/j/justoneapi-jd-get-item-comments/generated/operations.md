# JD.com Product Comments operations

Generated from JustOneAPI OpenAPI for platform key `jd`.

Endpoint group: `get-item-comments`.

## `getItemCommentsV1`

- Method: `GET`
- Path: `/api/jd/get-item-comments/v1`
- Summary: Product Comments
- Description: Get JD.com product Comments data, including ratings, timestamps, and reviewer signals, for customer feedback analysis and product research.
- Tags: `JD.com`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | A unique product identifier on JD.com (item ID). |
| `page` | `query` | no | `string` | n/a | Page number for paginated comments. |

### Request body

No request body.

### Responses

- `200`: OK
