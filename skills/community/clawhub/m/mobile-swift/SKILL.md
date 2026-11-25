---
name: mobile-swift
description: "Writes idiomatic modern Swift for iOS: Swift 6 strict concurrency (async/await, actors, @MainActor, Sendable, cancellation), value types, some vs any, typed throws, SwiftUI with @Observable, NavigationStack and stable identity, SwiftData, SPM modules and Swift Testing. Use when writing or refactoring Swift views, view models, services or packages, or fixing concurrency warnings and Swift 6 migration errors."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Swift for iOS

Write Swift the way a senior iOS engineer would in Swift 6: data-race safe by construction, value types
first, no crashes on unexpected input, SwiftUI views that stay small and cheap, and code split into
packages with tests next to it.

## When to use

- Writing new Swift, SwiftUI or SwiftData code, or generating a feature from a ticket.
- Refactoring or migrating older code: completion handlers, `ObservableObject`, `NavigationView`,
  Core Data, XCTest unit tests, Swift 5 language mode.
- Fixing compiler errors such as "sending risks causing data races", "non-Sendable type",
  "main actor-isolated property can not be referenced".
- Adding a local Swift package, a test target, a lint config, or a privacy manifest.

Not for: reviewing someone else's diff (use `mobile-code-review`), a security audit (use
`mobile-security`), or choosing an app architecture (use `mobile-mvvm`, `mobile-mvi`).

## Workflow

1. Read the project settings before writing code.
   - Swift language mode, strict concurrency level, default actor isolation, minimum iOS version.
   - `Package.swift` files, existing lint and format configs, test framework in use.
2. Match the deployment target. `@Observable` and SwiftData need iOS 17, `Mutex` needs iOS 18.
   Gate newer APIs with `if #available` or ask before raising the target.
3. Load the reference for the area being touched:
   [Concurrency](references/concurrency.md), [SwiftUI](references/swiftui.md),
   [SwiftData](references/swiftdata.md), [Testing](references/testing.md),
   [Packages and tooling](references/packages.md).
4. Model data first: value types, explicit `Sendable` where it crosses isolation, typed errors where the
   set is closed.
5. Decide isolation per type: `@MainActor` for UI-facing state, an `actor` for shared mutable state,
   `nonisolated` value types for everything else.
6. Write the code, then the tests in the same change. Swift Testing for unit tests, XCTest only for UI
   and performance tests.
7. Build with zero concurrency warnings, run the tests, run SwiftLint and the formatter.
8. List every `Info.plist` key, entitlement, background mode and privacy manifest entry the change adds.
   These have signing and App Review consequences and must be called out explicitly.

## Rules

### 1. Structs by default, `final class` only when identity matters

```swift
// BAD: reference semantics for plain data, shared mutation, not Sendable
class Reading { var value: Double; var date: Date }

// GOOD
struct Reading: Sendable, Equatable { let value: Double; let date: Date }

// GOOD: identity and lifetime matter (connection, cache, model observed by UI)
@MainActor @Observable
final class DeviceSession { var state: ConnectionState = .idle }
```

- Classes are `final` unless subclassing is designed for.
- `let` over `var`. Mutation happens through methods with clear names, not public setters.

### 2. No force unwraps, force casts or `try!` in app code

```swift
// BAD
let url = URL(string: base + path)!
let cell = tableView.dequeueReusableCell(withIdentifier: "c") as! DeviceCell

// GOOD
guard let url = URL(string: base + path) else { throw APIError.invalidURL(path) }
let name = device.name ?? String(localized: "Unknown device")
```

- In tests use `try #require(value)` instead of `!`, so a nil fails the test instead of crashing the run.
- A static literal URL may use a `guard` with `preconditionFailure("...")` and a message, never a bare `!`.

### 3. `some` when one concrete type is fixed, `any` only when it must vary at runtime

```swift
// BAD: existential box and dynamic dispatch for no reason
func render(_ items: any Collection<Reading>) -> any View

// GOOD: generic, specialised by the compiler
func render(_ items: some Collection<Reading>) -> some View

// GOOD: heterogeneous storage really needs an existential
var sinks: [any TelemetrySink]
```

- Write `any` explicitly for every existential even where the compiler does not yet require it.
- Primary associated types (`some Collection<Reading>`, `any AsyncSequence<Int, Never>`) instead of
  type-erasing wrappers.

### 4. Structured concurrency before unstructured `Task {}`

```swift
// BAD: unstructured tasks, no cancellation propagation, errors lost
Task { profile = try await api.profile() }
Task { devices = try await api.devices() }

// GOOD: both cancelled with the parent, errors propagate
async let profile = api.profile()
async let devices = api.devices()
state = .loaded(try await profile, try await devices)
```

- Dynamic fan-out uses `withThrowingTaskGroup`; bound the width for large inputs.
- `Task {}` only at an entry point from synchronous code (button action, delegate callback), and its
  handle is stored and cancelled when the owner goes away.
- `Task.detached` needs a written reason.

### 5. UI-facing state is `@MainActor`, data crossing isolation is `Sendable`

