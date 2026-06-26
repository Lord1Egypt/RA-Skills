# IMDb Keyword Search operations

Generated from JustOneAPI OpenAPI for platform key `imdb`.

Endpoint group: `main-search-query`.

## `mainSearchQuery`

- Method: `GET`
- Path: `/api/imdb/main-search-query/v1`
- Summary: Keyword Search
- Description: Get IMDb keyword Search data, including matched results, metadata, and ranking signals, for entity discovery and entertainment research.
- Tags: `IMDb`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User's authentication token. |
| `searchTerm` | `query` | yes | `string` | n/a | The term to search for (e.g., 'fire'). |
| `type` | `query` | no | `string` | `Top` | Category of results to include in search.

Available Values:
- `Top`: Top Results
- `Movies`: Movies
- `Shows`: TV Shows
- `People`: People
- `Interests`: Interests
- `Episodes`: Episodes
- `Podcast`: Podcasts
- `Video_games`: Video Games |
| enum | values | no | n/a | n/a | `Top`, `Movies`, `Shows`, `People`, `Interests`, `Episodes`, `Podcast`, `Video_games` |
| `limit` | `query` | no | `integer` | `25` | Maximum number of results to return (1-300). |
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
