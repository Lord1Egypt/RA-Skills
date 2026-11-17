---
name: go-elevenlabs
description: Unofficial Go client for the ElevenLabs REST API, generated with oapi-codegen. `elevenlabs.NewClientWithResponses("https://api.elevenlabs.io", opts...)` from `github.com/psyb0t/go-elevenlabs` returns a `*elevenlabs.ClientWithResponses` with one typed `...WithResponse` method per endpoint (voices, text to speech, speech to text, sound effects, dubbing, user info and more). Auth is the `xi-api-key` header set through `elevenlabs.WithRequestEditorFn`; JSON replies decode into `JSON200`, and audio replies come back as raw bytes in `Body`. Use when Go code needs to call ElevenLabs or already imports go-elevenlabs.
license: MIT
homepage: https://github.com/psyb0t/go-elevenlabs
user-invocable: true
metadata:
  openclaw:
    emoji: "🔊"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to the Go source of the current project. The library reads and writes no files."
  shell: "The Go toolchain (`go get`, `go build`, `go test`) to add and compile the dependency."
  network: "HTTPS to the ElevenLabs API at api.elevenlabs.io, and `go get` to your Go module proxy."
---

# go-elevenlabs

Typed Go client for the ElevenLabs API. Every endpoint in the ElevenLabs OpenAPI document is a method on `ClientWithResponses`.

For install, client options, more operations and response handling, see [references/setup.md](references/setup.md).

## Security & safety

- Read the API key from an environment variable such as `ELEVENLABS_API_KEY`. Never hardcode it, commit it or log it, and never print request headers.
- Requests go only to the base URL you pass, `https://api.elevenlabs.io`. Text, audio and voice samples you send are processed by ElevenLabs.
- Generation endpoints use account credits, and voice cloning and delete endpoints change the account. Call them only when the user asked for that action, and clone only voices the user has the rights to.

## When to use

- Go code needs to list voices, turn text into speech, transcribe audio or call another ElevenLabs endpoint.
- The project already imports `github.com/psyb0t/go-elevenlabs`.

## When NOT to use

- You need the realtime WebSocket APIs. This client covers only the REST API.
- The code is not Go.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-elevenlabs`, from inside your module:

```bash
go doc github.com/psyb0t/go-elevenlabs ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-elevenlabs TextToSpeechFullParams        # one method, params type or model
go doc -all github.com/psyb0t/go-elevenlabs                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-elevenlabs.

Method names come from the spec's operation IDs. `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status. Operations with a request body also have a `<OperationId>WithBodyWithResponse` variant that takes a content type and an `io.Reader`, which multipart uploads such as speech to text need.

## Usage

```go
import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/psyb0t/go-elevenlabs"
)

auth := elevenlabs.WithRequestEditorFn(
	func(_ context.Context, req *http.Request) error {
		req.Header.Set("xi-api-key", os.Getenv("ELEVENLABS_API_KEY"))

		return nil
	},
)

client, err := elevenlabs.NewClientWithResponses(
	"https://api.elevenlabs.io",
	auth,
)
if err != nil {
	return err
}

voices, err := client.GetVoicesWithResponse(ctx, nil)
if err != nil {
	return err // transport failure
}

if voices.JSON200 == nil {
	return fmt.Errorf("elevenlabs: status %d", voices.StatusCode())
}

for _, voice := range voices.JSON200.Voices {
	fmt.Println(voice.VoiceId, voice.Name)
}
```

Text to speech. A 200 reply is audio, so read `Body`:

```go
speech, err := client.TextToSpeechFullWithResponse(
	ctx,
	voiceID,
	nil,
	elevenlabs.TextToSpeechFullJSONRequestBody{Text: "Hello there."},
)
if err != nil {
	return err
}

if speech.StatusCode() != http.StatusOK {
	return fmt.Errorf("elevenlabs: status %d", speech.StatusCode())
}

audio := speech.Body // encoded per params.OutputFormat, e.g. mp3_44100_128
```

Leave the `XiApiKey` field of any `...Params` struct nil and let the request editor set the header.

A method returns an error only when the request could not be sent or the body could not be decoded. An API error is a normal response: check `StatusCode()`; a 422 also fills `JSON422`, an `*HTTPValidationError`.
