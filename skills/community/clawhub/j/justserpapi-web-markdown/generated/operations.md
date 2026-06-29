# Web Crawling Markdown operations

Generated from Just Serp API OpenAPI for group key `web`.

Endpoint group: `markdown`.

## `markdown`

- Method: `GET`
- Path: `/api/v1/web/markdown`
- Summary: Crawl Webpage (Markdown)
- Description: Get webpage crawl data, including removing boilerplate, for readable extraction, documentation workflows, and LLM input.
- Tags: `Web Crawling`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | yes | `string` | n/a | The full URL of the webpage to crawl and convert to Markdown (e.g., 'https://www.example.com'). |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
