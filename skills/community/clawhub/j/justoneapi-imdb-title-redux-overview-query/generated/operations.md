# IMDb Redux Overview operations

Generated from JustOneAPI OpenAPI for platform key `imdb`.

Endpoint group: `title-redux-overview-query`.

## `titleReduxOverviewQuery`

- Method: `GET`
- Path: `/api/imdb/title-redux-overview-query/v1`
- Summary: Redux Overview
- Description: Get IMDb title Redux Overview data, including key summary fields and linked metadata, for get a concise summary and overview of a movie or TV show's key attributes.
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
