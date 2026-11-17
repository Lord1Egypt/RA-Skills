# go-unstructured: setup and reference

This module is unofficial and not affiliated with Unstructured.

## Requirements

- Go 1.26.10 or newer, as declared in `go.mod`.
- An Unstructured API key exported as `UNSTRUCTURED_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-unstructured
```

Import `github.com/psyb0t/go-unstructured` for package `unstructured` or `github.com/psyb0t/go-unstructured/partition` for package `partition`.

## Base URLs and auth

| Package | Base URL |
| --- | --- |
| `unstructured` | `https://platform.unstructuredapp.io` |
| `partition` | `https://api.unstructuredapp.io` |

Both clients need a request editor that sets the `unstructured-api-key` header from the environment. Use `unstructured.WithRequestEditorFn` or `partition.WithRequestEditorFn` for the corresponding package. The Platform document models the key as an optional header parameter. Partition declares the `ApiKeyAuth` scheme and an anonymous alternative. Neither generated client adds a key automatically.

## Clients

Both packages provide `NewClientWithResponses(server, opts...)`, `WithRequestEditorFn`, `WithHTTPClient` and `WithBaseURL`. Supply an `*http.Client` with a timeout through `WithHTTPClient` when needed.

Each operation has a raw response method on `Client`, a parsed `...WithResponse` method on `ClientWithResponses`, and a `New...Request` constructor. JSON body operations provide typed body methods and raw body variants taking a content type and `io.Reader`. Multipart operations provide the raw body variant only.

## Platform operations

| Methods | Endpoints |
| --- | --- |
| `ListSourcesWithResponse`, `CreateSourceWithResponse` | `GET`, `POST /api/v1/sources/` |
| `GetSourceWithResponse`, `UpdateSourceWithResponse`, `DeleteSourceWithResponse` | `GET`, `PUT`, `DELETE /api/v1/sources/{source_id}` |
| `ListDestinationsWithResponse`, `CreateDestinationWithResponse` | `GET`, `POST /api/v1/destinations/` |
| `GetDestinationWithResponse`, `UpdateDestinationWithResponse`, `DeleteDestinationWithResponse` | `GET`, `PUT`, `DELETE /api/v1/destinations/{destination_id}` |
| `ListWorkflowsWithResponse`, `CreateWorkflowWithResponse` | `GET`, `POST /api/v1/workflows/` |
| `GetWorkflowWithResponse`, `UpdateWorkflowWithResponse`, `DeleteWorkflowWithResponse` | `GET`, `PUT`, `DELETE /api/v1/workflows/{workflow_id}` |
| `RunWorkflowWithBodyWithResponse` | `POST /api/v1/workflows/{workflow_id}/run` |
| `ListJobsWithResponse`, `CreateJobWithBodyWithResponse` | `GET`, `POST /api/v1/jobs/` |
| `GetJobWithResponse`, `CancelJobWithResponse` | `GET /api/v1/jobs/{job_id}`, `POST /api/v1/jobs/{job_id}/cancel` |
| `DownloadJobOutputWithResponse` | `GET /api/v1/jobs/{job_id}/download` |
| `GetJobDetailsWithResponse`, `GetJobFailedFilesWithResponse`, `GetJobFileStatusWithResponse` | `GET /api/v1/jobs/{job_id}/details`, `/failed-files`, `/file-status` |
| `ListTemplatesWithResponse`, `GetTemplateWithResponse` | `GET /api/v1/templates/`, `/api/v1/templates/{template_id}` |

Connection-check, notification, usage and account consumption operations are also generated. Some notification and usage method names contain the full route from their operation ID. Look up their exact names and required parameters with `go doc`, as the skill's "Finding endpoints and types" section shows.

Creating a job and running a workflow accept multipart bodies. Build those bodies with a multipart writer and pass the resulting content type, as with Partition uploads below. Their form fields differ; consult the generated request body models before building them.

The generation patch reduces UUID-or-string unions to ordinary `string` fields and parameters. The unrestricted string branch already accepts any string; the patch avoids anonymous union parameter structs with inaccessible storage. Other UUID-only fields still use the generated UUID type. Check the method signature before passing an identifier.

## Partition uploads

The Partition API exposes `POST /general/v0/general`. Its `PartitionWithBodyWithResponse` method accepts a context, `*partition.PartitionParams`, content type, body reader and optional request editors.

Build the request with `mime/multipart.NewWriter`. Add the document with `CreateFormFile("files", filename)`, write any options as form fields, close the multipart writer, and pass its `FormDataContentType()` with the completed body. Closing the writer before the request writes the final boundary. The generated client does not read files or build multipart bodies for you. `partition/client_test.go` demonstrates the request against a local server.

On JSON success, `JSON200` points to a slice of `partition.Element`. The spec also allows CSV output. For a CSV response, inspect `Body` and the response content type rather than expecting `JSON200`.

## Responses and pagination

`JSON200` is the decoded successful JSON body where specified. `Body`, `StatusCode()`, `Status()` and `HTTPResponse` expose the raw response. Error statuses do not necessarily produce a Go error; check the status and the relevant decoded field.

Open-ended additional properties, including Partition element fields, and unspecified JSON response bodies use `json.RawMessage`. Decode a selected value into the concrete type the calling code expects with `json.Unmarshal`. Keeping these values as raw JSON preserves large integers and nested data.

`ListWorkflowsParams` provides `Page` and `PageSize`; the spec defaults are 1 and 20. Workflow list responses are arrays, without a generated next-page token. Increment the page and stop when a page has fewer items than requested. Other list methods have their own filters; do not assume a shared pagination envelope.

The clients do not add retries or rate-limit handling. Handle 429 and transient failures in the caller with bounded retries appropriate to the operation.
