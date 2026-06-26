# Taobao and Tmall Product Reviews operations

Generated from JustOneAPI OpenAPI for platform key `taobao`.

Endpoint group: `get-item-comment`.

## `getItemCommentV3`

- Method: `GET`
- Path: `/api/taobao/get-item-comment/v3`
- Summary: Product Reviews
- Description: Get Taobao and Tmall product Reviews data, including ratings, timestamps, and reviewer signals, for feedback analysis and product research.
- Tags: `Taobao and Tmall`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for this API service. |
| `itemId` | `query` | yes | `string` | n/a | AUnique product identifier on Taobao/Tmall (item ID). |
| `orderType` | `query` | no | `string` | `feedbackdate` | Sort order for the result set.

Available Values:
- `feedbackdate`: Sort by feedback date
- `general`: General sorting |
| enum | values | no | n/a | n/a | `feedbackdate`, `general` |
| `page` | `query` | no | `integer` | `1` | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
