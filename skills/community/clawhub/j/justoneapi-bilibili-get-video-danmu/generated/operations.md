# Bilibili Video Danmaku operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-video-danmu`.

## `getVideoDanmuV2`

- Method: `GET`
- Path: `/api/bilibili/get-video-danmu/v2`
- Summary: Video Danmaku
- Description: Get Bilibili video Danmaku data, including timeline positions and comment text, for audience reaction analysis and subtitle-style comment review.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `aid` | `query` | yes | `string` | n/a | Bilibili Archive ID (AID). |
| `cid` | `query` | yes | `string` | n/a | Bilibili Chat ID (CID). |
| `page` | `query` | no | `string` | n/a | Page number for pagination. |

### Request body

No request body.

### Responses

- `200`: OK
