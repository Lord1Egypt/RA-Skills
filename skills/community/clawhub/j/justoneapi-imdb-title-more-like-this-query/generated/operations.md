# IMDb Recommendations operations

Generated from JustOneAPI OpenAPI for platform key `imdb`.

Endpoint group: `title-more-like-this-query`.

## `titleMoreLikeThisQuery`

- Method: `GET`
- Path: `/api/imdb/title-more-like-this-query/v1`
- Summary: Recommendations
- Description: Get IMDb title Recommendations data, including related titles and suggestion metadata, for content discovery and recommendation analysis.
- Tags: `IMDb`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User's authentication token. |
| `id` | `query` | yes | `string` | n/a | The unique IMDb ID of the title (e.g., tt12037194). |
| `languageCountry` | `query` | no | `string` | `en_US` | Language and country preferences.

Available Values:
- `en_US`: English (US)
- `fr_CA`: French (Canada)
- `fr_FR`: French (France)
- `de_DE`: German (Germany)
- `hi_IN`: Hindi (India)
- `it_IT`: Italian (Italy)
- `pt_BR`: Portuguese (Brazil)
- `es_ES`: Spanish (Spain)
- `es_US`: Spanish (US)
- `es_MX`: Spanish (Mexico) |
| enum | values | no | n/a | n/a | `en_US`, `fr_CA`, `fr_FR`, `de_DE`, `hi_IN`, `it_IT`, `pt_BR`, `es_ES`, `es_US`, `es_MX` |

### Request body

No request body.

### Responses

- `200`: OK
