# Weibo TV Video Details operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `tv-component`.

## `tvComponentV1`

- Method: `GET`
- Path: `/api/weibo/tv-component/v1`
- Summary: TV Video Details
- Description: Get Weibo tV Video Details data, including media URLs, author details, and engagement counts, for video research, archiving, and performance analysis.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `oid` | `query` | yes | `string` | n/a | Weibo video/object ID. |

### Request body

No request body.

### Responses

- `200`: OK
