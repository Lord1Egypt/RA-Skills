# Beike operations

Generated from JustOneAPI OpenAPI for platform key `beike`.

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
