# Integration reference

## Runnable examples

From a clone of [go-workflows](https://github.com/psyb0t/go-workflows):

```bash
make run-greeting
make run
```

The first is an in-memory client and worker. The second persists activity history in `quickstart.sqlite` and returns `42`. Docker, Make and Git are host requirements; the repository supplies its Go toolchain in the development image. Both complete programs are in the [README](https://github.com/psyb0t/go-workflows#use-it-in-an-application) and have executable tests.

For an existing application, import these packages after adding a published module version through its dependency tooling:

```go
import (
    "github.com/psyb0t/go-workflows/backend/sqlite"
    "github.com/psyb0t/go-workflows/client"
    "github.com/psyb0t/go-workflows/worker"
    "github.com/psyb0t/go-workflows/workflow"
)
```

Do not copy the repository's development Makefile into the consumer or require a separate workflow service.

## Storage, workers and clients

`sqlite.NewSqliteBackend(path)` owns a persistent file-backed pool and applies migrations by default. `NewInMemoryBackend` is disposable. `NewSqliteBackendWithDB` borrows a configured pool and leaves ownership with the caller. Network backends provide corresponding owned and borrowed constructors with their own migration options. Read [backend operations](https://github.com/psyb0t/go-workflows/blob/main/docs/backends.md) before enabling migrations on a shared pool.

`worker.New(backend, options)` starts both workflow and activity roles when `Start(ctx)` is called. `RegisterWorkflow` and `RegisterActivity` must succeed first. A separate client process needs the same storage namespace and compatible registered names, not a network connection to the worker. `registry.WithName` sets explicit names.

`client.New(backend)` creates the client. Submit through `CreateWorkflowInstance(ctx, client.WorkflowInstanceOptions{InstanceID: id}, workflowFunction, args...)`. Read a typed result through `client.GetWorkflowResult[T](ctx, client, instance, timeout)`. Use a stable, application-defined instance ID when another process needs to address that workflow.

Read [architecture and workers](https://github.com/psyb0t/go-workflows/blob/main/docs/architecture.md) for pollers, concurrency, leases, identities and shutdown.

## Feature map

| Need | API and constraints | Example |
| --- | --- | --- |
| External work | `workflow.ExecuteActivity[T](ctx, options, activity, args...).Get(ctx)`; effects must tolerate repeat attempts | [quickstart](https://github.com/psyb0t/go-workflows/tree/main/samples/quickstart) |
| Retries | Set `ActivityOptions.RetryOptions`; use `workflow.NewPermanentError` for non-retryable failures | [retries](https://github.com/psyb0t/go-workflows/tree/main/samples/retries) |
| Queue routing | `WorkflowInstanceOptions.Queue`, `ActivityOptions.Queue`, worker `WorkflowQueues` and `ActivityQueues`; an activity inherits the workflow queue by default | [queues](https://github.com/psyb0t/go-workflows/tree/main/samples/queues) |
| Split processes | `worker.NewWorkflowWorker` and `worker.NewActivityWorker`; share backend storage and compatible definitions | [split worker](https://github.com/psyb0t/go-workflows/tree/main/samples/simple-split-worker) |
| Child workflows | `workflow.CreateSubWorkflowInstance[T]`; register the child definition too | [subworkflow](https://github.com/psyb0t/go-workflows/tree/main/samples/subworkflow) |
| External events | Client `SignalWorkflow`, workflow `NewSignalChannel[T]`; keep payloads serializable | [signal](https://github.com/psyb0t/go-workflows/tree/main/samples/signal) |
| Durable waits | `workflow.ScheduleTimer` or `workflow.Sleep`, not `time.Sleep` | [timer](https://github.com/psyb0t/go-workflows/tree/main/samples/timer) |
| Cancellation | Cancel through the client; waiting workflows must select on `ctx.Done()` where interruption is required | [cancellation](https://github.com/psyb0t/go-workflows/tree/main/samples/cancellation) |
| Concurrency | `workflow.Go`, workflow channels, `Select` or workflow errgroup, not native goroutines in replayed code | [concurrent](https://github.com/psyb0t/go-workflows/tree/main/samples/concurrent) |
| Bound history growth | `ContinueAsNew` starts another execution with new arguments; it does not make incompatible definitions replay-safe | [continue as new](https://github.com/psyb0t/go-workflows/tree/main/samples/continue-as-new) |
| Logging and tracing | `workflow.Logger(ctx)` in workflows, `activity.Logger(ctx)` in activities; `ctxscope` metadata propagation | [context propagation](https://github.com/psyb0t/go-workflows/tree/main/samples/context-propagation) |
| Diagnostics | `diag.NewServeMux(backend)` mounts a read-only UI and JSON API; the host owns authentication and HTTP lifecycle | [web](https://github.com/psyb0t/go-workflows/tree/main/samples/web) |

Read the [workflow guide](https://github.com/psyb0t/go-workflows/blob/main/docs/guide.md) before changing replayed definitions. Keep compatible old definitions available for active instances; use new registered names for incompatible changes.

## Tests and repository development

`tester.NewWorkflowTester[T]` tests workflows with virtual time and activity expectations. `activitytester` supplies activity context. These do not prove database claims, migrations or crash recovery; use real backend integration tests for those boundaries.

Repository targets include `make test-sqlite`, `make test-postgres`, `make test-mysql`, `make test-redis`, `make test-recovery` and `make test-coverage`. Required infrastructure starts through testcontainers, not a shared Compose stack. All normal tests use `-race`.

SQL backends have package-local `db/models`, `db/repositories` and embedded migrations. Edit models or `cmd/repogen` query interfaces, then run `make generate`. Use generated repositories for ordinary CRUD and clauses; custom queriers cover joins and correlated queries. Never hand-edit generated code or a published migration.
