# Bilibili Video Captions operations

Generated from JustOneAPI OpenAPI for platform key `bilibili`.

Endpoint group: `get-video-caption`.

## `getVideoCaptionV1`

- Method: `GET`
- Path: `/api/bilibili/get-video-caption/v2`
- Summary: Video Captions
- Description: Get Bilibili video Captions data, including caption data, for transcript extraction and multilingual content analysis.
- Tags: `Bilibili`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | Access token for the API. |
| `bvid` | `query` | yes | `string` | n/a | Bilibili Video ID (BVID). |
| `aid` | `query` | yes | `string` | n/a | Bilibili AID. |
| `cid` | `query` | yes | `string` | n/a | Bilibili CID. |

### Request body

No request body.

### Responses

- `200`: OK
