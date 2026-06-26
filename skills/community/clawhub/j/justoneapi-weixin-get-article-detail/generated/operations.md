# WeChat Official Accounts Article Details operations

Generated from JustOneAPI OpenAPI for platform key `weixin`.

Endpoint group: `get-article-detail`.

## `getWeixinArticleDetailV1`

- Method: `GET`
- Path: `/api/weixin/get-article-detail/v1`
- Summary: Article Details
- Description: Get WeChat Official Accounts article Details data, including body content, for article archiving, research, and content analysis.
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
