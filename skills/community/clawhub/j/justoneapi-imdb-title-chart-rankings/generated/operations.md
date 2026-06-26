# IMDb Chart Rankings operations

Generated from JustOneAPI OpenAPI for platform key `imdb`.

Endpoint group: `title-chart-rankings`.

## `titleChartRankings`

- Method: `GET`
- Path: `/api/imdb/title-chart-rankings/v1`
- Summary: Chart Rankings
- Description: Get IMDb title Chart Rankings data, including positions in lists such as Top 250 and related charts, for ranking monitoring and title benchmarking.
- Tags: `IMDb`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User's authentication token. |
| `rankingsChartType` | `query` | yes | `string` | n/a | Type of rankings chart to retrieve.

Available Values:
- `TOP_250`: Top 250 Movies
- `TOP_250_TV`: Top 250 TV Shows |
| enum | values | no | n/a | n/a | `TOP_250`, `TOP_250_TV` |
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
