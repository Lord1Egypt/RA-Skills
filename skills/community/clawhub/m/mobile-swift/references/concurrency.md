# Swift concurrency reference

Load this when writing `async` code, actors, `Sendable` types, or bridging callback and delegate APIs.
Assumes Swift 6 language mode with complete data-race checking.

## Isolation map

| Kind of code | Isolation | Why |
|---|---|---|
| View models, routers, anything SwiftUI reads | `@MainActor final class` | UI reads and writes happen on main |
| Shared mutable state (caches, connection registry, token store) | `actor` | Serialised access without locks |
| Plain data, DTOs, parsers, pure functions | `nonisolated` value types | Usable from any isolation |
| Legacy class that must be shared and cannot be an actor | `final class` + `Mutex` (iOS 18+) | Synchronous access with a real lock |

Check the project's default actor isolation before adding annotations. Since Swift 6.2 a module can
default to `@MainActor` (Xcode build setting "Default Actor Isolation", or
`.defaultIsolation(MainActor.self)` in `Package.swift`). In such a module, mark parsers, DTOs and
background services `nonisolated` explicitly.

## async let vs task groups

- `async let`: a fixed, small number of child tasks known at compile time.
- `withThrowingTaskGroup`: a dynamic number of children, results collected in completion order.
- `withDiscardingTaskGroup` / `withThrowingDiscardingTaskGroup`: many children whose results are not needed.

```swift
// Collect results keyed by input, completion order does not matter
let readings = try await withThrowingTaskGroup(of: (Device.ID, Reading).self) { group in
    for id in ids {
        group.addTask { (id, try await api.latestReading(for: id)) }
    }
    var result: [Device.ID: Reading] = [:]
    for try await (id, reading) in group { result[id] = reading }
    return result
}
```

Bound the width when the input can be large, so 500 inputs do not open 500 connections:

```swift
func uploadAll(_ files: [URL], maxConcurrent: Int = 4) async throws {
    try await withThrowingTaskGroup(of: Void.self) { group in
        var pending = files.makeIterator()
        for _ in 0..<maxConcurrent {
            guard let file = pending.next() else { break }
            group.addTask { try await upload(file) }
        }
        while try await group.next() != nil {
            if let file = pending.next() {
                group.addTask { try await upload(file) }
            }
        }
    }
}
```

- When one child throws, the group cancels the remaining children and rethrows.
- Never let a child task escape the group closure.

## Actors and reentrancy

Every `await` inside an actor is a suspension point where other callers can run. Rules:

- Read state, mutate it, then suspend. Not read, suspend, mutate.
- Re-check invariants after each `await`.
- Deduplicate concurrent requests by caching the in-flight `Task`, not only the result.

```swift
actor FirmwareCatalog {
    private var inFlight: [String: Task<Manifest, Error>] = [:]

    func manifest(for model: String) async throws -> Manifest {
        if let task = inFlight[model] { return try await task.value }
        let task = Task { try await api.manifest(model) }
        inFlight[model] = task
        defer { inFlight[model] = nil }
        return try await task.value
    }
}
```

- Keep actor methods short. Long synchronous work inside an actor blocks every other caller.
- `nonisolated` on actor members that touch only immutable `let` state of `Sendable` type.

## Sendable

- Non-public structs and enums whose stored properties are all `Sendable` are inferred `Sendable`.
  Public types need an explicit conformance.
- Classes are `Sendable` only if `final` with immutable `Sendable` stored properties, or main-actor
  isolated, or protected by a lock.
- Closures crossing isolation are `@Sendable` and capture only `Sendable` values.

```swift
import Synchronization

// Synchronous, thread-safe counter for code that cannot await
final class PacketStats: Sendable {
    private let dropped = Mutex(0)
    func recordDrop() { dropped.withLock { $0 += 1 } }
    var droppedCount: Int { dropped.withLock { $0 } }
}
```

- `sending` on a parameter or result lets a non-`Sendable` value move across isolation when the caller
  no longer uses it. Prefer making the type `Sendable`; reach for `sending` when it cannot be.
