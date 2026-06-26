# Beike Resale Housing Details operations

Generated from JustOneAPI OpenAPI for platform key `beike`.

Endpoint group: `ershoufang/detail`.

## `ershoufangDetailV1`

- Method: `GET`
- Path: `/api/beike/ershoufang/detail/v1`
- Summary: Resale Housing Details
- Description: Get Beike resale Housing Details data, including - Pricing (total and unit price), Physical attributes (area, and layout, for displaying a full property profile to users and detailed price comparison between specific listings.
- Tags: `Beike`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `cityId` | `query` | yes | `string` | n/a | The ID of the city (e.g., '110000' for Beijing). |
| `houseCode` | `query` | yes | `string` | n/a | The unique identifier for the property listing. |

### Request body

No request body.

### Responses

- `200`: OK
