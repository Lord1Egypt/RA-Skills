# Google SERP Scholar Cite Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `scholar/cite/search`.

## `ScholarCiteSearch`

- Method: `GET`
- Path: `/api/v1/google/scholar/cite/search`
- Summary: Citations
- Description: Get Google scholar Citations data, including export links, for bibliography automation and citation workflows.
- Tags: `Google Scholar`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The unique ID of a Google Scholar search result to retrieve citation formats for. Found in the 'id' field of previous Scholar Search responses. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
