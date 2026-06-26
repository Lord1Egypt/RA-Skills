# Beike Community List operations

Generated from JustOneAPI OpenAPI for platform key `beike`.

Endpoint group: `community/list`.

## `communityListV1`

- Method: `GET`
- Path: `/api/beike/community/list/v1`
- Summary: Community List
- Description: Get Beike community List data, including - Community name and unique ID and Average listing price and historical price trends, for identifying popular residential areas in a city and comparing average housing prices across different communities.
- Tags: `Beike`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User authentication token. |
| `cityId` | `query` | yes | `string` | n/a | The ID of the city (e.g., '110000' for Beijing). |
| `condition` | `query` | no | `string` | n/a | Filter conditions for communities. |
| `limitOffset` | `query` | no | `integer` | `0` | Pagination offset, starting from 0 (e.g., 0, 20, 40...). |

### Request body

No request body.

### Responses

- `200`: OK
