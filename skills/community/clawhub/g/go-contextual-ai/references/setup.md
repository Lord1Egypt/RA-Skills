# go-contextual-ai: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`. UUID fields use `github.com/google/uuid` through it.

## Install

```bash
go get github.com/psyb0t/go-contextual-ai
```

The package name is `contextual`:

```go
import "github.com/psyb0t/go-contextual-ai"
```

## Client

- `contextual.NewClientWithResponses(server string, opts ...ClientOption)` returns a `*ClientWithResponses`. Each method returns a typed response struct.
- `contextual.NewClient` is the lower-level variant returning `*http.Response`.
- Options: `WithRequestEditorFn` (runs on every request, used for auth), `WithHTTPClient` (your own `*http.Client`, for timeouts and proxies), `WithBaseURL`.
- Every method also takes trailing `reqEditors ...RequestEditorFn` for per-call headers.

## Auth

The spec's security scheme is HTTP bearer. Send `Authorization: Bearer <key>`; keys are created in the Contextual AI console. Base URL: `https://api.contextual.ai/v1`.

## Method names

Method names are the spec's operation IDs, which repeat the path and HTTP method. Each has three forms: `X` (raw `*http.Response`), `XWithResponse` (typed), and for endpoints with a body `XWithBodyWithResponse` (raw body plus content type, used for multipart uploads).

| Area | Typed methods (`...WithResponse`) |
|---|---|
| Agents | `ListAgentsAgentsGet`, `CreateAgentAgentsPost`, `EditAgentAgentsAgentIdPut`, `DeleteAgentAgentsAgentIdDelete`, `CopyAgentAgentsAgentIdCopyPost`, `GetAgentMetadataAgentsAgentIdMetadataGet`, `ResetAgentAgentsAgentIdResetPut` |
| Agent queries | `QueryAgentsAgentIdQueryPost`, `QueryAgentsAgentIdQueryAclPost`, `ProvideFeedbackAgentsAgentIdFeedbackPost`, `GetRetrievalInfoAgentsAgentIdQueryMessageIdRetrievalInfoGet`, `GetMetricsAgentsAgentIdMetricsGet` |
| Templates | `ListTemplatesAgentsTemplatesGet`, `ListAclTemplatesAgentsTemplatesAclGet`, `GetTemplateConfigurationAgentsTemplatesTemplateGet`, `SaveTemplateAgentsAgentIdTemplatePost` |
| Datastores | `ListDatastoresDatastoresGet`, `CreateDatastoreDatastoresPost`, `EditDatastoreConfigurationDatastoresDatastoreIdPut`, `DeleteDatastoreDatastoresDatastoreIdDelete`, `GetDatastoreMetadataDatastoresDatastoreIdMetadataGet`, `ResetDatastoreDatastoresDatastoreIdResetPut` |
| Documents | `ListDocumentsDatastoresDatastoreIdDocumentsGet`, `IngestDocumentDatastoresDatastoreIdDocumentsPostWithBody` (multipart), `DeleteDocumentDatastoresDatastoreIdDocumentsDocumentIdDelete`, `GetDocumentMetadataDatastoresDatastoreIdDocumentsDocumentIdMetadataGet`, `UpdateDocumentMetadataDatastoresDatastoreIdDocumentsDocumentIdMetadataPut`, `GetParseResultsDatastoresDatastoreIdDocumentsDocumentIdParseGet` |
| Contents and chunks | `GetDocumentContentsDatastoresDatastoreIdContentsGet`, `GetContentMetadataDatastoresDatastoreIdContentsContentIdMetadataGet`, `EditChunkContentDatastoresDatastoreIdChunksContentIdContentPut` |
| Models | `GenerateGeneratePost`, `RerankRerankPost`, `LmunitLmunitPost` |
| Parse | `ParseParsePostWithBody` (multipart), `ParseListJobsParseJobsGet`, `ParseStatusParseJobsJobIdStatusGet`, `ParseResultsParseJobsJobIdResultsGet` |
| Extract | `ListSchemasExtractSchemasGet`, `CreateSchemaExtractSchemasPost`, `UploadDocumentExtractDocumentsUploadPostWithBody` (multipart), `StartExtractionJobExtractJobsPost`, `GetJobStatusExtractJobsJobIdGet`, `GetJobResultsExtractJobsJobIdResultsGet`, and the other `...Extract...` methods |
| Billing | `GetBalanceBillingBalanceGet`, `GetMonthlyUsageEndpointBillingUsagesMonthlyGet`, and the other `...Billing...` methods |
| Users and workspace | `GetUsersUsersGet`, `InviteUsersUsersPost`, `UpdateUserUsersPut`, `RemoveUserUsersDelete`, `GetConsentWorkspacesConsentGet`, `UpdateConsentWorkspacesConsentPut` |

Check `client.gen.go` for the exact parameter and body types of a method before using it.

## Types

- Path IDs are `openapi_types.UUID`, an alias of `uuid.UUID`, so `uuid.Parse` produces one.
- Optional fields are pointers. Plain numbers are `float64`.
- Unions (`oneOf`/`anyOf`) are structs with `As...`/`From...` methods.

## Errors

| Case | What you get |
|---|---|
| Network failure, bad URL, undecodable JSON | non-nil `err` |
| 2xx | `JSON200` set |
| 422 | `JSON422` (`*HTTPValidationError`, list of `ValidationError` in `Detail`) |
| Any other status | `StatusCode()` and raw `Body`, typed fields nil |
