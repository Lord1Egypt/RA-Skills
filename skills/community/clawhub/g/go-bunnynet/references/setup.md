# go-bunnynet: setup and reference

This module is unofficial and not affiliated with Bunny.net.

## Requirements and install

Use Go 1.26.10 or newer and an account API key exported as `BUNNYNET_API_KEY`.

```bash
go get github.com/psyb0t/go-bunnynet
```

## Client and auth

The base URL is `https://api.bunny.net`. Construct `bunnynet.NewClientWithResponses(server, opts...)`. Options include `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`.

Set `req.Header.Set("AccessKey", key)` in the request editor. Some operations also accept the spec's alternative `bearer` scheme: set the full `Authorization` header value through `req.Header.Set("Authorization", token)`. The client adds no prefixes. Check each operation's security requirements before using the alternative.

The working auth example is in the README and `example_test.go`.

## Main operations

| Method | Endpoint |
| --- | --- |
| `PullZonePublicIndexAllWithResponse` | `GET /pullzone` |
| `PullZonePublicIndexWithResponse` | `GET /pullzone/{id}` |
| `PullZonePublicAddWithResponse` | `POST /pullzone` |
| `PullZonePublicUpdatePullZoneWithResponse` | `POST /pullzone/{id}` |
| `PullZonePublicDeleteWithResponse` | `DELETE /pullzone/{id}` |
| `PurgePublicIndexPostWithResponse` | `POST /purge` |
| `DnsZonePublicIndexWithResponse` | `GET /dnszone` |
| `StorageZonePublicIndexAllWithResponse` | `GET /storagezone` |
| `StatisticsPublicGetStatisticsWithResponse` | `GET /statistics` |
| `CountriesPublicGetCountryListWithResponse` | `GET /country` |

All core operations are generated, including video library configuration, load balancers, API key listing and billing. The spec excludes storage file transfers and the separate Stream API. Request types include `PullZoneAddModel` and `PullZoneSettingsModel`.

## Responses

Raw methods return `*http.Response`; callers must close the body. `XWithResponse` methods read and close it, retaining `Body`, `HTTPResponse`, `StatusCode()`, `Status()` and typed fields such as `JSON200`. Request constructors are named `NewXRequest`. Body operations also offer raw reader variants.

Check errors before the response, and nil-check optional fields. HTTP errors are statuses, not necessarily Go errors. Creation responses can have no schema, so check status and raw body. Unformatted numbers map to `float64`.

## Pagination and rate limits

Pagination is endpoint-specific. Pull-zone listing declares an array but describes a paginated object for `page > 0`. The typed parser cannot decode that object. Use the raw method and decode it yourself when setting `Page`; otherwise leave it unset. DNS and other endpoints have their own parameter and response types.

The client has no automatic retries or page iteration. Check 429 responses, follow server retry guidance, and avoid replaying mutations without checking the operation's semantics.
