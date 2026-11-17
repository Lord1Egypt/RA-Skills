---
name: go-runway
description: Unofficial Go client for the Runway API, generated with oapi-codegen from Runway's OpenAPI document. Package runway (github.com/psyb0t/go-runway) has typed methods on runway.ClientWithResponses for all 49 paths of https://api.dev.runwayml.com, among them text, image and video to video, text to image, upscaling, text to speech, sound effects, voice dubbing, voices, avatars, realtime sessions, recipes, workflows, documents, uploads, task polling and cancelling, and organization credit balance and usage. Requests authenticate with a Bearer API key plus the X-Runway-Version header set to 2024-11-06, both set in one request editor. Use when Go code needs to call Runway's generation API, poll a Runway task, or already imports go-runway.
license: MIT
homepage: https://github.com/psyb0t/go-runway
user-invocable: true
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "`go get` fetches the module from your Go module proxy. At runtime the client sends HTTPS requests only to the base URL you pass, https://api.dev.runwayml.com."
---

# go-runway

Typed Go client for the Runway API. Every endpoint in Runway's OpenAPI document has a method on `runway.ClientWithResponses`, and responses decode into `JSON200`, `JSON400` and the other status fields.

For install details, method naming, union types and the full operation list, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from the environment (`RUNWAYML_API_SECRET`). Never hardcode it, commit it, or log it, and never print a request's headers.
- Requests go only to `https://api.dev.runwayml.com`. Prompts, images and other inputs you send leave the machine for Runway's servers.
- Generation endpoints spend the organization's credits. Start a generation, cancel or delete a task, or delete an avatar, voice, document or workflow only when the user asked for it, and only on resources the task created or named.

## When to use

- Go code needs to start a Runway generation (image, video, audio, speech) and poll the resulting task.
- Go code needs Runway account data: credit balance, usage, avatars, voices, workflows.
- The project already imports `github.com/psyb0t/go-runway`.

## When NOT to use

- The code is not Go. Runway ships official Python and Node SDKs.
- You only need a single curl call in a shell script.
- You need a high level helper that waits for a task. This client is generated and stops at one HTTP call per method; polling is your loop.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-runway`, from inside your module:

```bash
go doc github.com/psyb0t/go-runway ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-runway PostV1TextToImageJSONBody1    # one method, params type or model
go doc -all github.com/psyb0t/go-runway                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-runway.

The spec has no operation IDs, so method names come from the HTTP method and path: `GET /v1/tasks/{id}` is `GetV1TasksIdWithResponse`. A method takes the context, then the path parameters in order, then a `*<Name>Params` struct when the operation has query parameters (for example `GetV1AvatarsParams`), then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Models are in `types.gen.go` and the client in `client.gen.go`, both in package `runway`, so `go doc` shows both. Send union request bodies through `...WithBodyWithResponse`, as in the second example below.

## Usage

```go
import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-runway"
)

auth := runway.WithRequestEditorFn(func(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+os.Getenv("RUNWAYML_API_SECRET"))
	req.Header.Set("X-Runway-Version", "2024-11-06")

	return nil
})

client, err := runway.NewClientWithResponses("https://api.dev.runwayml.com", auth)
if err != nil {
	return err
}

org, err := client.GetV1OrganizationWithResponse(ctx)
if err != nil {
	return err // transport error
}

if org.JSON200 == nil {
	return fmt.Errorf("runway: status %d: %s", org.StatusCode(), org.Body)
}

fmt.Println(org.JSON200.CreditBalance)
```

Starting a text to image task and reading its status. Most request bodies are union types (one variant per model): fill the variant's struct and load it with the matching `From...` method on the `...JSONBody` type. Send a union body through the `...WithBodyWithResponse` method as marshaled JSON. The typed `...JSONRequestBody` methods marshal a union body as `{}`, because that named type does not carry the union's `MarshalJSON`.

```go
var body runway.PostV1TextToImageJSONBody

if err := body.FromPostV1TextToImageJSONBody1(runway.PostV1TextToImageJSONBody1{
	Model:      runway.PostV1TextToImageJSONBody1ModelGen4Image,
	PromptText: "a lighthouse at dusk, oil painting",
	Ratio:      runway.PostV1TextToImageJSONBody1RatioN10801080,
}); err != nil {
	return err
}

payload, err := json.Marshal(body)
if err != nil {
	return err
}

created, err := client.PostV1TextToImageWithBodyWithResponse(
	ctx,
	"application/json",
	bytes.NewReader(payload),
)
if err != nil {
	return err
}

if created.JSON200 == nil {
	return fmt.Errorf("runway: status %d: %s", created.StatusCode(), created.Body)
}

task, err := client.GetV1TasksIdWithResponse(ctx, created.JSON200.Id)
if err != nil {
	return err
}

// Every task variant carries status, so read it through any variant first,
// then decode the variant that matches.
head, err := task.JSON200.AsGetV1TasksId200JSONResponseBody0()
if err != nil {
	return err
}

if head.Status == "SUCCEEDED" {
	done, err := task.JSON200.AsGetV1TasksId200JSONResponseBody5()
	if err != nil {
		return err
	}

	fmt.Println(done.Output) // URLs of the generated files
}
```

A non-2xx response is not a Go error. Check the status field you expect (`JSON200`) or `StatusCode()`, and read `Body` for the raw error.
