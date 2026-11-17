# go-elevenlabs: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- An ElevenLabs API key, from the API keys page of the account settings.

## Install

```bash
go get github.com/psyb0t/go-elevenlabs
```

The package name is `elevenlabs`:

```go
import "github.com/psyb0t/go-elevenlabs"
```

## Auth

ElevenLabs authenticates with one header, `xi-api-key`. Set it once with `elevenlabs.WithRequestEditorFn`, as in SKILL.md.

The spec also lists `xi-api-key` as an optional header parameter on most operations, so most `...Params` structs have an `XiApiKey` field. Leave it nil. Request editors run after the params are applied, so a client-wide editor overrides a per-call `XiApiKey`.

## Client options

| Option | Effect |
|---|---|
| `elevenlabs.WithRequestEditorFn(fn)` | Runs `fn` on every request, used for the auth header. |
| `elevenlabs.WithHTTPClient(doer)` | Replaces `http.DefaultClient`, for timeouts or transport settings. Long audio can take a while; set a generous timeout. |
| `elevenlabs.WithBaseURL(url)` | Overrides the server passed to the constructor. |

Base URL: `https://api.elevenlabs.io`. Paths in the spec already start with `/v1` or `/v2`.

## Calling operations

Each operation `X` in the spec has:

- `client.XWithResponse(ctx, pathParams..., params, ...)` returning `*XResponse`.
- For operations with a JSON body, `client.XWithResponse(ctx, pathParams..., params, body)` takes the typed `XJSONRequestBody`, and `client.XWithBodyWithResponse(ctx, pathParams..., params, contentType, io.Reader)` takes raw bytes. Multipart uploads such as speech to text use the `WithBody` form with a `multipart.Writer`.

Some operations:

| Method | Endpoint |
|---|---|
| `GetVoicesWithResponse(ctx, *GetVoicesParams)` | `GET /v1/voices` |
| `GetUserInfoWithResponse(ctx, *GetUserInfoParams)` | user account info |
| `GetUserSubscriptionInfoWithResponse(ctx, *GetUserSubscriptionInfoParams)` | subscription and character usage |
| `TextToSpeechFullWithResponse(ctx, voiceId, *TextToSpeechFullParams, TextToSpeechFullJSONRequestBody)` | `POST /v1/text-to-speech/{voice_id}` |
| `TextToSpeechStreamWithResponse(ctx, voiceId, *TextToSpeechStreamParams, TextToSpeechStreamJSONRequestBody)` | streaming text to speech, read in full |

Run `go doc github.com/psyb0t/go-elevenlabs ClientWithResponsesInterface` to list the rest. Do not guess a method name.

`TextToSpeechFullJSONRequestBody` (`BodyTextToSpeechFull`) needs `Text`; `ModelId` and the voice settings are optional. `TextToSpeechFullParams.OutputFormat` picks the codec, sample rate and bitrate, formatted as `codec_sample_rate_bitrate`; some formats need a paid tier.

## Responses

Every `XResponse` has:

- `Body []byte` and `HTTPResponse *http.Response`.
- `StatusCode()` and `Status()`.
- `JSON200` for JSON replies. Audio replies have no `JSON200`; the audio is in `Body`.
- Most operations also have `JSON422 *HTTPValidationError` with a `Detail` list.

A method returns a non-nil error only for transport failures and bodies that do not decode. The `...WithResponse` methods read the whole body into memory; for a long stream, call the same operation on the raw `Client` and read `*http.Response.Body` yourself.

## Regenerating

`client.gen.go` is generated. For changes to the client itself, see `AGENTS.md` in the repository.
