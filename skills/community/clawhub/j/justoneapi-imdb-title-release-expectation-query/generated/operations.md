# IMDb Release Expectation operations

Generated from JustOneAPI OpenAPI for platform key `imdb`.

Endpoint group: `title-release-expectation-query`.

## `titleReleaseExpectationQuery`

- Method: `GET`
- Path: `/api/imdb/title-release-expectation-query/v1`
- Summary: Release Expectation
- Description: Get IMDb title Release Expectation data, including production status, release dates, and anticipation signals, for release monitoring and title research.
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
| `acceptCache` | `query` | no | `boolean` | `false` | Whether to accept cached data. |

### Request body

No request body.

### Responses

- `200`: OK
