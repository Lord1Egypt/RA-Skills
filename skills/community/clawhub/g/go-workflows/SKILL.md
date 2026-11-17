---
name: "go-workflows"
description: "Build durable Go workflows with psyb0t/go-workflows: connect clients and workers to shared storage, register activities, route queues, use retries, signals and timers, and test recovery. Use when integrating or maintaining this library."
homepage: https://github.com/psyb0t/go-workflows
user-invocable: true
permissions:
  filesystem: "Read the target application's Go source and configuration; edit only the requested integration and tests. Examples write a task-owned SQLite file."
  shell: "Run the target project's dependency and verification commands. This repository uses Docker-backed Make targets."
  network: "Fetch the library and documentation from GitHub and Go module infrastructure. Runtime connections go only to the application's configured database and activity destinations."
metadata:
  author: psyb0t
  openclaw:
    requires:
      bins: [docker, make]
---

# go-workflows

This is an importable Go library, not a separate workflow server. Clients persist requests in a backend; workers connected to that storage claim tasks and record history. A queue is a routing label. The optional diagnostics UI does not coordinate workers.

## Security & safety

- Workflow inputs, activity results, signals and errors become stored history. Keep credentials out of them. Activities use application-owned credentials and approved destinations.
- Activities can run more than once after failure or lease expiry. Make external side effects idempotent with a durable operation key.
- Queues and worker names are not authentication or tenant boundaries. Protect database credentials and isolate unrelated applications. Diagnostics has no built-in authentication; protect the whole mount before exposing it.
- Remove histories or change production schema only when requested. Do not use destructive SQL DOWN migrations to roll back an application binary.

## When to use

Use for durable background jobs, multi-step orchestration, delayed work, external signals, activity retries or workers sharing SQLite, PostgreSQL, MySQL or Redis storage.

## When NOT to use

Do not use it as a hosted API, a drop-in Temporal server, an authorization system or an exactly-once side-effect guarantee. A short request that needs no persisted progress may need only ordinary Go code.

## Integrate

1. Read the target project's build and dependency conventions. Add a published version of `github.com/psyb0t/go-workflows` through that project's dependency target. This repository's `make pkg-add` changes its own dependencies, not a consumer application.
2. Select persistent storage. Use file-backed SQLite on one host; use a network backend for replicas. In-memory SQLite is for disposable examples. Read [references/usage.md](references/usage.md) for constructors, ownership and examples.
3. Define workflow functions with `workflow.Context` and activities with ordinary Go code. Register every definition before starting workers. Producers and consumers must agree on registered names and serialization.
4. Connect client and worker to the same backend namespace and queues. `worker.Start(ctx)` already starts background polling. Give simultaneous replicas distinct worker names; do not enable `SingleWorkerMode` for replicas.
5. Keep workflow execution deterministic. Use workflow timers, channels and concurrency instead of native time, goroutines or I/O. External work belongs in activities. Use replay-aware `workflow.Logger(ctx)`.
6. Submit with `client.CreateWorkflowInstance` and wait with `client.GetWorkflowResult[T]` when needed. A client timeout does not cancel the workflow. Use the client cancellation operation explicitly.
7. On shutdown, cancel the worker context, call `WaitForCompletion`, then close storage owned by the application. Caller-owned pools stay open until their owner closes them.

## Choose features

Read [references/usage.md](references/usage.md) for queue routing, activity retries, subworkflows, signals, durable timers, cancellation, continued executions, diagnostics and testing. It links the maintained feature examples and public documentation.

## Verify

Run the consumer's tests through its existing build system. Check one completed result and its persisted history, intended queue routing, error handling and shutdown. For durable work, also test restart recovery and duplicate activity delivery.

When changing this repository, use `make format lint build`, `make test-coverage`, `make sec` and `make generate`. Tests use `-race`; the coverage floor is 90%. See the repository's local `AGENTS.md` for development rules. Report observed results and any checks that could not run.
