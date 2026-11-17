# go-zeroentropy: setup and reference

This module is unofficial and not affiliated with ZeroEntropy.

## Requirements

- Go 1.26.10 or newer, per `go.mod`.
- A ZeroEntropy API key from the [dashboard](https://dashboard.zeroentropy.dev/), exported as `ZEROENTROPY_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-zeroentropy
```

## Base URLs

| Region | Base URL |
| --- | --- |
| Default | `https://api.zeroentropy.dev/v1` |
| EU datacenters | `https://eu-api.zeroentropy.dev/v1` |

The base URL includes `/v1`. Choose the region containing the user's collections.

## Auth

The spec's `HTTPBearer` scheme requires `req.Header.Set("Authorization", "Bearer "+key)` in a `zeroentropy.WithRequestEditorFn`. The client does not read credentials from the environment itself. The README and `example_test.go` show the complete setup.

Document and page-image GET endpoints use a required `token` query parameter instead of the bearer security scheme. Treat these tokens as credentials and avoid logging their URLs. A document update that changes the document ID invalidates its existing download URLs.

## Client

- `zeroentropy.NewClientWithResponses(server, opts...)` creates the parsed-response client.
- Options include `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`. Supply an `http.Client` with an appropriate timeout for model calls.
- Each operation has a raw `Client.X`, parsed `ClientWithResponses.XWithResponse` and request-only `NewXRequest`. Operations with JSON request bodies also expose `XWithBodyWithResponse` for an `io.Reader`.
- Request body aliases end in `JSONRequestBody`. For example, the collection-list method accepts `EmptyRequest{}`, and retrieval uses `TopDocumentsRequest`, `TopPagesRequest` or `TopSnippetsRequest`.

## Operations

Paths below are relative to `/v1`. The full spec contains 30 operations, including endpoints marked hidden by the provider.

| Method | Endpoint |
| --- | --- |
| `CreateOrganizationAdminCreateOrganizationPostWithResponse` | `POST /admin/create-organization` |
| `GetOrganizationAdminGetOrganizationPostWithResponse` | `POST /admin/get-organization` |
| `UpdateOrganizationAdminUpdateOrganizationPostWithResponse` | `POST /admin/update-organization` |
| `AddApiKeyAdminAddApiKeyPostWithResponse` | `POST /admin/add-api-key` |
| `ListApiKeysAdminListApiKeysPostWithResponse` | `POST /admin/list-api-keys` |
| `DeleteApiKeyAdminDeleteApiKeyPostWithResponse` | `POST /admin/delete-api-key` |
| `UpdateApiKeyAdminUpdateApiKeyPostWithResponse` | `POST /admin/update-api-key` |
| `GetDocumentUsageUsageDocumentsPostWithResponse` | `POST /usage/documents` |
| `GetQueryUsageUsageQueriesPostWithResponse` | `POST /usage/queries` |
| `GetModelsRerankerUsageUsageModelsRerankerPostWithResponse` | `POST /usage/models/reranker` |
| `GetModelsEmbedUsageUsageModelsEmbedPostWithResponse` | `POST /usage/models/embed` |
| `GetModelsUsageCountersUsageModelsCountersPostWithResponse` | `POST /usage/models/counters` |
| `GetUsageCountersUsageCountersPostWithResponse` | `POST /usage/counters` |
| `RerankModelsRerankPostWithResponse` | `POST /models/rerank` |
| `EmbedModelsEmbedPostWithResponse` | `POST /models/embed` |
| `GetStatusStatusGetStatusPostWithResponse` | `POST /status/get-status` |
| `AddCollectionCollectionsAddCollectionPostWithResponse` | `POST /collections/add-collection` |
| `GetCollectionListCollectionsGetCollectionListPostWithResponse` | `POST /collections/get-collection-list` |
| `DeleteCollectionCollectionsDeleteCollectionPostWithResponse` | `POST /collections/delete-collection` |
| `AddDocumentDocumentsAddDocumentPostWithResponse` | `POST /documents/add-document` |
| `UpdateDocumentDocumentsUpdateDocumentPostWithResponse` | `POST /documents/update-document` |
| `GetDocumentInfoDocumentsGetDocumentInfoPostWithResponse` | `POST /documents/get-document-info` |
| `GetDocumentInfoListDocumentsGetDocumentInfoListPostWithResponse` | `POST /documents/get-document-info-list` |
| `DeleteDocumentDocumentsDeleteDocumentPostWithResponse` | `POST /documents/delete-document` |
| `GetPageInfoDocumentsGetPageInfoPostWithResponse` | `POST /documents/get-page-info` |
| `GetDocumentDocumentsGetDocumentGetWithResponse` | `GET /documents/get-document` |
| `GetPageImageDocumentsGetPageImageGetWithResponse` | `GET /documents/get-page-image` |
| `TopDocumentsQueriesTopDocumentsPostWithResponse` | `POST /queries/top-documents` |
| `TopPagesQueriesTopPagesPostWithResponse` | `POST /queries/top-pages` |
| `TopSnippetsQueriesTopSnippetsPostWithResponse` | `POST /queries/top-snippets` |

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200` | The decoded JSON success body, nil if absent |
| `JSON422` | The decoded validation error, when supplied |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Raw body, status and HTTP response |

Check the HTTP status even when the Go error is nil. Adding a new document returns 201 with no typed JSON payload; overwriting returns 200. Optional or nullable fields may be pointers. Scores and numeric embeddings are `float64`.

The document and page-image GET descriptions promise binary document data and JPEG images, but their schemas advertise JSON with an empty schema. A spec patch maps these two success schemas to `json.RawMessage`, so their `JSON200` fields preserve JSON bytes without decoding arbitrary objects. For binary content, use `Body` or the raw `Client` methods, closing the raw response body after reading it. `JSON200` does not decode binary content.

## Pagination and indexing

`GetDocumentInfoListDocumentsGetDocumentInfoListPostWithResponse` returns documents in lexicographic path order. Set `GetDocumentInfoListRequest.PathGt` to the last returned document's `Path` for the next request, keeping the collection and prefix unchanged. Stop when no documents remain. `Limit` defaults to 1024 and cannot exceed 1024.

Documents can take time to appear in retrieval after insertion. Use `GetStatusStatusGetStatusPostWithResponse` to inspect indexing progress. Collection listing returns the complete list.

## Retrieval and models

`TopDocumentsRequest.Query` is a required nullable pointer. A nil query requests filtering without relevance ordering and still incurs normal query cost. For document retrieval, `K` is between 1 and 2048, and non-null query text cannot exceed 4096 UTF-8 bytes. Query filters use the generated `StrJson` type and the provider's metadata-filtering format.

Reranking uses `RerankRequest`; embeddings use `EmbedRequest`. Their model fields select a model supported by the service. Embedding input is a generated union supporting either a string or a string array. Use its generated `FromEmbedRequestInput0` and `FromEmbedRequestInput1` helpers rather than writing the union's internal representation. Embedding responses can contain numeric vectors or base64-encoded float32 bytes, depending on the requested encoding.

## Rate limits

The client does not retry automatically. Inspect 429 responses and back off. Model requests can select fast or slow latency; explicitly requesting fast can return 429 when that capacity is exhausted. Choose timeouts that allow the selected latency mode.
