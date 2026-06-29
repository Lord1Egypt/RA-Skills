# Google SERP Trends Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `trends/search`.

## `TrendsSearch`

- Method: `GET`
- Path: `/api/v1/google/trends/search`
- Summary: Search
- Description: Get Google trends Search data, including interest over time, geo breakdowns, and related queries, for demand analysis and seasonal trend monitoring.
- Tags: `Google Trends`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search term or topic ID to analyze in Google Trends (e.g., 'iPhone', '/m/027lnzs' for Bitcoin). You can provide up to 5 terms separated by commas for comparisons. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `geo` | `query` | no | `string` | n/a | The geographic location code to filter trends (e.g., 'US', 'GB'). Omit for worldwide trends. See <a href="/reference/google-trends-locations">Google Trends Locations</a>. |
| `region` | `query` | no | `string` | n/a | Refines results for region charts. Supported values: 'COUNTRY', 'REGION', 'DMA', 'CITY'. |
| `data_type` | `query` | no | `string` | n/a | The type of trend data to retrieve. Supported values: 'TIMESERIES' (Interest over time), 'GEO_MAP' (Breakdown by region). |
| `tz` | `query` | no | `integer` | n/a | Time zone offset in minutes (e.g., '420' for PDT). Range: -1439 to 1439. |
| `cat` | `query` | no | `string` | n/a | The search category code (e.g., '0' for all categories). |
| `gprop` | `query` | no | `string` | n/a | The Google property to filter trends. Supported values: 'images', 'news', 'froogle' (Shopping), 'youtube'. |
| `date` | `query` | no | `string` | n/a | Date range filter for the search. Supports predefined values (now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m, today 12-m, today 5-y, all) and custom ranges: yyyy-mm-dd yyyy-mm-dd (e.g. 2021-10-15 2022-05-25) or hourly yyyy-mm-ddThh yyyy-mm-ddThh within 1 week (e.g. 2022-05-19T10 2022-05-24T22, based on tz). |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
