# Google SERP Scholar Profiles operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `scholar/profiles`.

## `ScholarProfiles`

- Method: `GET`
- Path: `/api/v1/google/scholar/profiles`
- Summary: Scholar Profiles
- Description: Get Google scholar Profiles data, including profile search results, affiliation and citation counts, and pagination tokens, for researcher discovery and academic directory building.
- Tags: `Google`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `mauthors` | `query` | yes | `string` | n/a | The search query for author profiles (e.g., 'John Smith', 'Harvard University'). |
| `after_author` | `query` | no | `string` | n/a | Token used to retrieve the next page of author profiles. |
| `before_author` | `query` | no | `string` | n/a | Token used to retrieve the previous page of author profiles. |

### Request body

No request body.

### Responses

- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
- `default`: default response
