# go-calcom: setup and reference

This module is unofficial and not affiliated with Cal.com.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A Cal.com API key or supported access token, exported as `CALCOM_API_KEY`. Endpoint access depends on the account plan and permissions.

## Install

```bash
go get github.com/psyb0t/go-calcom
```

## Base URL

The spec declares no server URL. Pass `https://api.cal.com` to `calcom.NewClientWithResponses`. The [profile docs](https://cal.com/docs/api-reference/v2/me/get-my-profile) show `https://api.cal.com/v2/me`. Generated paths already contain `/v2`, so use the host without that suffix. Pass another host for a configured deployment or local test server.

## Auth and API versions

Use a request editor with `req.Header.Set("Authorization", "Bearer "+token)`. The spec has no `securitySchemes`; it describes credentials as header parameters. Required `Authorization` fields in params must also be populated. Some endpoints accept the deprecated Platform `x-cal-client-id` and `x-cal-secret-key` headers. See the [provider introduction](https://cal.com/docs/api-reference/v2/introduction).

Many operations require `cal-api-version`, exposed as `CalApiVersion` in generated params. Set it explicitly; the generator does not apply schema defaults. Bookings use `2024-08-13`, event types `2024-06-14`, schedules `2024-06-11`, and available slots `2024-09-04`. These values identify endpoint versions. Read each generated parameter comment for the required version. `/v2/me` does not require this header in the spec.

## Client

- `calcom.NewClientWithResponses(server, opts...)` creates a client with parsed response methods.
- Options include `calcom.WithRequestEditorFn`, `calcom.WithHTTPClient` and `calcom.WithBaseURL`.
- Each operation has a raw `Client.X`, parsed `ClientWithResponses.XWithResponse`, and request-only `NewXRequest` form.
- Body operations also support `XWithBodyWithResponse` with a content type and `io.Reader`.

## Main operations

The client generates every operation in the supplied spec. Common read methods:

| Method | Endpoint |
| --- | --- |
| `MeControllerGetMeWithResponse` | `GET /v2/me` |
| `BookingsController20240813GetBookingsWithResponse` | `GET /v2/bookings` |
| `EventTypesController20240614GetEventTypesWithResponse` | `GET /v2/event-types` |
| `SlotsController20240904GetAvailableSlotsWithResponse` | `GET /v2/slots` |
| `SchedulesController20240611GetSchedulesWithResponse` | `GET /v2/schedules` |
| `CalendarsControllerGetCalendarsWithResponse` | `GET /v2/calendars` |
| `WebhooksControllerGetWebhooksWithResponse` | `GET /v2/webhooks` |

Bookings also have create, reschedule, cancel, confirmation, reassignment and other operations. Event types, schedules, teams and webhooks expose management operations. Read generated signatures for required path params, headers and bodies.

The slots endpoint requires UTC ISO 8601 `Start` and `End`. Select the event type by the supported ID or slug and owner fields. Slot responses are generated unions; use their `As...` methods to decode the matching schema.

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200`, `JSON201` and other declared status fields | Parsed body for that status, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Raw response and HTTP status |

Transport and decoding errors use the Go error return. HTTP failures can have a nil Go error, so check status and the expected parsed field. Optional and nullable fields may be pointers. Unformatted number fields are `float64`, including some IDs.

## Pagination

Bookings and webhooks use `Take` and `Skip` params. Booking responses expose `Pagination`, including `HasNextPage`, `ReturnedItems` and `RemainingItems`. Advance `Skip` by the number of returned items and stop when `HasNextPage` is false. Pagination varies across endpoint families; inspect each params and response type.

## Rate limits

Handle HTTP 429 with bounded backoff. The generated client does not automatically retry or pace requests. Avoid retrying booking mutations without checking their result and the endpoint's idempotency behavior.

## Source and license metadata

The source is https://raw.githubusercontent.com/calcom/cal.com/main/docs/api-reference/v2/openapi.json. It is OpenAPI 3.0.0, titled `Cal.diy API v2`, spec version `1.0.0`, with 82 paths and 121 operations. It declares no license or terms URL in its metadata. The downloaded specification is not redistributed in this module.
