# Kotlin pattern implementations

Load this when implementing or reviewing patterns in Kotlin (Android or KMP). Assumes coroutines, Flow and
Hilt. Adapt the DI annotations if the project uses Koin or manual injection.

## Repository (offline-first)

```kotlin
// Interface only because ViewModel tests use a fake and the domain module must not see Room or Retrofit.
interface DeviceRepository {
    fun observeDevices(): Flow<List<Device>>
    suspend fun refresh(): RefreshResult
}

class OfflineFirstDeviceRepository @Inject constructor(
    private val api: DeviceApi,
    private val dao: DeviceDao,
    @IoDispatcher private val io: CoroutineDispatcher,
) : DeviceRepository {

    override fun observeDevices(): Flow<List<Device>> =
        dao.observeAll().map { rows -> rows.map(DeviceEntity::toDomain) }

    override suspend fun refresh(): RefreshResult = withContext(io) {
        try {
            dao.upsertAll(api.devices().map(DeviceDto::toEntity))
            RefreshResult.Updated
        } catch (e: IOException) {
            RefreshResult.Offline
        }
    }
}

@Module
@InstallIn(SingletonComponent::class)
abstract class DataModule {
    @Binds abstract fun deviceRepository(impl: OfflineFirstDeviceRepository): DeviceRepository
}
```

- The UI observes the database; `refresh()` only writes into it. No second in-memory copy that can drift.
- `HttpException` from Retrofit is not an `IOException`; map it separately if the server can reject requests.

## Factory

```kotlin
// Factory function named after the type, the Kotlin convention (like MutableStateFlow(...)).
fun BackoffPolicy(config: RetryConfig): BackoffPolicy = when (config.mode) {
    RetryMode.Fixed -> BackoffPolicy { config.baseMillis }
    RetryMode.Exponential -> BackoffPolicy { attempt -> config.baseMillis shl attempt.coerceAtMost(6) }
}

// Companion factory for parsing; the constructor stays private so invalid instances cannot exist.
@JvmInline
value class SerialNumber private constructor(val value: String) {
    companion object {
        private val format = Regex("[A-Z0-9]{12}")
        fun parse(raw: String): SerialNumber? = raw.trim().uppercase().takeIf(format::matches)?.let(::SerialNumber)
    }
}
```

Assisted injection when a ViewModel or worker needs runtime arguments plus injected dependencies:
use Hilt `@AssistedInject` / `@AssistedFactory` rather than a hand-written factory class.

## Builder replaced by named and default arguments

```kotlin
data class ScanSettingsSpec(
    val timeout: Duration = 10.seconds,
    val serviceFilter: UUID? = null,
    val lowLatency: Boolean = false,
)

val spec = ScanSettingsSpec(serviceFilter = TELEMETRY_SERVICE, lowLatency = true)
val longer = spec.copy(timeout = 30.seconds)
```

- `require(...)` in `init` validates combinations a builder would have checked in `build()`.
- A type-safe DSL (`buildList { }`, `buildString { }`, a custom `@DslMarker` builder) is justified for
  nested structures such as test fixtures or menus, not for flat option bags.
- Java callers of a class with defaults need `@JvmOverloads` on the constructor.

## Singleton through DI

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun okHttp(): OkHttpClient = OkHttpClient.Builder().build()
}

@Singleton
class BleManager @Inject constructor(@ApplicationContext private val context: Context)
```

- Scope matches lifetime: `@Singleton` for process-wide, `@ActivityRetainedScoped` or `@ViewModelScoped`
  for screen-level state. Never put screen state in a `@Singleton`.
- An application `CoroutineScope` for work that outlives screens is also injected, not created ad hoc.

## Strategy

```kotlin
fun interface ChecksumStrategy { fun compute(bytes: ByteArray): Long }

class FrameValidator(private val checksum: ChecksumStrategy) {
    fun isValid(payload: ByteArray, expected: Long): Boolean = checksum.compute(payload) == expected
}

// java.util.zip.CRC32 is available on every API level.
val crc32 = ChecksumStrategy { bytes -> CRC32().apply { update(bytes) }.value }
```

Which checksum a device protocol uses is defined by the firmware spec. Do not guess it.

## Observer

```kotlin
class ConnectionMonitor @Inject constructor(private val bluetooth: BluetoothAdapterWrapper) {

    // Hot state: latest value always available, deduplicated.
    private val _state = MutableStateFlow<ConnState>(ConnState.Disconnected)
    val state: StateFlow<ConnState> = _state.asStateFlow()

    // Adapting a listener API into a cold Flow: unregister in awaitClose.
    fun adapterEnabled(): Flow<Boolean> = callbackFlow {
        val listener = AdapterListener { enabled -> trySend(enabled) }
        bluetooth.register(listener)
        awaitClose { bluetooth.unregister(listener) }
    }.distinctUntilChanged()
}
```

- `StateFlow` for state, `SharedFlow` for broadcasts where every subscriber needs every value.
- Expose cold flows to the UI through `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), initial)`.
- Collect in UI with `collectAsStateWithLifecycle()` or `repeatOnLifecycle`.

## Adapter

```kotlin
// DTO -> domain at the data-layer edge. The domain type never sees nullable wire fields.
fun DeviceDto.toDomain(): Device? {
    val serial = SerialNumber.parse(serial ?: return null) ?: return null
    return Device(serial = serial, name = name.orEmpty(), firmware = firmware ?: "unknown")
}

