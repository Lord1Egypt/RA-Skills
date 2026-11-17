---
name: go-unstructured
description: "Unofficial Go clients for the Unstructured Platform and Partition APIs, generated with oapi-codegen. Package unstructured covers sources, destinations, workflows, jobs, templates, notifications and usage; subpackage partition handles multipart document extraction. Use when Go code needs Unstructured API calls or already imports github.com/psyb0t/go-unstructured."
homepage: https://github.com/psyb0t/go-unstructured
license: MIT
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. Uploads read only files selected by the user."
  shell: "The Go toolchain adds and compiles the module dependency."
  network: "Module installation uses the configured Go module proxy. Runtime requests send API parameters or selected document contents over HTTPS to platform.unstructuredapp.io or api.unstructuredapp.io."
---

# go-unstructured

Unofficial typed Go clients for Unstructured. Use package `unstructured` at the module root for Platform operations and subpackage `partition` for document partitioning.

Read [references/setup.md](references/setup.md) for installation, base URLs, operation names, upload handling and pagination.

## Security & safety

- Read the API key from `UNSTRUCTURED_API_KEY` and set `unstructured-api-key` in a request editor. Never hardcode, commit or log it.
- Use `https://platform.unstructuredapp.io` for Platform and `https://api.unstructuredapp.io` for Partition. Upload requests send the selected document's contents to Unstructured.
- Creating, updating or deleting connectors, workflows or notification channels, running or cancelling jobs, and uploading documents act on the account or send data. Perform those actions only when the user requested them, on the resources and files in scope.

## When to use

- Go code needs Unstructured source or destination connectors, workflows, jobs, templates, notifications or usage.
- Go code needs to partition a document into elements.
- The project imports `github.com/psyb0t/go-unstructured` or its `partition` subpackage.

## When NOT to use

- The project is not Go.
- The user needs a client maintained by Unstructured. This module is unofficial.
- The task changes generated client code. Read the repository's `AGENTS.md` for generation instructions.

## Finding endpoints and types

The usage notes below cover a few calls. Every operation in each spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-unstructured`, from inside your module:

```bash
go doc github.com/psyb0t/go-unstructured ClientWithResponsesInterface            # every Platform endpoint method
go doc github.com/psyb0t/go-unstructured ListSourcesParams                       # one method, params type or model
go doc -all github.com/psyb0t/go-unstructured                                    # the whole Platform package
go doc github.com/psyb0t/go-unstructured/partition ClientWithResponsesInterface  # the Partition endpoint method
go doc github.com/psyb0t/go-unstructured/partition PartitionParameters           # Partition multipart form fields
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-unstructured.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Operations with multipart bodies (`PartitionWithBodyWithResponse`, `CreateJobWithBodyWithResponse`, `RunWorkflowWithBodyWithResponse`) have only the `WithBody` variant, which takes a content type and an `io.Reader` in place of the typed body.

## Usage

Construct `unstructured.NewClientWithResponses` with the Platform base URL and `unstructured.WithRequestEditorFn`. The editor sets `req.Header.Set("unstructured-api-key", os.Getenv("UNSTRUCTURED_API_KEY"))`. Then call `ListSourcesWithResponse(ctx, &unstructured.ListSourcesParams{})` to list sources. The complete compiling example is in the root `example_test.go` and README.

For Partition, construct `partition.NewClientWithResponses` with the Partition base URL and `partition.WithRequestEditorFn` using the same header. Call `PartitionWithBodyWithResponse` with a multipart body. See the setup reference before writing an upload.

Check both the returned error and the response status. Errors cover request, transport and decoding failures. API error statuses can return a nil Go error and a nil `JSON200`. Inspect `StatusCode()`, `Body` and any matching decoded error field. Check optional pointers before dereferencing them.

Number fields use `float64`. Both packages expose methods generated from the entire respective spec. Finish by compiling the calling code and testing it against a local HTTP server, without calling the provider during tests.
