# go-xai: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- An xAI API key, created in the xAI console.

## Install

```bash
go get github.com/psyb0t/go-xai
```

The package name is `xai`.

## Client

- `xai.NewClientWithResponses(server string, opts ...ClientOption)` returns a client whose methods decode responses. `xai.NewClient` returns the plain client, whose methods return `*http.Response` with the body unread.
- The spec lists no server, so always pass `https://api.x.ai`.
- `xai.WithRequestEditorFn` runs on every request; set the `Authorization: Bearer <key>` header there. `xai.WithHTTPClient` swaps in your own `*http.Client` (timeouts, proxies).
- Every method also takes per-call `reqEditors ...RequestEditorFn`.

## Methods

Names come from the spec's operation IDs. Each has a `...WithResponse` form, and endpoints with a JSON body also have `...WithBodyWithResponse` for a raw `io.Reader` body.

| Endpoint | Method |
|---|---|
| `GET /v1/api-key` | `HandleGetApiKeyInfoRequest` |
| `GET /v1/me` | `HandleGetMeRequest` |
| `GET /v1/models`, `/v1/models/{model_id}` | `HandleModelsListRequest`, `HandleModelGetRequest` |
| `GET /v1/language-models`, `/v1/language-models/{model_id}` | `HandleLanguageModelsListRequest`, `HandleLanguageModelGetRequest` |
| `POST /v1/chat/completions` | `HandleGenericCompletionRequest` |
| `GET /v1/chat/deferred-completion/{request_id}` | `HandleGetDeferredCompletionRequest` |
| `POST /v1/responses` | `HandleGenericModelRequest` |
| `GET` / `DELETE /v1/responses/{response_id}` | `HandleGetStoredCompletionRequest`, `HandleDeleteStoredCompletionRequest` |
| `POST /v1/messages` | `HandleGenericMessagesRequest` |
| `POST /v1/embeddings` | `HandleEmbeddingRequest` |
| `POST /v1/tokenize-text` | `HandleTokenizeTextRequest` |
| `POST /v1/images/generations` | `HandleGenerateImageRequest` |
| `POST /v1/videos/generations` | `HandleGenerateVideoRequest` |
| `GET /v1/videos/{request_id}` | `HandleGetDeferredVideoRequest` |
| `GET` / `POST /v1/files` | `HandleListFilesRequest`, `HandleUploadFileRequest` |
| `DELETE /v1/files/{file_id}` | `HandleDeleteFileRequest` |
| `GET` / `POST /v1/skills` | `HandleListSkillsRequest`, `HandleUploadSkillRequest` |
| `POST /v1/documents/search` | `HandleDocumentSearchRequestV2` |

The table is a selection. `go doc github.com/psyb0t/go-xai ClientWithResponsesInterface` lists every method; the spec also has completions, image and video edits, file content and public URLs, model lists per modality and more.

## Responses

Each `...WithResponse` method returns a struct with `Body []byte`, `HTTPResponse *http.Response`, `StatusCode()` and `JSON200`, the decoded 200 body. The spec documents only 200 bodies, so for any other status `JSON200` is nil and the error text is in `Body`.

## Union types

Schemas with `oneOf` become structs with `From<Variant>`, `As<Variant>` and `Merge<Variant>` methods. In chat requests:

- `Message`: `Message0` system, `Message1` developer, `Message2` user, `Message3` assistant, and the tool and function variants after that.
- `Content`: `Content0` is a string, `Content1` is a list of `ContentPart` for images and other parts.

## Errors

- A non-nil `err` from a method is a transport or decode error.
- A nil `err` with `JSON200 == nil` means the API answered with a non-200 status; report `StatusCode()` and `Body`.
