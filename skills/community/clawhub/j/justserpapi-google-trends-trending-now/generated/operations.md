# Google SERP Trends Trending Now operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `trends/trending-now`.

## `TrendsTrendingNow`

- Method: `GET`
- Path: `/api/v1/google/trends/trending-now`
- Summary: Trending Now
- Description: Get Google trends Trending Now data, including latest trending topics, region and time-window filters, and volume indicators, for breaking-trend monitoring and editorial planning.
- Tags: `Google Trends`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `geo` | `query` | yes | `string` | n/a | The geographic location code to retrieve real-time trends for (e.g., 'US' for United States). Default is 'US'. |
| `hours` | `query` | no | `string` | n/a | Time window for trending topics. Supported values: '4' (past 4 hours), '24' (past 24 hours), '48' (past 48 hours), '168' (past 7 days). |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en'). |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