// Callback API -> suspend. Resume exactly once; a resume after cancellation is ignored.
suspend fun LocationClient.currentLocation(): Location =
    suspendCancellableCoroutine { cont ->
        val request = requestSingle(
            onResult = { cont.resume(it) },
            onError = { cont.resumeWithException(it) },
        )
        cont.invokeOnCancellation { request.cancel() }
    }
```

## Decorator

```kotlin
class CachingForecastSource(
    private val inner: ForecastSource,
    private val time: TimeSource = TimeSource.Monotonic,
    private val ttl: Duration = 10.minutes,
) : ForecastSource by inner {

    private val mutex = Mutex()
    private var cached: Pair<TimeMark, Forecast>? = null

    override suspend fun forecast(): Forecast = mutex.withLock {
        cached?.takeIf { it.first.elapsedNow() < ttl }?.second
            ?: inner.forecast().also { cached = time.markNow() to it }
    }
}
```

- `TimeSource` is injected so tests pass a `TestTimeSource` and advance it with `+=`.
- The `Mutex` makes concurrent callers share one fetch instead of racing.

## Facade

```kotlin
class DeviceSession @Inject constructor(
    private val client: GattClient,
    private val queue: GattQueue,
    private val machine: ConnectionStateMachine,
) {
    suspend fun open(address: String, desiredMtu: Int): OpenResult {
        machine.onEvent(ConnEvent.Connect)
        val link = client.connect(address) ?: return OpenResult.Unreachable
        val mtu = (queue.execute(GattCommand.RequestMtu(desiredMtu)) as? GattResponse.Mtu)?.value
            ?: return OpenResult.Failed
        queue.execute(GattCommand.DiscoverServices)
        queue.execute(GattCommand.EnableNotifications(TELEMETRY_CHARACTERISTIC))
        machine.onEvent(ConnEvent.LinkUp(mtu = mtu))
        return OpenResult.Ready(link)
    }
}
```

The facade sequences calls; it does not own UI state or persistence.

## State machine (connection)

```kotlin
sealed interface ConnState {
    data object Disconnected : ConnState
    data class Connecting(val attempt: Int) : ConnState
    data class Connected(val mtu: Int) : ConnState
    data object Disconnecting : ConnState
    data class Failed(val error: ConnError) : ConnState
}

sealed interface ConnEvent {
    data object Connect : ConnEvent
    data class LinkUp(val mtu: Int) : ConnEvent
    data class LinkLost(val error: ConnError) : ConnEvent
    data object Disconnect : ConnEvent
    data object Closed : ConnEvent
}

fun reduce(state: ConnState, event: ConnEvent, maxAttempts: Int = 3): ConnState = when (state) {
    ConnState.Disconnected, is ConnState.Failed -> when (event) {
        ConnEvent.Connect -> ConnState.Connecting(attempt = 1)
        else -> state
    }
    is ConnState.Connecting -> when (event) {
        is ConnEvent.LinkUp -> ConnState.Connected(event.mtu)
        is ConnEvent.LinkLost ->
            if (state.attempt < maxAttempts) ConnState.Connecting(state.attempt + 1) else ConnState.Failed(event.error)
        ConnEvent.Disconnect -> ConnState.Disconnecting
        ConnEvent.Connect, ConnEvent.Closed -> state
    }
    is ConnState.Connected -> when (event) {
        is ConnEvent.LinkLost -> ConnState.Connecting(attempt = 1)
        ConnEvent.Disconnect -> ConnState.Disconnecting
        ConnEvent.Connect, is ConnEvent.LinkUp, ConnEvent.Closed -> state
    }
    ConnState.Disconnecting -> when (event) {
        ConnEvent.Closed, is ConnEvent.LinkLost -> ConnState.Disconnected
        else -> state
    }
}

class ConnectionStateMachine @Inject constructor(private val log: Logger) {
    private val _state = MutableStateFlow<ConnState>(ConnState.Disconnected)
    val state: StateFlow<ConnState> = _state.asStateFlow()

    // Safe from GATT binder threads: update is an atomic compare-and-set over a pure function.
    fun onEvent(event: ConnEvent) {
        val (old, new) = _state.updateAndGetPair { reduce(it, event) }
        if (old == new) log.debug("Ignored $event in $old")
    }
}

