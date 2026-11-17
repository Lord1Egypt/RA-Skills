---
name: go-bunnynet
description: Writes Go code with go-bunnynet (package bunnynet, github.com/psyb0t/go-bunnynet), an unofficial generated client for the Bunny.net core API covering CDN pull zones, cache purges, DNS, storage and video library configuration, statistics, load balancers and billing. Use when a Go project imports go-bunnynet or needs Bunny.net core API calls. Excludes storage file transfers and the separate Stream API.
license: MIT
homepage: https://github.com/psyb0t/go-bunnynet
user-invocable: true
metadata:
  openclaw:
    emoji: "🐰"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source in the current project. The library reads and writes no files."
  shell: "The Go toolchain to add and compile the dependency."
  network: "Module downloads use the configured Go proxy. Runtime core API requests use https://api.bunny.net."
---

# go-bunnynet

Unofficial, typed Go client for the Bunny.net core API, in package `bunnynet` at the module root. Read [references/setup.md](references/setup.md) for installation, methods and response handling.

## Security & safety

- Read `BUNNYNET_API_KEY` from the environment and set `AccessKey` through `WithRequestEditorFn`. Never hardcode or log credentials.
- Use `https://api.bunny.net`. Core account keys differ from storage zone passwords and video library keys.
- Creating, changing or deleting resources, purging caches, rotating keys and closing accounts act on the user's account. Call those operations only when requested.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-bunnynet`, from inside your module:

```bash
go doc github.com/psyb0t/go-bunnynet ClientWithResponsesInterface  # every endpoint method
go doc github.com/psyb0t/go-bunnynet PullZonePublicIndexAllParams  # one method, params type or model
go doc -all github.com/psyb0t/go-bunnynet                          # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-bunnynet.

Method names come from the spec's operation IDs with punctuation removed (`PullZonePublic_IndexAll` becomes `PullZonePublicIndexAll`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON201` and so on, per declared status) holds the decoded body; it is nil for any other status and for success responses the spec gives no schema.

## Usage

Use the README example, compiled as `Example` in `example_test.go`. Construct `bunnynet.NewClientWithResponses` with `bunnynet.WithRequestEditorFn`; attach `AccessKey` in the editor. Supply `bunnynet.WithHTTPClient` with a timeout when needed.

`PullZonePublicIndexAllWithResponse(ctx, nil)` lists pull zones. `PullZonePublicIndexWithResponse(ctx, id, nil)` fetches one. Operation IDs determine method names, with punctuation removed.

Check the Go error, HTTP status and decoded field separately. API errors can return a nil Go error. Optional fields are pointers. Success responses with no schema expose status and raw body only.

Pull-zone listing declares an array but describes an object when `page > 0`. Leave `Page` unset for typed decoding or use raw `PullZonePublicIndexAll` and decode the paginated body. There are no automatic retries or pagination.

For changes to the generated client, read `AGENTS.md` and regenerate from the spec.
