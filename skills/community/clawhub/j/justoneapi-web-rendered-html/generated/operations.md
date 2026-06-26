# Web Page Rendered HTML Content operations

Generated from JustOneAPI OpenAPI for platform key `web`.

Endpoint group: `rendered-html`.

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
