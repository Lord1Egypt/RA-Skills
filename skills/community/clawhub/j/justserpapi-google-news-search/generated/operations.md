# Google SERP News Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `news/search`.

## `newsSearch`

- Method: `GET`
- Path: `/api/v1/google/news/search`
- Summary: Search
- Description: Get Google news Search data, including headlines and source metadata, for media monitoring and news aggregation.
- Tags: `Google News`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for Google News (e.g., 'artificial intelligence', 'climate change'). |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `topic_token` | `query` | no | `string` | n/a | The Google News topic token to retrieve results for a specific category (e.g., 'World', 'Technology'). Obtained from previous responses. |
| `publication_token` | `query` | no | `string` | n/a | The Google News publication token to fetch results from a specific source (e.g., 'CNN', 'BBC'). Obtained from previous responses. |
| `section_token` | `query` | no | `string` | n/a | The Google News section token to access a specific subsection within a topic or publication. |
| `so` | `query` | no | `string` | n/a | Sorting order for news results. Supported values: '0' (Relevance, default), '1' (Date). Only works with 'story_token'. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
