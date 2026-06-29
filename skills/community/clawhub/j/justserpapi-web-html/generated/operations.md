# Web Crawling Html operations

Generated from Just Serp API OpenAPI for group key `web`.

Endpoint group: `html`.

## `html`

- Method: `GET`
- Path: `/api/v1/web/html`
- Summary: Crawl Webpage (HTML)
- Description: Get webpage crawl data, including returns full raw HTML content, fast and cost-efficient, and optimized for static page crawling, for scraping, metadata extraction, and page structure analysis.
- Tags: `Web Crawling`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | yes | `string` | n/a | The full URL of the webpage to crawl (e.g., 'https://www.example.com'). |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
