# IMDb News by Category operations

Generated from JustOneAPI OpenAPI for platform key `imdb`.

Endpoint group: `news-by-category-query`.

## `newsByCategoryQuery`

- Method: `GET`
- Path: `/api/imdb/news-by-category-query/v1`
- Summary: News by Category
- Description: Get IMDb news by Category data, including headlines, summaries, and source metadata, for media monitoring and news research.
- Tags: `IMDb`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User's authentication token. |
| `category` | `query` | yes | `string` | n/a | News category to filter by.

Available Values:
- `TOP`: Top News
- `MOVIE`: Movie News
- `TV`: TV News
- `CELEBRITY`: Celebrity News |
| enum | values | no | n/a | n/a | `TOP`, `MOVIE`, `TV`, `CELEBRITY` |
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
