---
name: go-bfl
description: Writes Go code with go-bfl (package bfl, github.com/psyb0t/go-bfl), an unofficial generated client for the Black Forest Labs FLUX API. Use when a Go program submits FLUX image or video generation tasks, polls task results, calls the image and video tools, reads credits or manages fine-tunes.
license: MIT
homepage: https://github.com/psyb0t/go-bfl
user-invocable: true
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins:
        - go
permissions:
  filesystem: "Guides edits to Go source. The client reads and writes no files."
  shell: "The Go toolchain to add and compile the dependency."
  network: "Module proxy for installation. At runtime, HTTPS to api.bfl.ai or a validated provider polling host."
---

# go-bfl

Unofficial, typed Go client for the Black Forest Labs FLUX API. Package `bfl` lives at the module root. Read [references/setup.md](references/setup.md) for constructors, operation names and response handling.

## Security & safety

- Load `BFL_API_KEY` from the environment. Send it in `x-key` through `bfl.WithRequestEditorFn`. Never log the key, task IDs or signed output URLs.
- Use `https://api.bfl.ai`. Validate HTTPS and an approved provider host before following a returned `polling_url`; never send the key to an arbitrary URL.
- Submissions spend credits. Delete-finetune changes account state. Call these only for the user's requested action. Do not retry a paid submission blindly.

## When to use

Use for Go code that submits FLUX image or video tasks, uses FLUX tools, polls task status, reads credits or manages fine-tunes. This module is unofficial. For changing the generated client, read the repository's `AGENTS.md`.

## Finding endpoints and types

The examples below cover a few calls. Every operation in the spec has a generated method, and the spec's descriptions are on them as Go doc comments. Look names and fields up instead of guessing. After `go get github.com/psyb0t/go-bfl`, from inside your module:

```bash
go doc github.com/psyb0t/go-bfl ClientWithResponsesInterface    # every endpoint method
go doc github.com/psyb0t/go-bfl GetResultV1GetResultGetParams   # one method, params type or model
go doc -all github.com/psyb0t/go-bfl                            # the whole package
```

The same documentation is at https://pkg.go.dev/github.com/psyb0t/go-bfl.

Method names come from the spec's operation IDs, which include the path and HTTP method (`FluxPro11V1FluxPro11Post`). `<OperationId>WithResponse` takes the context, then the path parameters in order, then `*<OperationId>Params` when the operation has query or header parameters, then the request body when it has one. The `JSON200` field (or `JSON422` and so on, per declared status) holds the decoded body; it is nil for any other status. Submission and result bodies are unions, decoded with the `As...` accessors described below.

## Usage

Follow the compiled submit-then-poll example in the root `example_test.go`, also shown in `README.md`. Construct `bfl.NewClientWithResponses` with the base URL, a request editor setting `x-key`, and a bounded HTTP client.

1. Submit with `FluxPro11V1FluxPro11PostWithResponse(ctx, bfl.FluxPro11Inputs{Prompt: &prompt})`.
2. Check the Go error and `JSON200`, then call `AsAsyncResponse()`. Verify `Id` and `PollingUrl` are nonempty. Webhook submissions use `AsAsyncWebhookResponse()` instead.
3. Poll with `GetResultV1GetResultGetWithResponse(ctx, &bfl.GetResultV1GetResultGetParams{Id: task.Id})`. Use a bounded context and a timer between requests.
4. Decode with `AsResultResponse()` or `AsSettledCostResultResponse()` when the settled cost is needed. Continue for `Pending`, `Reasoning`, `Generating`. Consume `Result` on `Ready`. Treat every other status as terminal or unknown.
5. Inspect untyped result JSON before using any media URL. The client does not download media.

HTTP status failures are responses, usually with nil `JSON200`, rather than Go errors. Inspect `StatusCode()` and `Body`. Union accessors do not validate required fields. Nullable fields are pointers; check them before dereferencing. Costs, credits and progress use `float64`. Keyframe tuples use untyped array elements and need caller validation.
