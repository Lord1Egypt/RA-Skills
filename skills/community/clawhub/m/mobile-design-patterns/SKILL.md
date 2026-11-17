---
name: mobile-design-patterns
description: "Chooses and implements design patterns in Kotlin, Java, Swift and Dart mobile code: Repository, Factory, Strategy, Observer, Adapter, Decorator, Facade, State machine, Command, Coordinator, Result types and Delegation, with a selection table and over-engineering warnings. Use when picking a pattern, refactoring god classes or flag-driven state, wrapping an SDK, or when a design feels over-abstracted."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile design patterns

Pick the smallest structure that solves a real problem in Android, iOS or Flutter code, implement it
idiomatically for the language, and remove patterns that only add indirection.

## When to use

- Structuring a new feature, data source, SDK wrapper, device protocol or navigation flow.
- Refactoring long `when` / `switch` chains, boolean state flags, god classes or copy-pasted wrappers.
- Reviewing code full of `*Manager`, `*Factory`, `*Builder`, `*Impl` names and deciding which ones earn their place.
- Modelling a lifecycle (BLE connection, upload, onboarding, checkout) as an explicit state machine.
- Deciding between thrown exceptions and typed results at a layer boundary.

Not for: whole-app architecture (use `mobile-mvvm`, `mobile-mvi`, `mobile-mvc`) or security design
(use `mobile-security`).

## Workflow

1. Write the problem in one sentence before naming a pattern: "X changes independently of Y because Z".
   No sentence, no pattern.
2. Check whether the language already solves it: named and default arguments, `by` delegation, function
   types, sealed types, `Flow` / `AsyncSequence` / `Stream`, protocol extensions. Prefer the language feature.
3. Find the problem in the selection table and read the matching rule, including its "Skip when" line.
4. Load the language reference for full implementations: [Kotlin](references/kotlin.md),
   [Swift](references/swift.md), [Dart](references/dart.md), [Java](references/java.md).
5. Implement the smallest version. Add an interface or protocol only for a second implementation,
   a test seam or a module boundary.
6. Wire collaborators through constructor injection, never through globals.
7. Unit test what the pattern isolates: transitions, strategies, mappers, decorators, command ordering.
8. When reviewing, name the cost of a misused pattern (extra files, indirection, test burden) and show the
   simpler alternative.

## Pattern selection

| Problem | Pattern | Mobile example | Skip when |
|---|---|---|---|
| UI must not know if data comes from network, database or cache | Repository | Room or Core Data as source of truth, API refreshes it | One read-only source, no mapping, no caching |
| Concrete type depends on runtime input | Factory | Exporter per format, message type from JSON | Only one type, or DI already builds it |
| Many optional parameters | Named / default args (Builder only in Java) | Notification spec, request options | Kotlin, Swift, Dart: almost always skip Builder |
| One shared instance | DI scope (`@Singleton`, app container) | HTTP client, database, BLE manager | Never hand-roll a mutable global |
| Interchangeable algorithm | Strategy, often just a function | Retry backoff, sort order, image compression | Only one algorithm and no test need |
| React to changing values | Observer via platform streams | Connection state, database queries | One-shot value: use a suspend / async function |
| Foreign API does not fit your interface | Adapter | Callback SDK to suspend / async, DTO to domain | You own both sides: change the interface |
| Add caching, logging, retry or metrics without editing a class | Decorator | Timed or caching repository | It belongs on every call: put it in the class or an HTTP interceptor |
| Multi-step subsystem used from many places | Facade | `DeviceSession.open()` hides connect, MTU, discovery, notifications | It starts holding UI state: split it |
| Behaviour depends on phase; some transitions are illegal | State machine | BLE connection, upload, onboarding | Two states a single `Boolean` models correctly |
| Operations must be queued, serialized, retried or undone | Command | GATT operation queue, undoable edits | Fire-and-forget call with no ordering needs |
| Flow logic spread across screens | Coordinator / Router | Onboarding, deep links, auth gate | One push from list to detail |
| Expected failures are part of the API | Result / sealed errors / typed throws | Network, validation, pairing errors | Programmer errors: let them crash |
| Reuse behaviour or call back to an owner | Delegation | Kotlin `by`, `CBCentralManagerDelegate` | Inheritance is not involved and a lambda suffices |

## Rules

### 1. An abstraction needs a reason

Kotlin:
```kotlin
// BAD: interface + Impl with one implementation, no fake, same module
interface DateFormatter { fun format(i: Instant): String }
class DateFormatterImpl : DateFormatter { ... }

// GOOD: a plain class until a second implementation, a test fake or a module boundary appears
class DateFormatter(private val zone: ZoneId) { fun format(i: Instant): String = ... }
```