private inline fun <T> MutableStateFlow<T>.updateAndGetPair(transform: (T) -> T): Pair<T, T> {
    while (true) {
        val old = value
        val new = transform(old)
        if (compareAndSet(old, new)) return old to new
    }
}
```

- `reduce` is pure, so it is trivially unit tested and safe to retry inside `compareAndSet`.
- Side effects (reconnect timers, `gatt.close()`) run in a collector of `state`, not inside `reduce`.
- Prefer listing events explicitly over `else` where the compiler should flag new events.

```kotlin
class ReduceTest {
    @Test fun `link lost while connected starts reconnect`() {
        assertEquals(ConnState.Connecting(1), reduce(ConnState.Connected(mtu = 247), ConnEvent.LinkLost(ConnError.Timeout)))
    }

    @Test fun `gives up after max attempts`() {
        assertEquals(
            ConnState.Failed(ConnError.Timeout),
            reduce(ConnState.Connecting(3), ConnEvent.LinkLost(ConnError.Timeout), maxAttempts = 3),
        )
    }
}
```

## Command (GATT queue with results and timeout)

```kotlin
sealed interface GattCommand {
    class Read(val characteristic: UUID) : GattCommand
    class Write(val characteristic: UUID, val value: ByteArray) : GattCommand
    class RequestMtu(val mtu: Int) : GattCommand
    data object DiscoverServices : GattCommand
    class EnableNotifications(val characteristic: UUID) : GattCommand
}

sealed interface GattResponse {
    class Value(val bytes: ByteArray) : GattResponse
    data class Mtu(val value: Int) : GattResponse
    data object Done : GattResponse
}

class GattQueue(scope: CoroutineScope, private val executor: GattExecutor) {

    private class Pending(val command: GattCommand, val result: CompletableDeferred<GattResponse>)

    private val pending = Channel<Pending>(Channel.UNLIMITED)

    init {
        scope.launch {
            for (p in pending) {
                // withTimeoutOrNull: a plain withTimeout throws a CancellationException subtype.
                val response = try {
                    withTimeoutOrNull(5.seconds) { executor.executeAndAwait(p.command) }
                } catch (e: GattException) {
                    p.result.completeExceptionally(e)
                    continue
                }
                if (response != null) p.result.complete(response) else p.result.completeExceptionally(GattTimeoutException(p.command))
            }
        }
    }

    suspend fun execute(command: GattCommand): GattResponse {
        val p = Pending(command, CompletableDeferred())
        pending.send(p)
        return p.result.await()
    }
}
```

- `Write` holds a `ByteArray`, so it is a plain class: a `data class` would compare arrays by reference.
- `GattExecutor.executeAndAwait` issues the platform call and suspends until the matching
  `BluetoothGattCallback` fires (bridged with `suspendCancellableCoroutine` or a `CompletableDeferred`).
- Payload size, write type and retry policy come from the firmware protocol document.

Undo / redo variant:

```kotlin
interface EditCommand {
    fun apply(doc: Document): Document
    fun revert(doc: Document): Document
}

class History(private var doc: Document) {
    private val undo = ArrayDeque<EditCommand>()
    private val redo = ArrayDeque<EditCommand>()
    fun run(c: EditCommand) { doc = c.apply(doc); undo.addLast(c); redo.clear() }
    fun undo() { undo.removeLastOrNull()?.let { doc = it.revert(doc); redo.addLast(it) } }
}
```

## Router (Compose)

```kotlin
@Composable
fun DeviceListScreen(state: DeviceListState, onDeviceClick: (String) -> Unit) { ... }

// The nav host owns the back stack; screens only raise intents.
// With Navigation 3 the back stack is a list of typed keys you own, rendered by NavDisplay.
DeviceListScreen(state = state, onDeviceClick = { id -> backStack.add(DeviceDetailKey(id)) })
```

- ViewModels do not hold a `NavController`. Navigation triggered by a result is modelled as state the
  screen reacts to, or a callback from the screen after it observes success.
- Deep links and auth gating are decided in one place (the nav host or a small router class).

## Result types

```kotlin
sealed interface Outcome<out T, out E> {
    data class Ok<T>(val value: T) : Outcome<T, Nothing>
    data class Err<E>(val error: E) : Outcome<Nothing, E>
}

inline fun <T, E, R> Outcome<T, E>.map(f: (T) -> R): Outcome<R, E> = when (this) {
    is Outcome.Ok -> Outcome.Ok(f(value))
    is Outcome.Err -> this
}
```

- `kotlin.Result` is fine inside a layer, but its error is an untyped `Throwable` and `runCatching`
  catches `CancellationException`. At layer boundaries prefer a sealed domain result.
- Exceptions for programmer errors (`require`, `check`, `error`) are not wrapped.

## Delegation

```kotlin
// Class delegation: override only what changes.
class ReadOnlySettings(private val inner: Settings) : Settings by inner {
    override fun set(key: String, value: String) = throw UnsupportedOperationException("read-only")
}

// Property delegation: lifecycle-aware or lazy values without boilerplate.
private val viewModel: DevicesViewModel by viewModels()
private val parser by lazy(LazyThreadSafetyMode.NONE) { FrameParser() } // main-thread only
```

- `by inner` forwards calls made on the wrapper only. If `inner` calls its own methods internally,
  the override is not used (unlike inheritance). Check this before relying on it.
