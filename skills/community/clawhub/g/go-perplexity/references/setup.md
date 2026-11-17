# go-perplexity: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Perplexity API key, created in the API settings of a Perplexity account.

## Install

```bash
go get github.com/psyb0t/go-perplexity
```

The package name is `perplexity`.

## Client

- `perplexity.NewClientWithResponses(server string, opts ...ClientOption)` returns a client whose methods decode responses. `perplexity.NewClient` returns the plain client, whose methods return `*http.Response` with the body unread.
- The base URL is `https://api.perplexity.ai`.
- `perplexity.WithRequestEditorFn` runs on every request; set the `Authorization: Bearer <key>` header there. `perplexity.WithHTTPClient` swaps in your own `*http.Client` (timeouts, proxies).
- Every method also takes per-call `reqEditors ...RequestEditorFn`.

## Methods

Names come from the spec's operation IDs. Each has a `...WithResponse` form, and endpoints with a body also have `...WithBodyWithResponse` for a raw `io.Reader` body.

| Endpoint | Method |
|---|---|
| `POST /v1/sonar` | `ChatCompletionsChatCompletionsPost` |
| `POST` / `GET /v1/async/sonar` | `CreateAsyncChatCompletionsAsyncChatCompletionsPost`, `ListAsyncChatCompletionsAsyncChatCompletionsGet` |
| `GET /v1/async/sonar/{api_request}` | `GetAsyncChatCompletionResponseAsyncChatCompletionsApiRequestGet` |
| `POST /search` | `SearchSearchPost` |
| `POST /v1/embeddings` | `EmbeddingsV1EmbeddingsPost` |
| `POST /v1/contextualizedembeddings` | `ContextualizedEmbeddingsV1ContextualizedembeddingsPost` |
| `GET /v1/models` | `ListModels` (response type `ListModelsResponse2`) |
| `POST /v1/agent`, `GET /v1/agent/{id}` | `CreateAgent`, `RetrieveAgent` |
| `POST /v1/agent/{id}/cancel` | `CancelAgentResponse` |
| `GET /v1/agent/{id}/files`, `.../files/{file_id}/content` | `ListAgentFiles`, `DownloadAgentFile` |
| `GET /v1/skills`, `/v1/skills/{skill_id}` | `ListSkills`, `GetSkill` |
| `POST /v1/skills`, `PUT /v1/skills/{skill_id}` | `CreateSkillWithBody`, `UpdateSkillWithBody` (raw body only) |
| `DELETE /v1/skills/{skill_id}` | `DeleteSkill` |
| `POST /v1/decisions` | `DecisionsV1DecisionsPost` |
| `GET /v1/analytics/computer/usage`, `/v2/...` | `GetComputerUsageAnalytics`, `GetComputerUsageAnalyticsV2` |

The full list is in `client.gen.go` under `ClientWithResponsesInterface`.

## Responses

Each `...WithResponse` method returns a struct with `Body []byte`, `HTTPResponse *http.Response`, `StatusCode()` and a `JSON<status>` field per status the spec documents with a JSON body, for example `JSON200` and `JSON422` (`*HTTPValidationError`) on the Sonar endpoint. Fields for other statuses stay nil; `Body` always holds the raw response.

## Union types

Schemas with `oneOf` become structs with `From<Variant>`, `As<Variant>` and `Merge<Variant>` methods:

- `ChatMessageInput_Content`: `ChatMessageInputContent0` is a string, `ChatMessageInputContent1` a list of content parts.
- `ChatMessageOutput_Content`: read text with `AsChatMessageOutputContent0`.
- `ApiSearchRequest_Query`: `ApiSearchRequestQuery0` is one query string, `ApiSearchRequestQuery1` a list of queries.

## Errors

- A non-nil `err` from a method is a transport or decode error.
- A nil `err` with `JSON200 == nil` means the API answered with another status; check the matching `JSON<status>` field or report `StatusCode()` and `Body`.