Valid reasons for an interface or protocol: a fake in ViewModel tests, a domain module that must not see
the data module, multiple real implementations, a platform split (KMP `expect` / `actual`).

### 2. Repository: one source of truth, domain types out

```kotlin
// BAD: ViewModel talks to Retrofit and Room directly and exposes DTOs
class DevicesViewModel(private val api: DeviceApi, private val dao: DeviceDao) : ViewModel()

// GOOD: database is the source of truth, network only refreshes it, mapping happens here
class DeviceRepository @Inject constructor(private val api: DeviceApi, private val dao: DeviceDao) {
    fun observeDevices(): Flow<List<Device>> = dao.observeAll().map { rows -> rows.map { it.toDomain() } }
    suspend fun refresh() = dao.upsertAll(api.devices().map { it.toEntity() })
}
```

Skip when: one repository per table that forwards DAO calls 1:1. Group by feature or aggregate instead.

### 3. Factory: one place decides which type to build

Kotlin:
```kotlin
// BAD: construction logic duplicated at every call site
val exporter = if (format == "pdf") PdfExporter(fonts) else CsvExporter(separator = ';')

// GOOD
class ExporterFactory @Inject constructor(private val fonts: FontProvider) {
    fun create(format: ExportFormat): Exporter = when (format) {
        ExportFormat.Pdf -> PdfExporter(fonts)
        ExportFormat.Csv -> CsvExporter(separator = ';')
    }
}
```

Dart (factory constructor with pattern matching on untrusted JSON):
```dart
sealed class Message {
  const Message();
  factory Message.fromJson(Map<String, Object?> json) => switch (json) {
        {'type': 'text', 'body': String body} => TextMessage(body),
        {'type': 'image', 'url': String url} => ImageMessage(Uri.parse(url)),
        _ => throw FormatException('Unknown message type: ${json['type']}'),
      };
}
```

Skip when: there is one concrete type, or the DI container already provides it. No factory of factories.

### 4. Builder: use named and default arguments instead

Kotlin:
```kotlin
// BAD: hand-written builder in a language with named arguments
val spec = NotificationSpec.Builder().title("Low battery").channel("alerts").build()

// GOOD
data class NotificationSpec(val title: String, val channel: String = "default", val silent: Boolean = false)
val spec = NotificationSpec(title = "Low battery", channel = "alerts")
```

Swift: a struct with defaulted `var` properties gets a memberwise initializer with default arguments.
Dart: `const NotificationSpec({required this.title, this.channel = 'default'})` plus `copyWith`.
Java: a Builder is the right tool; see [Java](references/java.md).

### 5. Singleton: scope it in DI, do not hand-roll it

Kotlin:
```kotlin
// BAD: global mutable state, leaks Context, cannot be replaced in tests
object Session { lateinit var context: Context; var token: String? = null }

// GOOD
@Singleton
class SessionStore @Inject constructor(@ApplicationContext private val context: Context)
```

Swift:
```swift
// BAD: hidden dependency
final class FeedModel { func load() async throws { items = try await APIClient.shared.feed() } }

// GOOD: injected, `.shared` may be the default only at the composition root
final class FeedModel {
    private let api: FeedAPI
    init(api: FeedAPI) { self.api = api }
}
```

Fine to keep: stateless Kotlin `object` utilities and `data object` cases of sealed types.

### 6. Strategy: often just a function

Kotlin:
```kotlin
// BAD: algorithm switches on a mode flag
fun delayFor(attempt: Int, mode: String): Long = if (mode == "exp") 500L shl attempt else 1_000L

// GOOD: the policy is a value the caller injects
fun interface BackoffPolicy { fun delayMillis(attempt: Int): Long }

val exponential = BackoffPolicy { attempt -> 500L shl attempt.coerceAtMost(6) }
val fixed = BackoffPolicy { 1_000L }
class Uploader(private val backoff: BackoffPolicy)
```

Swift: `let backoff: (Int) -> Duration`. Dart: `typedef BackoffPolicy = Duration Function(int attempt);`.
Skip when: only one algorithm exists and tests do not need to swap it.

### 7. Observer: use the platform stream type, not listener lists

Kotlin:
```kotlin
// BAD: listeners never removed, callbacks on arbitrary threads
private val listeners = mutableListOf<(ConnState) -> Unit>()

// GOOD
private val _state = MutableStateFlow<ConnState>(ConnState.Disconnected)
val state: StateFlow<ConnState> = _state.asStateFlow()
```

