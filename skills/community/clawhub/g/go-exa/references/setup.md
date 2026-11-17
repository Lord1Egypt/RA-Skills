# go-exa: setup and reference

This module is unofficial and not affiliated with Exa.

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- An Exa API key from the [dashboard](https://dashboard.exa.ai), exported as `EXA_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-exa
```

The module path ends in `go-exa` and the package is `exa`, so import it with an explicit name:

```go
import exa "github.com/psyb0t/go-exa"
```

## Auth

Send the key as `x-api-key` from a request editor, either for every call with `exa.WithRequestEditorFn` on the constructor or per call as the last argument. The spec also accepts `Authorization: Bearer <key>`. The generated client sets neither on its own.

## Client

- `exa.NewClientWithResponses("https://api.exa.ai", opts...)`. Options: `exa.WithRequestEditorFn`, `exa.WithHTTPClient` (your own `*http.Client`, for timeouts), `exa.WithBaseURL`.
- Each operation has `Client.X` (raw `*http.Response`), `ClientWithResponses.XWithResponse` (parsed) and `NewXRequest` (request only). Operations with a body also have `XWithBodyWithResponse` taking a raw `io.Reader`.

## Operations

| Method | Endpoint | Body or params | `JSON200` |
|---|---|---|---|
| `SearchWithResponse` | `POST /search` | `SearchJSONRequestBody` (`Query` required) | `*SearchResponse`, a results or synthesis union |
| `FindSimilarWithResponse` | `POST /findSimilar` | `FindSimilarJSONRequestBody` (`Url` required) | `*FindSimilarResponse` |
| `GetContentsWithResponse` | `POST /contents` | `GetContentsJSONRequestBody` (`Urls` required) | `*ContentsResponse` |
| `AnswerWithResponse` | `POST /answer` | `AnswerJSONRequestBody` (`Query` required) | `*AnswerResponse` |
| `CreateAgentRunWithResponse` | `POST /agent/runs` | `*CreateAgentRunParams`, `CreateAgentRunJSONRequestBody` | Check the declared success fields in `CreateAgentRunResponse` |
| `ListAgentRunsWithResponse` | `GET /agent/runs` | `*ListAgentRunsParams` (`Cursor`, `Limit`) | `*AgentRunList` |
| `GetAgentRunWithResponse` | `GET /agent/runs/{id}` | run ID | `*AgentRun` |

Search options on `SearchJSONRequestBody` include `NumResults`, `Category`, `IncludeDomains`, `ExcludeDomains`, publication and crawl date bounds, `Contents`, `Type` and `UserLocation`. Some options are unions; inspect the generated field type and its `From...` helpers rather than assigning older enum types. `Contents` uses `*ContentsRequest` to request text, highlights or summaries. The current specification removes the earlier research task API; use the agent run methods above.

## Responses

| Field or method | Holds |
|---|---|
| `JSON200`, `JSON201` and other declared status fields | The decoded body for that status, nil otherwise |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response |

- `SearchResponse` is a union. Call `AsSearchResultsResponse()` for ordinary results or `AsSearchSynthesisResponse()` for synthesis output. `SearchResultsResponse.Results` is `[]SearchResultOutput`, with required `Url`, `Title` and `Id` strings and optional content fields. `CostDollars` uses `CostDollarsOutput`.
- Some fields are unions, a JSON value that can be one of several shapes. Read them with the generated `As...` methods: `AnswerResponse.Answer.AsAnswerResponseAnswer0()` gives the answer as a string, `AsAnswerResponseAnswer1()` gives the structured answer when the request set `OutputSchema`. Set a union field on a request with the matching `From...` method.
- Wrappers that share a name with a schema get a `2` suffix: `SearchResponse2`, `AnswerResponse2`, `FindSimilarResponse2`.
