# Instagram Reels Search operations

Generated from JustOneAPI OpenAPI for platform key `instagram`.

Endpoint group: `search-reels`.

## `searchReelsV1`

- Method: `GET`
- Path: `/api/instagram/search-reels/v1`
- Summary: Reels Search
- Description: Get Instagram reels Search data, including post ID, caption, and author profile, for tracking trends and viral content via specific keywords or hashtags and discovering high-engagement reels within a particular niche.
- Tags: `Instagram`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API service. |
| `keyword` | `query` | yes | `string` | n/a | The search keyword or hashtag to filter Reels. |
| `paginationToken` | `query` | no | `string` | n/a | Token used for retrieving the next page of results. |

### Request body

No request body.

### Responses

- `200`: OK