Swift: `@Observable` for UI models, `AsyncStream` for single-consumer event streams, Combine
`CurrentValueSubject` when several subscribers need the latest value.
Dart: `Stream` from a `StreamController.broadcast()` closed by its owner, or `ValueNotifier` for UI.
Skip when: the value is produced once. Return it from a suspend or async function.

### 8. Adapter: wrap foreign APIs at the edge

Kotlin:
```kotlin
// BAD: SDK callback types leak into the ViewModel
printer.print(job, object : PrintCallback { ... })

// GOOD: one adapter turns the callback API into a cancellable suspend function
suspend fun LegacyPrinter.printAwait(job: PrintJob): PrintResult =
    suspendCancellableCoroutine { cont ->
        val handle = print(job, object : PrintCallback {
            override fun onDone(result: PrintResult) = cont.resume(result)
            override fun onError(error: Throwable) = cont.resumeWithException(error)
        })
        cont.invokeOnCancellation { handle.cancel() }
    }
```

Swift: `withCheckedThrowingContinuation`, resumed exactly once. Dart: a `Completer`.
DTO-to-domain mappers are adapters too; keep them in the data layer.

### 9. Decorator: add cross-cutting behaviour by wrapping

Kotlin:
```kotlin
// BAD: timing code copy-pasted into every method, or a subclass of the concrete client
// GOOD: delegate everything, override only what changes
class TimedDeviceApi(private val inner: DeviceApi, private val metrics: Metrics) : DeviceApi by inner {
    override suspend fun firmwareInfo(id: String): FirmwareInfo {
        val mark = TimeSource.Monotonic.markNow()
        try { return inner.firmwareInfo(id) } finally { metrics.record("firmwareInfo", mark.elapsedNow()) }
    }
}
```

Skip when: the concern is HTTP-level (use an OkHttp `Interceptor` or `URLSession` configuration), or the
stack of decorators has an order nobody documented.

### 10. Facade: hide a multi-step subsystem behind intent-level calls

```kotlin
// BAD: every screen repeats connect -> request MTU -> discover services -> enable notifications
// GOOD
class DeviceSession @Inject constructor(private val gatt: GattClient, private val queue: GattQueue) {
    suspend fun open(address: String): Result<Unit> = ...   // runs the whole sequence in order
    fun telemetry(): Flow<Telemetry> = ...
    suspend fun close() = ...
}
```

Skip when: the facade starts holding UI state, analytics and persistence. Split it by capability.

### 11. State machine: sealed states, explicit transitions

Kotlin:
```kotlin
// BAD: flags that can contradict each other (connected && connecting)
var isConnecting = false; var isConnected = false; var lastError: Throwable? = null

// GOOD: states carry their own data; one pure function decides transitions
sealed interface ConnState {
    data object Disconnected : ConnState
    data class Connecting(val attempt: Int) : ConnState
    data class Connected(val mtu: Int) : ConnState
    data class Failed(val error: ConnError) : ConnState
}

fun reduce(state: ConnState, event: ConnEvent): ConnState = when (state) {
    is ConnState.Connecting -> when (event) {
        is ConnEvent.LinkUp -> ConnState.Connected(event.mtu)
        is ConnEvent.LinkLost -> if (state.attempt < 3) ConnState.Connecting(state.attempt + 1) else ConnState.Failed(event.error)
        else -> state // illegal here: ignore and log
    }
    // ... one branch per state
}

// GATT callbacks arrive on binder threads: funnel every event through one atomic update
fun onEvent(event: ConnEvent) = _state.update { reduce(it, event) }
```

Swift: `enum ConnectionState` with associated values and a `mutating func handle(_ event:)` inside an actor.
Dart: `sealed class` plus an exhaustive `switch`. Full versions with tests are in the references.
Skip when: two states that one `Boolean` models without contradictions.

### 12. Command: operations as values, executed in order

```kotlin
// BAD: Android GATT allows one outstanding operation; the second call is rejected while the first runs
gatt.writeCharacteristic(config, payload, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
gatt.readCharacteristic(status)

// GOOD: commands queued and run one at a time by a single consumer
sealed interface GattCommand {
    class Write(val characteristic: UUID, val value: ByteArray) : GattCommand
    class Read(val characteristic: UUID) : GattCommand
}

class GattQueue(scope: CoroutineScope, private val executor: GattExecutor) {
    private val commands = Channel<GattCommand>(Channel.UNLIMITED)
    init { scope.launch { for (command in commands) executor.executeAndAwait(command) } }
    fun enqueue(command: GattCommand) { commands.trySend(command) }
}
```

Also fits: undo / redo (`apply` and `revert`), offline actions persisted and replayed.
Skip when: calls are independent and fire-and-forget.

### 13. Coordinator / Router: views raise intents, one owner decides the flow

