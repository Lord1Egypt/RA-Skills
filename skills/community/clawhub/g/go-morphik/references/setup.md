# go-morphik: setup and reference

This module is unofficial and not affiliated with Morphik.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A Morphik API key, exported as `MORPHIK_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-morphik
```

## Base URL and auth

The vendor SDK defaults to `https://api.morphik.ai` and sends `Authorization: Bearer <key>`. Supply that URL to `morphik.NewClientWithResponses`, or select your own Morphik deployment. Set the header in a `morphik.WithRequestEditorFn` callback. The generated client does not read environment variables itself.

The public spec has no `servers` or `securitySchemes` entries. It exposes optional `authorization` header parameters on protected operations instead.

## Client

- `morphik.NewClientWithResponses(server, opts...)`. Options: `morphik.WithRequestEditorFn`, `morphik.WithHTTPClient` (for your own HTTP client and timeouts), `morphik.WithBaseURL`.
- Each operation has a raw `Client` method, a parsed `ClientWithResponses` method ending in `WithResponse`, and a request constructor. JSON operations also expose typed request body methods. Raw body methods accept a content type and an `io.Reader`.

## Main operations

| Method | Endpoint |
|---|---|
| `GetAvailableModelsModelsGetWithResponse` | `GET /models` |
| `IngestTextIngestTextPostWithResponse` | `POST /ingest/text` |
| `ListDocsDocumentsPostWithResponse` | `POST /documents` |
| `ListDocsDocumentsListDocsPostWithResponse` | `POST /documents/list_docs` (alias) |
| `GetDocumentDocumentsDocumentIdGetWithResponse` | `GET /documents/{document_id}` |
| `DeleteDocumentDocumentsDocumentIdDeleteWithResponse` | `DELETE /documents/{document_id}` |
| `RetrieveChunksRetrieveChunksPostWithResponse` | `POST /retrieve/chunks` |
| `RetrieveDocumentsRetrieveDocsPostWithResponse` | `POST /retrieve/docs` |
| `QueryCompletionQueryPostWithResponse` | `POST /query` |
| `SearchDocumentsByNameSearchDocumentsPostWithResponse` | `POST /search/documents` |
| `HealthCheckHealthGetWithResponse` | `GET /health` |

The full client preserves all 72 operations across 63 paths, including ingestion uploads, document summaries, collection routes under `/folders`, models, API keys, logs, usage, connectors, cloud apps and chats. Request bodies include `IngestTextRequest`, `ListDocsRequest`, `RetrieveRequest` and `CompletionQueryRequest`.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200` | The decoded JSON body on success, nil otherwise |
| `JSON422` | A decoded validation error where the spec defines one |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

Number fields are `float64`. Optional fields can be pointers or generated union types. Check the generated definitions before building a request or dereferencing a response.

## Pagination

`ListDocsRequest` supports `Skip` and `Limit`. Its `ListDocsResponse` contains `ReturnedCount`, `HasMore` and `NextSkip`, plus optional `TotalCount` when requested. Continue with `NextSkip` while `HasMore` is true. Listing uses POST with a JSON body, not GET.

## Pitfalls

- Long generated method names come from FastAPI operation IDs. Use the actual generated name rather than an SDK's shorter method name.
- `/documents` and `/documents/list_docs` are aliases and have distinct generated methods.
- File ingestion uses multipart form bodies. Build one with `mime/multipart`, pass the reader to the raw body method, and use the writer's `FormDataContentType()` value.
- The client does not automatically retry HTTP errors, walk pages or decode streaming events. Inspect the status and response body before choosing a retry policy.
