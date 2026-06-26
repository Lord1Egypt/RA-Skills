# WeChat Official Accounts Article Comments operations

Generated from JustOneAPI OpenAPI for platform key `weixin`.

Endpoint group: `get-article-comment`.

## `getArticleComment`

- Method: `GET`
- Path: `/api/weixin/get-article-comment/v1`
- Summary: Article Comments
- Description: Get WeChat Official Accounts article Comments data, including commenter details, comment text, and timestamps, for feedback analysis.
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
