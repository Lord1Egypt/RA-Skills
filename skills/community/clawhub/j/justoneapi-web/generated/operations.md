# Web Page operations

Generated from JustOneAPI OpenAPI for platform key `web`.

## `htmlV1`

- Method: `GET`
- Path: `/api/web/html/v1`
- Summary: HTML Content
- Description: Get the HTML content of a web page.
- Tags: `Web Page`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `url` | `query` | yes | `string` | n/a | The URL of the web page to fetch. |

### Request body

No request body.

### Responses

- `200`: OK

## `markdownV1`

- Method: `GET`
- Path: `/api/web/markdown/v1`
- Summary: Markdown Content
- Description: Get the Markdown content of a web page.
- Tags: `Web Page`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `url` | `query` | yes | `string` | n/a | The URL of the web page to fetch. |

### Request body

No request body.

### Responses

- `200`: OK

## `renderedHtmlV1`

- Method: `GET`
- Path: `/api/web/rendered-html/v1`
- Summary: Rendered HTML Content
- Description: Get the Rendered HTML content of a web page.
- Tags: `Web Page`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Authentication token for this API service. |
| `url` | `query` | yes | `string` | n/a | The URL of the web page to fetch. |

### Request body

No request body.

### Responses

- `200`: OK