```swift
// BAD: silences the checker, data race still possible
final class TokenStore: @unchecked Sendable { var token: String? }

// GOOD: an actor owns the mutable state
actor TokenStore {
    private var token: String?
    func update(_ new: String?) { token = new }
}
```

- View models: `@MainActor @Observable final class`.
- `@unchecked Sendable` and `nonisolated(unsafe)` only with a lock guarding every field and a comment
  explaining why an actor does not fit.
- No `DispatchQueue.main.async` in `async` code; isolate the function or type to `@MainActor` instead.

### 6. Actor state is re-checked after every `await`

```swift
// Inside an actor or a @MainActor class.
// BAD: reentrancy, two callers both pass the check and both connect
func connect() async throws {
    guard state == .idle else { return }
    try await transport.open()
    state = .connected
}

// GOOD: claim the state before suspending
func connect() async throws {
    guard state == .idle else { return }
    state = .connecting
    do { try await transport.open(); state = .connected }
    catch { state = .idle; throw error }
}
```

### 7. Cancellation is checked in loops and forwarded to callback APIs

```swift
// BAD: keeps uploading after the user left the screen
for chunk in chunks { try await upload(chunk) }

// GOOD
for chunk in chunks {
    try Task.checkCancellation()
    try await upload(chunk)
}
```

- Wrap callback APIs that support cancelling in `withTaskCancellationHandler`. Details in
  [Concurrency](references/concurrency.md).
- Do not catch `CancellationError` and turn it into a user-facing error state.

### 8. Callbacks are bridged once, at the edge

```swift
// BAD: continuation resumed for every discovery, traps on the second one
func scan() async -> Peripheral {
    await withCheckedContinuation { c in
        scanner.onDiscover = { c.resume(returning: $0) }
    }
}

// GOOD: repeated events are a stream, cleaned up when the consumer stops
// scanner: a Sendable wrapper around the platform delegate API
func discoveries() -> AsyncStream<Peripheral> {
    let (stream, continuation) = AsyncStream.makeStream(of: Peripheral.self)
    scanner.onDiscover = { continuation.yield($0) }
    continuation.onTermination = { [scanner] _ in scanner.stop() }
    scanner.start()
    return stream
}
```

- One-shot callback: `withCheckedThrowingContinuation`, resumed exactly once on every path.
- Repeated events: `AsyncStream` / `AsyncThrowingStream` with `onTermination`.

### 9. Typed throws only for closed, local error domains

```swift
// BAD: public API promises a single error type forever, callers gain nothing
public func sync() async throws(SyncError)

// GOOD: closed set, callers switch exhaustively
func decode(_ frame: Data) throws(FrameError) -> Packet
enum FrameError: Error { case tooShort(Int), badChecksum, unknownOpcode(UInt8) }
```

- Use `throws(E)` for parsers, validation and module-internal code. Use untyped `throws` at module and
  network boundaries where new failure kinds will appear.
- Typed throws does not replace `Result` in stored properties.

### 10. SwiftUI: the view that creates a model owns it in `@State`

```swift
// BAD: legacy pattern, model recreated on every parent redraw
@ObservedObject var model = DeviceListModel()

// GOOD
struct DeviceListScreen: View {
    @State private var model = DeviceListModel()
    var body: some View {
        DeviceList(model: model)
            .task { await model.load() }
    }
}
```

- Passed-in `@Observable` models are plain `let`/`var` properties; use `@Bindable` only to get bindings.
- `@Binding` for a value the parent owns. `@Environment` for app-wide dependencies.
- `.task(id: query)` for work that restarts when an input changes; it cancels the previous run.

### 11. SwiftUI identity is stable and views stay small

```swift
// BAD: index identity, AnyView erasure, heavy body
ForEach(items.indices, id: \.self) { i in AnyView(row(items[i])) }

// GOOD
ForEach(items) { item in DeviceRow(device: item) }
```

- Items are `Identifiable` with an id from the data, never `UUID()` created in `body`.
- Conditional content uses `@ViewBuilder` or `Group`, not `AnyView`.
- Extract subviews when `body` stops fitting on a screen; no formatters, sorting or I/O inside `body`.

### 12. Capture lists break cycles, and only where a cycle exists

```swift
// BAD: self -> task -> self, the loop keeps the object alive forever
monitor = Task { for await r in readings { self.append(r) } }

// GOOD
monitor = Task { [weak self] in
    for await r in readings {
        guard let self else { return }
        append(r)
    }
}
```

- Escaping closures stored by `self` (timers, observers, stored tasks) capture `[weak self]`.
- `unowned` only when the referenced object provably outlives the closure.
- SwiftUI views are structs: no `[weak self]` in `.task` or button actions.
- Delegates are `weak var delegate: (any SomeDelegate)?` with an `AnyObject`-constrained protocol.

### 13. SwiftData contexts stay on their actor