- `@preconcurrency import SomeModule` for dependencies not yet annotated. Remove it once they are.

## Swift 6.2 isolation of async functions

With the upcoming feature `NonisolatedNonsendingByDefault` (on in new Xcode 26 projects with
"Approachable Concurrency"), a `nonisolated async` function runs on the caller's actor instead of
hopping to the global executor.

- To force work off the caller's actor (CPU-heavy parsing, compression), mark the function `@concurrent`.
- Check which mode the project uses before reasoning about where an `async` function runs.

```swift
// CPU-bound work explicitly leaves the main actor
@concurrent
nonisolated func decodeLog(_ data: Data) async throws -> [LogEntry] {
    try LogDecoder().decode(data)
}
```

## Cancellation

Cancellation is cooperative. Nothing stops unless the code checks.

- `try Task.checkCancellation()` in loops and before expensive steps.
- `Task.isCancelled` when cleanup is needed instead of throwing.
- `Task.sleep(for:)` and `URLSession` async APIs throw `CancellationError` on cancel.
- Callback APIs with their own cancel method use `withTaskCancellationHandler`:

```swift
func fetch(_ request: LegacyRequest) async throws -> Data {
    let operation = LegacyOperation(request) // Sendable; cancel() is thread-safe
    return try await withTaskCancellationHandler {
        try await withCheckedThrowingContinuation { continuation in
            operation.start { result in continuation.resume(with: result) }
        }
    } onCancel: {
        operation.cancel()
    }
}
```

- `onCancel` runs immediately and concurrently, possibly before `start` is called. The operation must
  tolerate cancel-before-start.
- The cancelled operation must still complete its callback so the continuation resumes.

## Continuations

- `withCheckedThrowingContinuation` in all code. The unsafe variants only after profiling proves a need.
- Resume exactly once on every path, including error and timeout paths.
- A checked continuation that is never resumed leaks the task and logs a warning; resuming twice traps.

## AsyncStream

```swift
func notifications(from characteristic: CharacteristicID) -> AsyncThrowingStream<Data, Error> {
    let (stream, continuation) = AsyncThrowingStream.makeStream(
        of: Data.self,
        bufferingPolicy: .bufferingNewest(64)
    )
    let token = transport.subscribe(characteristic) { event in
        switch event {
        case .value(let data): continuation.yield(data)
        case .failed(let error): continuation.finish(throwing: error)
        case .ended: continuation.finish()
        }
    }
    continuation.onTermination = { _ in token.cancel() }
    return stream
}
```

- Choose a buffering policy on purpose. The default is unbounded; high-rate sensor or BLE notifications
  should use `.bufferingNewest(n)` so memory cannot grow without limit.
- `onTermination` releases the underlying subscription when the consumer cancels or the stream ends.
- `AsyncStream` supports one consumer. For several consumers, give each its own stream.
- Consume in `.task` in SwiftUI, or in a stored `Task` that is cancelled in the owner's teardown.

## Time

- `try await Task.sleep(for: .seconds(2))`, not `Task.sleep(nanoseconds:)`.
- Inject `any Clock<Duration>` into types that wait, time out or debounce, so tests control time.

```swift
final class Reconnector {
    private let clock: any Clock<Duration>
    init(clock: any Clock<Duration> = ContinuousClock()) { self.clock = clock }

    func backoff(attempt: Int) async throws {
        try await clock.sleep(for: .seconds(min(1 << attempt, 30)))
    }
}
```

## Migrating older code

- Convert completion handlers at the lowest layer first, then move up. Keep the callback version only
  if other modules still depend on it.
- Replace `DispatchQueue` serial queues that guard state with an `actor`.
- Replace `DispatchGroup` fan-out with a task group.
- Move one module at a time to Swift 6 language mode; fix warnings in Swift 5 mode with complete
  checking first.
- Never fix a data-race error with `@unchecked Sendable` without a lock covering every stored property.
