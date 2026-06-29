# Google SERP Finance Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `finance/search`.

## `financeSearch`

- Method: `GET`
- Path: `/api/v1/google/finance/search`
- Summary: Search
- Description: Get Google finance Search data, including market summaries, company details, and related finance results, for finance monitoring and market research.
- Tags: `Google Finance`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The stock symbol, company name, or index you want to search for on Google Finance (e.g., 'AAPL', 'Tesla', 'S&P 500'). |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
