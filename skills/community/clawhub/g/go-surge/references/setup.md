# go-surge: setup and reference

This module is unofficial and not affiliated with Surge.

## Requirements

- Go 1.26.11 or newer, per `go.mod`.
- A Surge API token exported as `SURGE_API_KEY`.
- An account ID for account-scoped operations.

## Install

```bash
go get github.com/psyb0t/go-surge
```

## Base URL and auth

Use `https://api.surge.app`. The spec declares HTTP bearer authentication with bearer format `Surge API token`.

Attach a request editor through `surge.WithRequestEditorFn` and set `req.Header.Set("Authorization", "Bearer "+token)`. The full example in the root README is compiled by `example_test.go`.

## Client

- `surge.NewClientWithResponses(server, opts...)` returns a parsed client. Options include `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`.
- `Client.X` returns a raw `*http.Response`; the caller closes its body. `ClientWithResponses.XWithResponse` reads, closes and decodes the response. `NewXRequest` builds a request without sending it.
- Body operations also expose `XWithBodyWithResponse` for raw request bodies.

## Operations

| Methods, each with a WithResponse suffix | Endpoint |
|---|---|
| `ListAccounts`, `CreateAccount` | `GET`, `POST /accounts` |
| `GetAccount`, `UpdateAccount`, `ArchiveAccount` | `GET`, `PATCH`, `DELETE /accounts/{id}` |
| `CheckAccountStatus` | `GET /accounts/{account_id}/status` |
| `CreateAudience` | `POST /accounts/{account_id}/audiences` |
| `ListAudienceContacts`, `AddContactToAudience` | `GET`, `POST /audiences/{audience_id}/contacts` |
| `SendBlast` | `POST /accounts/{account_id}/blasts` |
| `ResendBrandVerificationMessage` | `POST /accounts/{account_id}/brand_verification_messages` |
| `ListCampaigns`, `CreateCampaign` | `GET`, `POST /accounts/{account_id}/campaigns` |
| `GetCampaign`, `UpdateCampaign` | `GET`, `PATCH /campaigns/{id}` |
| `ListTollFreeCampaigns`, `CreateTollFreeCampaign` | `GET`, `POST /accounts/{account_id}/toll_free_campaigns` |
| `GetTollFreeCampaign`, `UpdateTollFreeCampaign` | `GET`, `PATCH /toll_free_campaigns/{campaign_id}` |
| `ListContacts`, `CreateContact` | `GET`, `POST /accounts/{account_id}/contacts` |
| `GetContact`, `UpdateContact` | `GET`, `PATCH /contacts/{id}` |
| `ListMessages`, `CreateMessage` | `GET`, `POST /accounts/{account_id}/messages` |
| `GetMessage` | `GET /messages/{id}` |
| `GetAttachmentFile` | `GET /attachments/{attachment_id}/file` |
| `ListAvailablePhoneNumbers` | `GET /accounts/{account_id}/available_phone_numbers` |
| `ListPhoneNumbers`, `PurchasePhoneNumber` | `GET`, `POST /accounts/{account_id}/phone_numbers` |
| `GetPhoneNumber`, `UpdatePhoneNumber`, `ReleasePhoneNumber` | `GET`, `PATCH`, `DELETE /phone_numbers/{id}` |
| `ListRecordings` | `GET /accounts/{account_id}/recordings` |
| `GetRecording`, `DeleteRecording` | `GET`, `DELETE /recordings/{id}` |
| `GetRecordingFile` | `GET /recordings/{recording_id}/file` |
| `ListUsers`, `CreateUser` | `GET`, `POST /accounts/{account_id}/users` |
| `GetUser`, `UpdateUser`, `DeleteUser` | `GET`, `PATCH`, `DELETE /users/{id}` |
| `CreateToken` | `POST /users/{user_id}/tokens` |
| `CreateVerification` | `POST /accounts/{account_id}/verifications` |
| `CheckVerification` | `POST /verifications/{id}/checks` |

## Messages and unions

`CreateMessageJSONRequestBody` aliases `MessageParams`. Its `MessageParams0` branch uses `Conversation`; its `MessageParams1` branch requires `To` and optionally accepts `From`. Initialize the union with `FromMessageParams0` or `FromMessageParams1`, checking the returned error. Include `Body` or `Attachments`. Do not combine conversation routing with direct routing.

Campaign request bodies also contain unions. Read their generated `As...`, `From...` and `Merge...` helpers rather than assuming the wrapper exposes branch fields directly.

Delivery is asynchronous. A 201 response means the message was created and enqueued. Delivery status comes later. The client adds no retries, rate limiting or polling.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200`, `JSON201` | Decoded success bodies, nil when absent |
| `JSONDefault` | Default error body for most operations |
| `Body`, `HTTPResponse`, `StatusCode()`, `Status()` | Raw response and status |

Verification methods have additional typed status fields, such as 409, 422 and 429. File endpoints can return redirects or raw bytes instead of JSON. Inspect their status and response fields.

Number fields map to `float64`. Many optional or nullable fields are pointers. Generated enum types expose `Valid()`, but the client does not validate every request field or enforce cross-field constraints.

## Pagination and rate limits

List parameters expose `After` and `Before` where the spec declares them. List bodies expose `Data` and `Pagination`. Send `NextCursor` as `After`, or `PreviousCursor` as `Before`, without modifying it. Stop when the relevant cursor is nil. There is no automatic page iterator.

Inspect 429 responses and use a bounded backoff policy appropriate for the caller. Do not blindly retry message creation or other writes, since retries can duplicate effects.

## Webhook models

All component schemas are generated, including `MessageSentEvent`, `MessageReceivedEvent`, `MessageDeliveredEvent`, `MessageFailedEvent` and other event payloads. This is REST plus data models, with no WebSocket package, event dispatcher or webhook signature verification.
