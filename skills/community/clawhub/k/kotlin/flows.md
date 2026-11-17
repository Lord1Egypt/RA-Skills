# Flows — Cold Streams, Hot State, And Lost Events

Three questions decide every Flow design: cold or hot, what happens with no subscriber, and what happens when the consumer is slower than the producer. Get those wrong and the failure is silence — no exception, just missing updates.

## Symptom → Cause

| Symptom | Cause | Fix |
|---|---|---|
| Collector never runs | The flow is cold and nothing collects it, or the upstream never emits | Collect it; check the producer with a `.onEach { log() }` before the operator chain |
| UI stops updating after a while | A new state `equals` the old one — `StateFlow` conflates (SKILL.md rule 6) | Emit a new immutable value; never mutate and re-assign the same instance |
| Events (navigation, toast) sometimes lost | `SharedFlow(replay = 0)` with no subscriber at emit time | `Channel` + `receiveAsFlow`, or an acknowledged state field |
| Event fires twice after rotation | `replay = 1` on an event stream, re-delivered to the new subscriber | Drop replay; use a consume-once carrier |
| Network call runs several times | Multiple collectors on a cold flow, each starting its own upstream | `shareIn`/`stateIn` with the right `SharingStarted` |
| Upstream keeps running in the background | `SharingStarted.Eagerly`/`Lazily`, or collection not tied to a lifecycle | `WhileSubscribed(5_000)` plus lifecycle-aware collection |
| Emissions pile up / memory grows | Producer faster than consumer with an unbounded buffer | `conflate`, `buffer(n, onBufferOverflow)`, or `collectLatest` |
| "Flow invariant is violated" exception | Emitting from a different coroutine inside `flow { }` | `channelFlow` + `send`, or emit from the same coroutine |
| Values arrive on the wrong thread | `flowOn` placed after the operator you meant to move | `flowOn` affects only the *upstream* of where it sits |

## Cold vs Hot

| | Cold (`flow {}`, `asFlow()`) | `StateFlow` | `SharedFlow` | `Channel` |
|---|---|---|---|---|
| Runs without collectors | No | N/A (holds a value) | Yes (emissions may be dropped) | Yes (buffers) |
| Initial value | No | Required | Optional via `replay` | No |
| Conflation | No | Always, by `equals` | Only with `onBufferOverflow` | Configurable |
| Multiple collectors | Independent executions | Shared, all see the current value | Shared broadcast | Split: each element goes to one receiver |
| Completes | Yes | Never | Never | On close |
| Use for | Requests, DB queries, transformations | UI/screen state | Broadcast events, analytics | Exactly-once events, work queues |

## Sharing: `shareIn` And `stateIn`

- Both need a scope, and that scope's lifetime is the upstream's lifetime. A ViewModel-owned scope is the usual correct answer.
- `SharingStarted.WhileSubscribed(5_000)` is the Android convention: 5 seconds outlives a configuration change (the old collector detaches and the new one attaches within milliseconds) while still stopping the upstream on a real backgrounding. `stopTimeoutMillis` shorter than a rotation restarts the query on every rotation; `Eagerly` never stops.
- `WhileSubscribed(stopTimeoutMillis = 5_000, replayExpirationMillis = …)` also controls whether a returning subscriber sees stale cached data or waits for fresh.
- `stateIn` requires an initial value and gives you `.value` synchronously; the suspending overload waits for the first upstream emission instead — that one blocks screen rendering until data arrives.
- Do not `stateIn` a flow that must not be conflated (progress ticks, keystroke-by-keystroke input where duplicates matter): equality conflation drops repeats silently.

## Operators That Change Semantics

- `map`, `filter`, `transform` — run in the collector's context unless a `flowOn` sits upstream.
- `flowOn(dispatcher)` — moves everything *above* it; operators below stay on the collector's context. Two `flowOn` calls carve the chain into segments.
- `conflate()` — keep only the latest pending value; the consumer skips intermediate ones. Correct for UI, wrong for events.
- `buffer(capacity, onBufferOverflow)` — decouples producer and consumer speeds. `BufferOverflow.SUSPEND` (default) applies backpressure to the producer; `DROP_OLDEST`/`DROP_LATEST` choose which data to lose, explicitly.
- `collectLatest` / `mapLatest` / `flatMapLatest` — cancel the in-flight block when a new value arrives. The canonical search-as-you-type shape: `debounce(300).distinctUntilChanged().flatMapLatest { query(it) }`.
- `debounce(ms)` waits for a quiet window; `sample(ms)` takes the latest per interval. Debounce for typing, sample for a firehose of sensor or progress data.
- `distinctUntilChanged()` uses `equals` — on a data class with a timestamp field, nothing is ever "unchanged".
- `flatMapMerge(concurrency = n)` for parallel fan-out with a cap; `flatMapConcat` preserves order at the cost of parallelism.
- `onStart`/`onCompletion`/`onEmpty` for loading and empty states; `onCompletion` receives the cancellation cause too, so check `cause == null` before treating it as success.
- `retryWhen { cause, attempt -> attempt < 3 && cause is IOException }` with a delay implements bounded retry; a bare `retry()` retries forever, including on a bug.

## Building Flows

- `flow { emit(x) }` — sequential producer; emissions must come from the block's own coroutine (that is the flow invariant).
- `channelFlow { send(x) }` — when values come from other coroutines or several sources; costs a channel, buys concurrency.
- `callbackFlow { … awaitClose { unregister() } }` — the only correct wrapper for a listener API. Omitting `awaitClose` throws at runtime; unregistering outside it leaks the listener for the flow's whole lifetime.
- `flowOf`, `asFlow()` on collections and ranges for tests and fixtures.
- Cold-flow discipline: a `flow { }` builder should be re-runnable. Anything with side effects (writes, analytics) belongs in the collector or in `onEach`, not in the producer.

## Events Without Losing Them

Ranked by how much you can afford to lose:

1. `Channel(Channel.BUFFERED)` exposed as `receiveAsFlow()` — buffers while nobody collects, each event delivered once. Default for navigation and one-shot UI effects.
2. Event as part of the state (`data class State(val error: ErrorEvent?)`) with an explicit `onErrorShown()` that clears it — survives process death if the state is persisted, costs an extra callback.
3. `MutableSharedFlow(replay = 0, extraBufferCapacity = 1, onBufferOverflow = DROP_OLDEST)` — broadcast to several collectors, and the drop policy is at least written down rather than accidental.

`SharedFlow` with `replay = 0` and default capacity is the accidental data-loss configuration: `tryEmit` returns false and callers rarely check.

## Testing Flows

- Collect into a list on a background coroutine before triggering emissions; asserting on `.value` alone hides intermediate states, and `StateFlow` conflation means "the test saw two states" is not evidence the UI did.
- A `stateIn(WhileSubscribed())` flow emits nothing until something subscribes: a test that only reads `.value` gets the initial value forever.
- `first()` / `take(n).toList()` terminate a hot flow's collection; collecting a `StateFlow` with `toList()` never returns.

## Review Checklist

- Every hot flow states its `SharingStarted` policy and the scope that owns it.
- Every event stream has a documented answer to "what if nobody is collecting".
- Every `callbackFlow` has `awaitClose` with a real unregister.
- Every `buffer`/`conflate` was chosen, not inherited from an example.
- No side effect inside a cold flow's producer block.
