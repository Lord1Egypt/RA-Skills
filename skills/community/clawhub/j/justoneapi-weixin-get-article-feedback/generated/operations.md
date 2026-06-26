# WeChat Official Accounts Article Engagement Metrics operations

Generated from JustOneAPI OpenAPI for platform key `weixin`.

Endpoint group: `get-article-feedback`.

## `getArticleFeedback`

- Method: `GET`
- Path: `/api/weixin/get-article-feedback/v1`
- Summary: Article Engagement Metrics
- Description: Get WeChat Official Accounts article Engagement Metrics data, including like, share, and comment metrics, for article performance tracking and benchmarking.
- Tags: `WeChat Official Accounts`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `articleUrl` | `query` | yes | `string` | n/a | The URL of the Weixin article. |

### Request body

No request body.

### Responses

- `200`: OK
