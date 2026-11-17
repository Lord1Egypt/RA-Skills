---
name: go-calcom
description: Writes Go code with go-calcom (package calcom, github.com/psyb0t/go-calcom), an unofficial client for Cal.com API v2 generated with oapi-codegen from the public OpenAPI document, with typed methods for bookings, event types, available slots, schedules, calendars, teams, webhooks and profile. Use when Go code needs Cal.com scheduling operations or already imports go-calcom.
license: MIT
homepage: https://github.com/psyb0t/go-calcom
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The client reads and writes no files."
  shell: "The Go toolchain to install and compile the dependency."
  network: "go get fetches the module through the configured Go proxy. Runtime calls send scheduling data over HTTPS to api.cal.com or an explicitly configured Cal.com deployment."
---

# go-calcom

Unofficial, typed Go client for Cal.com API v2, in package `calcom` at the module root.

For install, operation names, headers and pagination, see [references/setup.md](references/setup.md).

## Security & safety

- Use Bearer auth from `CALCOM_API_KEY`. Never hardcode, commit or log credentials or request headers.
- Pass `https://api.cal.com` as the server, or another deployment only when explicitly configured. Generated paths already contain `/v2`.
- Creating, rescheduling or cancelling bookings and editing schedules, event types, teams or webhooks changes account data. Perform those operations only when requested and only for the intended resources.

## When to use

- Go code needs to inspect availability, bookings, event types, schedules, calendars or profile.
- Go code needs to manage Cal.com scheduling resources at the user's request.
- The project already imports `github.com/psyb0t/go-calcom`.

## When NOT to use

- The code is not Go. This module ships only a Go package.
- You need a client maintained by Cal.com. This client is unofficial.
- You want to change generated code. Read `AGENTS.md` in the repository.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-calcom`, from inside your module:

```bash
go doc github.com/psyb0t/go-calcom ClientWithResponsesInterface                 # every endpoint method
go doc github.com/psyb0t/go-calcom BookingsController20240813GetBookingsParams  # one method, params type or model
go doc -all github.com/psyb0t/go-calcom                                         # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-calcom.

Method names come from the spec's operation IDs, which include controller names and endpoint versions (`BookingsController20240813GetBookings`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `Authorization` and `CalApiVersion` headers are fields of that params struct. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status.

## Usage

```go
import (
    "context"
    "net/http"
    "os"

    "github.com/psyb0t/go-calcom"
)

token := "Bearer " + os.Getenv("CALCOM_API_KEY")
auth := calcom.WithRequestEditorFn(
    func(_ context.Context, req *http.Request) error {
        req.Header.Set("Authorization", token)
        return nil
    },
)
client, err := calcom.NewClientWithResponses("https://api.cal.com", auth)
if err != nil {
    panic(err)
}
res, err := client.MeControllerGetMeWithResponse(
    context.Background(),
    &calcom.MeControllerGetMeParams{Authorization: token},
)
if err != nil {
    panic(err)
}
if res.StatusCode() != http.StatusOK || res.JSON200 == nil {
    panic(res.Status())
}
_ = res.JSON200.Data.Username
```

Auth is represented by operation header parameters in the source spec. Populate required `Authorization` fields even when a request editor sets the final header. Many operations also require `CalApiVersion`; use the endpoint's documented version, not a single global version. `/v2/me` has no version header in the spec.

The error return covers transport and decoding failures. For API errors, inspect `StatusCode()` and `Body`; parsed success fields can be nil. Optional and nullable model fields can be pointers. Number fields are `float64`.

Method names follow the source operation IDs, including controller names and endpoint versions. The source document is titled `Cal.diy API v2`, spec version `1.0.0`. It defines the generated coverage; check the online docs before assuming it includes every hosted API operation.
