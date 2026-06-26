# Beike Resale Housing List operations

Generated from JustOneAPI OpenAPI for platform key `beike`.

Endpoint group: `get-ershoufang-list`.

## `getErshoufangListV1`

- Method: `GET`
- Path: `/api/beike/get-ershoufang-list/v1`
- Summary: Resale Housing List
- Description: Get Beike resale Housing List data, including - Supports filtering by city/region, price range, and layout, for building search result pages for property portals and aggregating market data for regional housing trends.
- Tags: `Beike`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `cityId` | `query` | yes | `string` | n/a | The ID of the city (e.g., '110000' for Beijing). |
| `condition` | `query` | no | `string` | n/a | Filter conditions (e.g., region, price range, layout). |
| `offset` | `query` | no | `integer` | `0` | Pagination offset, starting from 0 (e.g., 0, 20, 40...). |

### Request body

No request body.

### Responses

- `200`: OK
