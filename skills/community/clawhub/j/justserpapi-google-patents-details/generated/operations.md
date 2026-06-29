# Google SERP Patents Details operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `patents/details`.

## `patentDetails`

- Method: `GET`
- Path: `/api/v1/google/patents/details`
- Summary: Details
- Description: Get Google patent Details data, including abstracts, claims, and legal status, for patent review and IP due diligence.
- Tags: `Google Patent`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `patent_id` | `query` | yes | `string` | n/a | The unique Google Patent ID (e.g., 'US1234567B1'). |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
