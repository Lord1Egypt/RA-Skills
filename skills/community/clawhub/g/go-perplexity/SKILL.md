---
name: go-perplexity
description: Unofficial Go client for the Perplexity REST API at https://api.perplexity.ai. Package perplexity (github.com/psyb0t/go-perplexity), generated with oapi-codegen from Perplexity's OpenAPI document, has one typed method per endpoint on the client from perplexity.NewClientWithResponses, covering Sonar chat completions (sync and async), web search, embeddings and contextualized embeddings, agents and their files, skills, decisions, models and usage analytics, with JSON bodies decoded into Go structs. Auth is a bearer API key set through a request editor. Use when Go code needs to call the Perplexity API or already imports go-perplexity.
license: MIT
homepage: https://github.com/psyb0t/go-perplexity
user-invocable: true
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends requests only to the base URL you pass, https://api.perplexity.ai."
---

# go-perplexity

Typed Go client for the Perplexity API. Every endpoint in Perplexity's OpenAPI document is a method on `ClientWithResponses`.

For install, the method list, union types and error handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `PERPLEXITY_API_KEY`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL passed to `NewClientWithResponses`. Use `https://api.perplexity.ai`.
- Calls cost money and some change account state (creating, updating and deleting skills, creating and cancelling agent runs). Make those calls only when the user asked for them, and only on resources the task created or named.

## When to use

- Go code needs Sonar answers with citations, Perplexity web search, embeddings or another Perplexity endpoint.
- The project already imports `github.com/psyb0t/go-perplexity`.

## When NOT to use

- The code is not Go.
- You need streaming. The generated methods read the whole response body; for server-sent events, use the plain `Client` method, which returns the `*http.Response` with the body unread, and parse the stream yourself.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-perplexity`, from inside your module:

```bash
go doc github.com/psyb0t/go-perplexity ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-perplexity ApiChatCompletionsRequest     # one method, params type or model
go doc -all github.com/psyb0t/go-perplexity                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-perplexity.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Skill create and update have only raw body forms, `CreateSkillWithBodyWithResponse` and `UpdateSkillWithBodyWithResponse`, which take a content type and an `io.Reader`.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-perplexity"
)

auth := perplexity.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("PERPLEXITY_API_KEY"))

	return nil
})

client, err := perplexity.NewClientWithResponses("https://api.perplexity.ai", auth)
if err != nil {
	return err
}
```

A Sonar chat completion. Message content is a union, built and read with `From...` and `As...` helpers (`Content0` is plain text):

```go
var content perplexity.ChatMessageInput_Content
if err := content.FromChatMessageInputContent0("What changed in Go 1.26?"); err != nil {
	return err
}

res, err := client.ChatCompletionsChatCompletionsPostWithResponse(ctx, perplexity.ApiChatCompletionsRequest{
	Model: perplexity.ApiChatCompletionsRequestModelSonar,
	Messages: []perplexity.ChatMessageInput{{
		Content: &content,
		Role:    perplexity.ChatMessageRoleUser,
	}},
})
if err != nil {
	return err // transport error
}

if res.JSON200 == nil {
	return fmt.Errorf("sonar: status %d: %s", res.StatusCode(), res.Body)
}

for _, choice := range res.JSON200.Choices {
	if choice.Message.Content == nil {
		continue
	}

	text, err := choice.Message.Content.AsChatMessageOutputContent0()
	if err == nil {
		fmt.Println(text)
	}
}
```

A web search:

```go
var query perplexity.ApiSearchRequest_Query
if err := query.FromApiSearchRequestQuery0("go generics tutorial"); err != nil {
	return err
}

maxResults := 5

found, err := client.SearchSearchPostWithResponse(ctx, perplexity.ApiSearchRequest{
	Query:      query,
	MaxResults: &maxResults,
})
if err != nil {
	return err
}

if found.JSON200 == nil {
	return fmt.Errorf("search: status %d: %s", found.StatusCode(), found.Body)
}

for _, page := range found.JSON200.Results {
	fmt.Println(page.Title, page.Url)
}
```
