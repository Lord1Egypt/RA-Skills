# go-render-api: setup and reference

## Requirements

- Go 1.26.11 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.
- A Render API key, created under Account Settings in the Render Dashboard.

## Install

```bash
go get github.com/psyb0t/go-render-api
```

The package name is `render`. The module path ends in `go-render-api`, so import it with an explicit name:

```go
import render "github.com/psyb0t/go-render-api"
```

## Auth

Render takes `Authorization: Bearer <api key>`. Add the header with a `RequestEditorFn`: for every request through `render.WithRequestEditorFn`, or for one call through the trailing `reqEditors` argument of that method.

## Client options

| Option | Effect |
|---|---|
| `render.WithRequestEditorFn(fn)` | Runs `fn` on every request, used for the auth header. |
| `render.WithHTTPClient(doer)` | Replaces `http.DefaultClient`, for timeouts or transport settings. |
| `render.WithBaseURL(url)` | Overrides the server passed to the constructor. |

Base URL: `https://api.render.com/v1`.

## Calling operations

Each operation `X` in the spec has:

- `client.XWithResponse(ctx, pathParams..., params, ...)` returning `*XResponse`.
- For operations with a JSON body, `client.XWithResponse(ctx, pathParams..., body)` takes the typed `XJSONRequestBody`, and `client.XWithBodyWithResponse(ctx, pathParams..., contentType, io.Reader)` takes raw bytes.

Some operations, by name in `client.gen.go`:

| Method | Endpoint |
|---|---|
| `ListServicesWithResponse(ctx, *ListServicesParams)` | `GET /services` |
| `RetrieveServiceWithResponse(ctx, serviceId)` | `GET /services/{serviceId}` |
| `ListDeploysWithResponse(ctx, serviceId, *ListDeploysParams)` | `GET /services/{serviceId}/deploys` |
| `CreateDeployWithResponse(ctx, serviceId, CreateDeployJSONRequestBody)` | `POST /services/{serviceId}/deploys` |
| `SuspendServiceWithResponse(ctx, serviceId)` | suspends a service |
| `DeleteServiceWithResponse(ctx, serviceId)` | deletes a service |

Search `client.gen.go` for `WithResponse(` to find the rest. Do not guess a method name.

Path IDs such as `ServiceIdParam` are plain `string` aliases.

## Paging

List endpoints return a slice of wrappers, each with the item and its `Cursor`, for example `ServiceList = []ServiceWithCursor`. Set `Limit` (`LimitParam`, an `int`) and pass the last item's cursor as `Cursor` (`CursorParam`, a `string`) in the next call's params to read the next page. Render's [pagination docs](https://api-docs.render.com/reference/pagination) have the details.

## Responses

Every `XResponse` has:

- `Body []byte` and `HTTPResponse *http.Response`.
- `StatusCode()` and `Status()`.
- One `JSONnnn` field per documented status, set only when the response had that status. Error statuses (`JSON401`, `JSON404`, `JSON429`, `JSON500` and so on) are aliases of `render.Error`, with optional `Message`, `Code` and `Id`.

A method returns a non-nil error only for transport failures and bodies that do not decode.

## Regenerating

`client.gen.go` is generated. For changes to the client itself, see `AGENTS.md` in the repository.
