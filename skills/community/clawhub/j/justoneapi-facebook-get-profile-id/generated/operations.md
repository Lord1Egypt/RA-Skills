# Facebook Get Profile ID operations

Generated from JustOneAPI OpenAPI for platform key `facebook`.

Endpoint group: `get-profile-id`.

## `getProfileIdV1`

- Method: `GET`
- Path: `/api/facebook/get-profile-id/v1`
- Summary: Get Profile ID
- Description: Retrieve the unique Facebook profile ID from a given profile URL.
- Tags: `Facebook`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `token` | `query` | yes | `string` | n/a | User security token for API access authentication. |
| `url` | `query` | yes | `string` | n/a | The path part of the Facebook profile URL. Do not include `https://www.facebook.com`. Example: `/people/To-Bite/pfbid021XLeDjjZjsoWse1H43VEgb3i1uCLTpBvXSvrnL2n118YPtMF5AZkBrZobhWWdHTHl/` |

### Request body

No request body.

### Responses

- `200`: OK
