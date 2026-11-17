---
name: go-jina
description: Unofficial Go client for the Jina AI APIs, generated with oapi-codegen. Package `jina` (`github.com/psyb0t/go-jina`) calls api.jina.ai for embeddings, reranking, the model list, chat completions (document OCR) and batch embedding jobs; package `jinareader` (`github.com/psyb0t/go-jina/reader`) calls r.jina.ai to read a web page as markdown, text, HTML or JSON. Every endpoint is a typed `...WithResponse` method on `ClientWithResponses`, auth is a bearer API key set through `WithRequestEditorFn`, and responses decode into `JSON200` and per-status error fields. Use when Go code needs Jina embeddings, a reranker or the Reader API, or already imports go-jina.
license: MIT
homepage: https://github.com/psyb0t/go-jina
user-invocable: true
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends requests only to the base URL you pass: https://api.jina.ai for `jina`, https://r.jina.ai for `jinareader`."
---

# go-jina

Typed Go clients for the Jina AI APIs. `jina` covers api.jina.ai, `jinareader` covers the Reader API at r.jina.ai.

For install details, the full operation list and the union types, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from the environment (`JINA_API_KEY`) and set it in a request editor. Never hardcode it, commit it or log it, and never log the outgoing `Authorization` header.
- Text, images and documents you embed or rerank, and the URLs you read, are sent to Jina AI's servers. Only send data the user is fine sharing with Jina AI.
- Batch jobs cost money and `CancelBatchJobV1BatchBatchIdDelete` cancels one. Create or cancel jobs only when the user asked for it, and only jobs the task owns.

## When to use

- Go code needs text or multimodal embeddings, a reranking pass, or the model list from Jina AI.
- Go code needs a web page as clean markdown or JSON through the Jina Reader.
- The project already imports `github.com/psyb0t/go-jina`.

## When NOT to use

- Web search on s.jina.ai. That API is not in these specs and has no client here.
- Code that is not Go. Call the HTTP API directly or use another client.
- Local or self-hosted embedding models. This client only talks to Jina AI's hosted APIs.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the specs has a generated method, and the specs' descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-jina`, from inside your module:

```bash
go doc github.com/psyb0t/go-jina ClientWithResponsesInterface         # every endpoint method
go doc github.com/psyb0t/go-jina EmbeddingsV3Request                  # one method, params type or model
go doc -all github.com/psyb0t/go-jina                                 # the whole package
go doc github.com/psyb0t/go-jina/reader ClientWithResponsesInterface  # every Reader method
go doc github.com/psyb0t/go-jina/reader GetTargetUrlParams            # the Reader options
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-jina.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. In `jina` the IDs spell out the path and HTTP method (`EmbeddingsV1EmbeddingsPost`); in `jinareader` the `{url}` path parameter is renamed, so the method is `GetTargetUrl`, not `GetUrl`.

## Client and auth

```go
import (
	"context"
	"net/http"
	"os"

	"github.com/psyb0t/go-jina"
)

auth := jina.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("JINA_API_KEY"))

	return nil
})

client, err := jina.NewClientWithResponses("https://api.jina.ai", auth)
if err != nil {
	return err
}
```

`jinareader` has the same `WithRequestEditorFn` and `NewClientWithResponses`; use base URL `https://r.jina.ai`.

## Embeddings

The request body is a union over model families. Fill the variant for the model, then set it on `jina.EmbeddingRequest`:

```go
var input jina.EmbeddingsV3Request_Input
if err := input.FromEmbeddingsV3RequestInput0("hello world"); err != nil {
	return err
}

task := jina.EmbeddingsV3RequestTaskRetrievalQuery

var body jina.EmbeddingRequest
if err := body.FromEmbeddingsV3Request(jina.EmbeddingsV3Request{
	Model: jina.EmbeddingsV3RequestModelJinaEmbeddingsV3,
	Input: input,
	Task:  &task,
}); err != nil {
	return err
}

res, err := client.EmbeddingsV1EmbeddingsPostWithResponse(ctx, body)
if err != nil {
	return err
}

if res.JSON200 == nil {
	return fmt.Errorf("embeddings: status %d: %s", res.StatusCode(), res.Body)
}

data, err := res.JSON200.Data.AsEmbeddingResponseData0() // []SingleEmbeddingData
if err != nil {
	return err
}

vector, err := data[0].Embedding.AsSingleEmbeddingDataEmbedding1() // []float64
```

## Reranking

```go
docs := make([]jina.TextRerankerRequest_Documents_Item, 2)
_ = docs[0].FromTextRerankerRequestDocuments0("first document")
_ = docs[1].FromTextRerankerRequestDocuments0("second document")

var body jina.RerankingRequest
if err := body.FromTextRerankerRequest(jina.TextRerankerRequest{
	Model:     jina.TextRerankerRequestModelJinaRerankerV2BaseMultilingual,
	Query:     "what is a vector",
	Documents: docs,
}); err != nil {
	return err
}

res, err := client.RerankV1RerankPostWithResponse(ctx, body)
// res.JSON200.Results: []RerankingResult with Index and RelevanceScore, best first
```

Check the errors from the `From...` calls in real code; the underscores above only keep the example short.

## Reader

```go
accept := "application/json"

res, err := reader.GetTargetUrlWithResponse(
	ctx,
	"https://example.com",
	&jinareader.GetTargetUrlParams{Accept: &accept},
)
// res.JSON200.Data.Content, .Title, .Url
```

Without `Accept: application/json` the answer is plain text in `res.Body`. Reader options such as `XRespondWith` and `XTargetSelector` are fields on the params struct.

## Errors

A transport failure comes back as `err`. An HTTP error status does not: check `res.StatusCode()` or `res.JSON200 == nil`, then read the typed error field (`res.JSON401`, `res.JSON422`, `res.JSON429` and so on, each a `*jina.ErrorResponse` with `Detail`) or the raw `res.Body`.