Swift:
```swift
// BAD: each view builds the next screen and its dependencies
NavigationLink { PairingView(service: PairingService(api: .shared)) } label: { Text("Continue") }

// GOOD: typed routes, one owner of the path
enum OnboardingRoute: Hashable { case permissions, pairing, done }

@MainActor @Observable
final class OnboardingCoordinator {
    var path: [OnboardingRoute] = []
    func permissionsGranted() { path.append(.pairing) }
    func paired() { path.append(.done) }
}
```

Kotlin (Compose): screens take callbacks (`onDeviceClick: (String) -> Unit`); the nav host owns the back
stack. Dart: `go_router` with `redirect` for auth gates. Skip when: the app has a handful of linear screens.

### 14. Expected errors are typed results; bugs still crash

Kotlin:
```kotlin
// BAD: every failure collapses to null; runCatching also swallows CancellationException
suspend fun pair(id: String): Device? = runCatching { api.pair(id) }.getOrNull()

// GOOD
sealed interface PairResult {
    data class Paired(val device: Device) : PairResult
    data object Timeout : PairResult
    data class Rejected(val reason: String) : PairResult
}
```

Swift: `func pair(id: String) async throws(PairingError) -> Device` when the error set is closed.
Dart: `sealed class Result<T>` with `Ok` and `Err`, matched with an exhaustive `switch`.
Do not mix thrown exceptions and result types in the same layer.

### 15. Delegation: compose behaviour, keep back-references weak

Kotlin:
```kotlin
// BAD: inheriting a concrete class to reuse one method
class AuditedStore : PrefsStore() { override fun put(k: String, v: String) { audit(k); super.put(k, v) } }

// GOOD: class delegation through an interface
class AuditedStore(private val inner: KeyValueStore, private val audit: Audit) : KeyValueStore by inner {
    override fun put(key: String, value: String) { audit.record(key); inner.put(key, value) }
}
```

Swift:
```swift
// BAD: strong delegate, owner <-> child retain cycle
var delegate: ScannerDelegate?

// GOOD: class-constrained protocol, weak reference
protocol ScannerDelegate: AnyObject { func scanner(_ s: Scanner, didFind device: Device) }
weak var delegate: ScannerDelegate?
```

## Anti-patterns

- `interface Foo` + `FooImpl` with one implementation and no fake, in the same module.
- A pattern chosen before the problem was stated. "We might need it later" is not a reason.
- `*Manager` and `*Helper` classes that mix networking, persistence and UI state: a god object, not a facade.
- Builders in Kotlin, Swift or Dart; hand-rolled singletons with `lateinit` or `static var shared` state.
- Use cases that only forward one repository call, added "for consistency".
- Boolean flags modelling a lifecycle, or a state machine where transitions happen in many places.
- Listener lists, `NotificationCenter` or event buses used where a typed stream would do.
- Generic `BaseRepository<T>`, `BaseViewModel<S, E, A>` hierarchies that every feature must bend to.
- Strategy hierarchies for an algorithm that has exactly one implementation.
- Wrapping every third-party type "in case we switch libraries" when nothing is planned.
- Decorator chains or command queues with undocumented ordering assumptions.

## Checklist

- [ ] Problem stated in one sentence before the pattern was chosen
- [ ] Language feature considered first (named args, `by`, function types, sealed types, streams)
- [ ] Every interface or protocol has a second implementation, a test fake or a module boundary
- [ ] Repositories expose domain types and a single source of truth
- [ ] Shared instances come from DI scopes, not mutable globals
- [ ] Observables use `Flow` / `AsyncSequence` / Combine / `Stream`, and subscriptions are scoped
- [ ] Foreign APIs adapted at the edge; callbacks resume exactly once and support cancellation
- [ ] State machines: sealed states, one transition function, illegal transitions handled, events serialized
- [ ] Commands that touch serialized resources (GATT, files) run one at a time
- [ ] Navigation decisions live in one owner per flow
- [ ] Expected errors typed; cancellation not swallowed; programmer errors not caught
- [ ] Swift delegates are `weak` with `AnyObject` protocols
- [ ] Unit tests cover transitions, strategies, mappers and decorator behaviour

## Related skills

- `mobile-mvvm`, `mobile-mvi`, `mobile-mvc` -- the architecture these patterns plug into
- `mobile-kotlin`, `mobile-java`, `mobile-swift`, `mobile-flutter` -- language idioms behind each implementation
- `mobile-code-review` -- reviewing pattern misuse as part of a change
- `mobile-security` -- when a pattern wraps storage, crypto or network trust decisions
- `mobile-ble` -- the connection state machine and GATT command queue in practice
