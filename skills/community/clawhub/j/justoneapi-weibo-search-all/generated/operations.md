# Weibo Keyword Search operations

Generated from JustOneAPI OpenAPI for platform key `weibo`.

Endpoint group: `search-all`.

## `searchAllV2`

- Method: `GET`
- Path: `/api/weibo/search-all/v2`
- Summary: Keyword Search
- Description: Get Weibo keyword Search data, including authors, publish times, and engagement signals, for trend monitoring.
- Tags: `Weibo`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | API access token. |
| `q` | `query` | yes | `string` | n/a | Search Keywords. |
| `startDay` | `query` | yes | `string` | n/a | Start Day (yyyy-MM-dd). |
| `startHour` | `query` | yes | `integer` | n/a | Start Hour (0-23). |
| `endDay` | `query` | yes | `string` | n/a | End Day (yyyy-MM-dd). |
| `endHour` | `query` | yes | `integer` | n/a | End Hour (0-23). |
| `hotSort` | `query` | no | `boolean` | `false` | Hot sort, true for hot sort, false for time sort. Default is false. |
| `contains` | `query` | no | `string` | `ALL` | Contains filter for the result set.

Available Values:
- `ALL`: All
- `PICTURE`: Has Picture
- `VIDEO`: Has Video
- `MUSIC`: Has Music
- `LINK`: Has Link |
| enum | values | no | n/a | n/a | `ALL`, `PICTURE`, `VIDEO`, `MUSIC`, `LINK` |
| `page` | `query` | no | `integer` | `1` | Page number, starting with 1. |

### Request body

No request body.

### Responses

- `200`: OK
