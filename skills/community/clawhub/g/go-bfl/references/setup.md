# go-bfl: setup and reference

This module is unofficial and not affiliated with Black Forest Labs.

## Requirements and install

Go 1.26.10 or newer, per `go.mod`. Export the API key as `BFL_API_KEY`.

```sh
go get github.com/psyb0t/go-bfl
```

## Base URL and auth

Use `https://api.bfl.ai`. The `APIKeyHeader` scheme sends the key in the `x-key` header. Set it through `bfl.WithRequestEditorFn(func(_ context.Context, req *http.Request) error { req.Header.Set("x-key", key); return nil })`. The result endpoint declares no security requirement, but a client-wide editor adds the header there too.

## Client

- `bfl.NewClientWithResponses(server, opts...)`.
- Options: `WithRequestEditorFn`, `WithHTTPClient` for timeouts, `WithBaseURL`.
- Each operation has a raw method, a parsed `...WithResponse` method and a `New...Request` constructor. JSON bodies also have `...WithBodyWithResponse` methods accepting an `io.Reader`.

## Main operations

| Parsed method | Endpoint |
| --- | --- |
| `FluxPro11V1FluxPro11PostWithResponse` | `POST /v1/flux-pro-1.1` |
| `FluxDevV1FluxDevPostWithResponse` | `POST /v1/flux-dev` |
| `GenerateFlux11UltraV1FluxPro11UltraPostWithResponse` | `POST /v1/flux-pro-1.1-ultra` |
| `GenerateFlux2ProV1Flux2ProPostWithResponse` | `POST /v1/flux-2-pro` |
| `GenerateFluxKontextProV1FluxKontextProPostWithResponse` | `POST /v1/flux-kontext-pro` |
| `Flux3ImageV1Flux3ImagePostWithResponse` | `POST /v1/flux-3-image` |
| `Flux3VideoV1Flux3VideoPostWithResponse` | `POST /v1/flux-3-video` |
| `GetResultV1GetResultGetWithResponse` | `GET /v1/get_result?id=...` |
| `GetCreditsV1CreditsGetWithResponse` | `GET /v1/credits` |
| `MyFinetunesV1MyFinetunesGetWithResponse` | `GET /v1/my_finetunes` |
| `FinetuneDetailsV1FinetuneDetailsGetWithResponse` | `GET /v1/finetune_details` |
| `DeleteFinetuneV1DeleteFinetunePostWithResponse` | `POST /v1/delete_finetune` |

The full generated client also includes every FLUX 2 variant in the spec, fill, expand, fine-tuned ultra, FLUX 3 image klein, video editing and upscaling, outpainting, virtual try-on, erase and deblur. No operation is excluded by tag.

## Submission and polling

`FluxPro11Inputs` is the image request body. Its `Prompt` field is a `*string`; dimensions and seed are `*int`. The response is a union of `AsyncResponse` and `AsyncWebhookResponse`. Polling submissions provide required `Id` and `PollingUrl`; webhook submissions provide `Id`, `Status` and `WebhookUrl`.

Poll with `GetResultV1GetResultGetParams{Id: task.Id}`. Its success response is a union of `SettledCostResultResponse` and `ResultResponse`. `AsResultResponse()` reads the shared fields; `AsSettledCostResultResponse()` also reads `Cost`. The accessors only decode JSON and can succeed on the other branch with missing fields zeroed. Validate the fields your application needs.

`StatusResponsePending`, `StatusResponseReasoning` and `StatusResponseGenerating` mean keep polling. `StatusResponseReady` means output is available. Error, task-not-found, request-moderated, content-moderated and no-card-generated statuses are terminal failures. Reject unknown statuses rather than polling forever.

`Result` is untyped JSON. `Progress`, `Details` and `Preview` can be nil. Numeric values use `float64`. Keyframe tuples are arrays of untyped JSON values; validate their length and number/string positions before submitting.

## Errors and rate limits

The Go error covers transport and JSON decoding failures. API failures are represented by `StatusCode()`, `Body` and any matching typed status field. Submission validation failures decode into `JSON422`. Use a bounded context, delay between polls and backoff on 429. The client has no built-in retry or rate-limit policy. Avoid replaying paid submissions after an uncertain transport result.
