# go-vectara: setup and reference

This module is unofficial and not affiliated with Vectara.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A Vectara credential with the roles required by each operation. The README example reads `VECTARA_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-vectara
```

## Base URL

Use `https://api.vectara.io`. Generated paths include `/v2`; adding it to the server URL duplicates the path prefix.

## Auth

Set `x-api-key` with `req.Header.Set("x-api-key", os.Getenv("VECTARA_API_KEY"))` in a request editor.

OAuth client credentials are exchanged at `https://auth.vectara.io/oauth2/token`. Send the access token as `Authorization: Bearer <token>`. Token acquisition and renewal belong to the caller. The spec also has a distinct `GetOAuthToken` operation at `/oauth/token`; do not assume it is the security scheme's token URL.

`VisitorToken` uses `X-Visitor-Id`, carrying the encrypted token returned by visitor creation. `FederatedSignIn` uses a bearer token from a registered trusted issuer. Only operations declaring these schemes accept them.

## Client

- `vectara.NewClientWithResponses(server, opts...)`. Options: `vectara.WithRequestEditorFn`, `vectara.WithHTTPClient` (custom client and timeouts), `vectara.WithBaseURL`.
- Each operation has a raw method returning `*http.Response`, a parsed `...WithResponse` method and a `New...Request` builder. Body operations also expose raw-body variants taking a content type and `io.Reader`.
- Request editors attach credentials. Security constants do not implement authentication.

## Main operations

| Method | Endpoint |
| --- | --- |
| `ListCorporaWithResponse`, `CreateCorpusWithResponse` | `GET`, `POST /v2/corpora` |
| `GetCorpusWithResponse`, `UpdateCorpusWithResponse`, `DeleteCorpusWithResponse` | `GET`, `PATCH`, `DELETE /v2/corpora/{corpus_key}` |
| `ListCorpusDocumentsWithResponse`, `CreateCorpusDocumentWithResponse` | `GET`, `POST /v2/corpora/{corpus_key}/documents` |
| `SearchCorpusWithResponse`, `QueryCorpusWithResponse` | `GET`, `POST /v2/corpora/{corpus_key}/query` |
| `QueryWithResponse` | `POST /v2/query` |
| `ListChatsWithResponse`, `CreateChatWithResponse` | `GET`, `POST /v2/chats` |
| `ListAgentsWithResponse`, `CreateAgentWithResponse` | `GET`, `POST /v2/agents` |
| `CreateAgentInputWithResponse` | `POST /v2/agents/{agent_key}/sessions/{session_key}/events` |
| `ListPipelinesWithResponse` | `GET /v2/pipelines` |

The full operation and type list is in `client_*.gen.go` and the Go reference. The client also covers tools, instructions, aliases, connectors, pipeline runs, metrics, traces, users, API keys and application clients.

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200`, `JSON201` and other generated status fields | Decoded body for that status, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Raw body, HTTP status and response metadata |

Unformatted number fields map to `float64`. Optional fields may be pointers. A non-2xx status does not necessarily produce a Go error; inspect the status and expected success field.

`JsonSchemaObject` emits `default: null` when its `Default` field is unset. Use a raw-body request variant if the JSON Schema default keyword must be omitted.

## Pagination

Many list operations take `PageKey` and `Limit`. Pass the response's `Metadata.PageKey` into the next request until no next key is returned. For `ListCorporaWithResponse`, use `ListCorporaParams.PageKey`. Check optional pointers before access. Search uses `Limit` and `Offset` instead; consult each operation's parameters.

## Streaming and retries

For SSE, use the raw method and process `response.Body` incrementally. Close the body when finished. Parsed methods buffer the full body and do not decode event streams.

The client does not retry or back off. Handle rate limits and transient failures in caller code, considering whether repeating a mutating request is safe.
