# go-roark: setup and reference

This module is unofficial and not affiliated with Roark.

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- A Roark bearer credential exported as `ROARK_API_KEY`.

## Install

```bash
go get github.com/psyb0t/go-roark
```

## Base URL and authentication

The production base URL is `https://api.roark.ai`. Add `roark.WithRequestEditorFn` when creating the client and set `req.Header.Set("Authorization", "Bearer "+os.Getenv("ROARK_API_KEY"))` in the editor. The complete example is in [../SKILL.md](../SKILL.md).

A project-scoped key returns its one bound project. A user-scoped credential can list available projects with `GetV1ProjectsWithResponse`, then select one with `req.Header.Set("X-Roark-Project-Id", projectID)` in the same editor. Read the projects from `res.JSON200.Data.Projects` after checking `JSON200`. `GetV1MeWithResponse` describes credential scope and permissions.

## Client

- `roark.NewClientWithResponses(server, opts...)` constructs the parsed-response client. Options include `roark.WithRequestEditorFn`, `roark.WithHTTPClient` for a custom HTTP client with timeouts, and `roark.WithBaseURL`.
- Each operation has `Client.X` returning a raw `*http.Response`, `ClientWithResponses.XWithResponse` returning a parsed response, and `NewXRequest` to build a request.
- Operations with a body also expose `XWithBodyWithResponse`, accepting a content type and raw `io.Reader`.
- Generated methods for UUID path parameters use `github.com/oapi-codegen/runtime/types.UUID`. Check each signature before passing an ID.

## Main operations

| Method | Endpoint |
| --- | --- |
| `GetV1MeWithResponse` | `GET /v1/me` |
| `GetV1ProjectsWithResponse` | `GET /v1/projects` |
| `GetV1AgentWithResponse` | `GET /v1/agent` |
| `GetV1CallWithResponse` | `GET /v1/call` |
| `GetV1CallByCallIdTranscriptWithResponse` | `GET /v1/call/{callId}/transcript` |
| `GetV1ChatWithResponse` | `GET /v1/chat` |
| `GetV1PersonaWithResponse` | `GET /v1/persona` |
| `PostV1SimulationRunWithResponse` | `POST /v1/simulation/run` |
| `GetV1SimulationJobByJobIdWithResponse` | `GET /v1/simulation/job/{jobId}` |
| `GetV1SimulationPlanWithResponse` | `GET /v1/simulation/plan` |
| `GetV1MetricDefinitionsWithResponse` | `GET /v1/metric/definitions` |
| `GetV1MetricCollectionJobsWithResponse` | `GET /v1/metric/collection-jobs` |
| `GetV1UsageWithResponse` | `GET /v1/usage` |

All 160 source operations are generated, including writes for agents, prompts, plans, environments, personas, metrics, flows, webhooks, managed configuration and organization projects. Use `client.gen.go` for the full list and exact body types. Operation IDs with hyphens are normalized to Go identifiers.

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200`, `JSON201` | The decoded success body for that status, nil otherwise |
| `JSON401`, other declared status fields | The decoded API error body for that status |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | The raw response and status |

A nil transport error does not prove API success. Check the expected status field before reading its data. Number fields are `float64`. Optional and nullable fields may be pointers; check for nil before dereferencing. Union schemas may have generated accessor methods rather than direct fields.

## Pagination

List operations such as calls, agents, personas, metric definitions and simulation plans accept `Limit` and `After` in their generated params type. Read `JSON200.Pagination.HasMore` and `NextCursor`; pass the cursor as `After` for the next page. Stop when `HasMore` is false or the cursor is nil. Endpoint limits differ: calls allow up to 100, agents and plans up to 50, metric definitions up to 500. Use the limit documented on the specific generated params type.

## Simulation and metric jobs

`PostV1SimulationRunWithResponse` starts a run from a template, inline plan or saved plan ID. `GetV1SimulationJobByJobIdWithResponse` reads an individual simulation job. Creating a simulation plan saves a reusable definition; it does not start a simulation.

Creating a metric collection job starts processing. Supply exactly one of call IDs or chat IDs. A successful HTTP response to a job creation request does not mean the job has finished; inspect its status with the matching read operation.

## Rate limits

Some operations declare HTTP 429 responses. Handle rate limits with bounded backoff instead of retrying in a tight loop. The generated client adds no automatic retries, pagination or job polling.