```swift
// BAD: ModelContext and model objects are not Sendable
Task.detached { context.insert(entity) }

// GOOD: background work in a model actor, identifiers cross the boundary
@ModelActor
actor ReadingImporter {
    func importAll(_ rows: [ReadingDTO]) throws {
        for row in rows { modelContext.insert(ReadingEntity(row)) }
        try modelContext.save()
    }
}
```

- UI reads with `@Query`; writes go through `@Environment(\.modelContext)` or a model actor.
- Pass `PersistentIdentifier` between actors, not model instances. See [SwiftData](references/swiftdata.md).

### 14. Features are local packages with explicit, minimal APIs

```swift
// BAD: public only so a sibling target can call it, now visible to the whole app
public func makeDecoder() -> JSONDecoder

// GOOD: visible to other targets of the same Swift package, hidden from everyone else
package func makeDecoder() -> JSONDecoder
```

- One local package (or one target) per feature plus shared core modules; features depend on core,
  never on each other.
- Default to `internal`. `package` spans targets of one Swift package only; `public` is for what
  other packages and the app target import.
- Every dependency is declared in `Package.swift`; nothing relies on a transitive import.

### 15. Swift Testing for unit tests, XCTest where it is still required

```swift
// BAD: a nil or a thrown error crashes the whole test run
func testParse() { XCTAssertEqual(try! parse(frame).battery!, 87) }

// GOOD: failures are reported, the run continues
@Test func parsesBatteryLevel() throws {
    let packet = try parse(frame)
    let battery = try #require(packet.battery)
    #expect(battery == 87)
}
```

- XCTest stays for UI tests (`XCUIApplication`) and performance tests (`measure`).
- No `sleep` in tests; inject a clock. Details in [Testing](references/testing.md).

## Platform and project changes

Call these out in the change summary every time, with the exact key or entitlement name.

- `Info.plist` usage strings: `NSBluetoothAlwaysUsageDescription`, `NSCameraUsageDescription`,
  `NSLocationWhenInUseUsageDescription` and others. For Bluetooth, camera and microphone a missing
  string terminates the app on first access.
- `UIBackgroundModes` entries such as `bluetooth-central` or `location`. App Review asks for justification.
- Entitlements (push, App Groups, Keychain sharing, associated domains) change the provisioning profile.
- `PrivacyInfo.xcprivacy`: required-reason APIs (for example `UserDefaults`, file timestamps, system boot
  time, disk space) need a declared reason; collected data types and tracking domains must match reality.
  See [Packages and tooling](references/packages.md).

## Anti-patterns

- Sprinkling `@MainActor`, `@unchecked Sendable` or `nonisolated(unsafe)` until the compiler is quiet.
- `Task { }` inside `onAppear` instead of `.task`.
- `DispatchSemaphore` or `DispatchGroup.wait()` to make async code synchronous.
- `ObservableObject` and `@Published` in new code on iOS 17+.
- Giant views with `AnyView` and computed `some View` properties instead of real subviews.
- `UUID()` as the `id` of items created during rendering.
- Singletons (`static let shared`) reached from deep inside views and models instead of injection.
- `try?` that silently drops an error the user should see.
- One giant app target with every file `public` "just in case".
- Adding a third-party SDK without checking it ships its own privacy manifest and signature.

## Checklist

- [ ] Language mode, strict concurrency and deployment target checked before writing
- [ ] Value types by default; classes are `final`
- [ ] No `!`, `as!`, `try!` in app code; tests use `#require`
- [ ] UI-facing types `@MainActor`; shared mutable state in actors; no unjustified `@unchecked Sendable`
- [ ] Actor state re-validated after each `await`
- [ ] Long loops check cancellation; continuations resume exactly once; streams have `onTermination`
- [ ] Escaping closures stored by `self` use `[weak self]`; delegates are `weak`
- [ ] SwiftUI models owned with `@State`; async work in `.task` / `.task(id:)`; stable `ForEach` ids
- [ ] No `AnyView` or heavy work in `body`
- [ ] SwiftData contexts not shared across actors; identifiers passed instead of models
- [ ] New code in the right package with the narrowest access level
- [ ] Swift Testing unit tests added; XCTest only for UI and performance
- [ ] Zero warnings, tests pass, SwiftLint and formatter clean
- [ ] `Info.plist`, entitlements, background modes and privacy manifest changes listed explicitly

## Related skills

- `mobile-code-review` -- review checklist that applies these rules to a diff
- `mobile-security` -- Keychain, ATS, data protection and MASVS checks for the code written here
- `mobile-mvvm`, `mobile-mvi` -- where view models, state and intents live
- `mobile-design-patterns` -- repository, coordinator and dependency injection patterns in Swift
- `mobile-ci-cd` -- Xcode Cloud, signing and test plans in the pipeline
- `mobile-kotlin`, `mobile-flutter` -- the equivalent rules for Android and Flutter
- `mobile-kmp` -- consuming a Kotlin Multiplatform framework from Swift
- `mobile-ble` -- CoreBluetooth rules
- `mobile-testing` -- cross-platform test strategy and snapshot tests
- `mobile-performance` -- Instruments, launch time and MetricKit
