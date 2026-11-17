# go-zulip: setup and reference

This module is unofficial and not affiliated with Zulip.

## Requirements

- Go 1.26.11 or newer, per `go.mod`.
- A Zulip server API URL, account or bot email address and API key, exported as `ZULIP_SERVER`, `ZULIP_EMAIL` and `ZULIP_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-zulip
```

## Server and auth

Use `https://your-organization.zulipchat.com/api/v1` for Zulip Cloud or your self-hosted server's HTTPS origin followed by `/api/v1`. HTTP Basic auth uses email as username and API key as password. Attach `req.SetBasicAuth(email, apiKey)` through `zulip.WithRequestEditorFn`; the client does not read environment variables or attach credentials itself.

## Client

- `zulip.NewClientWithResponses(server, opts...)` creates a client with parsed responses.
- `zulip.WithRequestEditorFn` attaches credentials or other request headers.
- `zulip.WithHTTPClient` accepts a configured HTTP client, including timeouts.
- `zulip.WithBaseURL` overrides the server URL.
- Each operation has a raw client method, a `...WithResponse` parsed method and a request constructor. Body operations also expose a raw-body variant taking an `io.Reader` and content type.

## Main operations

The base URL supplies `/api/v1`; paths below are relative to it. The generated source lists every operation.

| Method | Endpoint |
| --- | --- |
| `GetOwnUserWithResponse` | `GET /users/me` |
| `GetUsersWithResponse` | `GET /users` |
| `GetMessagesWithResponse` | `GET /messages` |
| `SendMessageWithFormdataBodyWithResponse` | `POST /messages` |
| `GetStreamsWithResponse` | `GET /streams` |
| `GetSubscriptionsWithResponse` | `GET /users/me/subscriptions` |
| `GetEventsWithResponse` | `GET /events` |

## Request encoding

Many POST and PATCH operations accept `application/x-www-form-urlencoded`. Use the generated form method and request body type when available. For a raw-body call, pass the correct content type and encode array or object values as specified by the operation. Query parameters such as message `narrow` can also contain JSON inside a string. Do not substitute a JSON body for a form body.

The generated client uses a custom template to serialize composite form values as JSON and honor fields marked `application/json`, including quoted string values. Default query serialization handles the spec's JSON query declarations. For union fields, populate the wrapper with its generated `From...` method; a zero wrapper does not identify a union member.

The three multipart operations, `UploadFile`, `UploadAvatar` and `UploadCustomEmoji`, expose raw-body methods. Build the body with `mime/multipart.Writer`, close the writer to finish the body and pass its `FormDataContentType()` to the corresponding `...WithBodyWithResponse` method. The content type must include the writer's boundary; the generated multipart model does not encode a multipart body automatically.

## Responses

`JSON200` holds the decoded success response when the response content type and status match. `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the raw response. Check the status and decoded field before use; the Go error return alone does not report all API errors. Schema fields can be pointers or union wrappers, so read the generated type before accessing them. Number fields map to `float64`.

## Message history and events

`GetMessagesWithResponse` uses an anchor plus `num_before` and `num_after`, with optional narrowing. Advance the anchor using returned message IDs and honor the response's `found_oldest` and `found_newest` markers. There is no automatic page iterator.

The events API uses REST long polling and queue IDs. Create a queue with the registration endpoint, then request events using its queue ID and the last event ID. Use the registration response's `event_queue_longpoll_timeout_seconds` when setting the polling HTTP timeout. This module does not manage queue lifetimes, polling loops or reconnection automatically.

## Errors and rate limits

Inspect unsuccessful HTTP statuses and Zulip's decoded error fields before deciding whether to retry. Back off on HTTP 429; the generated client does not implement retry or rate-limit handling. Do not blindly retry message creation or other mutations.

## Provider integration terms

The spec restricts server-provided GIPHY, Tenor and KLIPY API keys to Zulip clients. Do not reuse them in unrelated applications. Read each provider's terms before enabling the corresponding integration.
