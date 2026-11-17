# Coroutines and Flow reference

Load this when writing or changing suspend functions, scopes, dispatchers, Flow pipelines or ViewModel state.

## Scopes and ownership

| Work | Scope |
|---|---|
| Screen-bound loading, user actions | `viewModelScope` (runs on `Dispatchers.Main.immediate`) |
| UI-only work in a composable | `rememberCoroutineScope()` or `LaunchedEffect` |
| Activity or Fragment UI collection | `lifecycleScope` + `repeatOnLifecycle(Lifecycle.State.STARTED)` |
| Must finish even if the screen closes (short) | Injected application scope |
| Must survive process death, constraints, retries | WorkManager (`CoroutineWorker`) |

Application scope, provided once:

```kotlin
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class ApplicationScope
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class IoDispatcher
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class DefaultDispatcher

@Module
@InstallIn(SingletonComponent::class)
object CoroutinesModule {
    @Provides @IoDispatcher fun io(): CoroutineDispatcher = Dispatchers.IO
    @Provides @DefaultDispatcher fun default(): CoroutineDispatcher = Dispatchers.Default

    @Provides @Singleton @ApplicationScope
    fun appScope(@DefaultDispatcher dispatcher: CoroutineDispatcher): CoroutineScope =
        CoroutineScope(SupervisorJob() + dispatcher)
}
```

- `SupervisorJob` so one failed child does not cancel the whole app scope.
- A class that creates its own `CoroutineScope(...)` must also own a `close()` or `cancel()` path.

## Structured concurrency

```kotlin
// Parallel, all-or-nothing: first failure cancels the siblings and is rethrown
suspend fun loadProfile(id: UserId): Profile = coroutineScope {
    val user = async { userApi.get(id) }
    val stats = async { statsApi.get(id) }
    Profile(user.await(), stats.await())
}

// Fan-out over a list
suspend fun uploadAll(files: List<File>) = coroutineScope {
    files.map { async { uploader.upload(it) } }.awaitAll()
}

// Bounded parallelism for many items
private val uploads = io.limitedParallelism(4)
```

- `supervisorScope` when children fail independently; handle each child's failure at its `await` or
  inside the child.
- `CoroutineExceptionHandler` works only on root coroutines (`launch` in a scope). It does nothing on
  `async` or on child coroutines.
- `withTimeout` throws `TimeoutCancellationException`; `withTimeoutOrNull` returns null. Prefer the latter
  when timeout is an expected outcome.
- Long CPU loops call `ensureActive()` or `yield()` so cancellation can take effect.
- `NonCancellable` only for short cleanup in `finally`:

```kotlin
try {
    session.stream()
} finally {
    withContext(NonCancellable) { session.close() }
}
```

## Error handling

```kotlin
// A suspend-safe replacement for runCatching
suspend inline fun <T> suspendRunCatching(block: () -> T): Result<T> = try {
    Result.success(block())
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    Result.failure(e)
}
```

- Map exceptions to a domain error type in the data layer. The UI renders `UiError`, not `IOException`.
- Do not mix `Result`/sealed results and thrown exceptions for the same failure in one layer.

## Cold vs hot

| Type | Starts | Holds value | Use for |
|---|---|---|---|
| `flow {}`, Room `Flow`, `callbackFlow` | On each collect | No | Data streams from a source |
| `StateFlow` | Always active | Latest value, conflated, `distinctUntilChanged` | UI state |
| `SharedFlow` | Always active | Configurable replay | Broadcast events to many collectors |
| `Channel` | n/a | Buffered until received | Single-consumer events |

## ViewModel state patterns

```kotlin
@HiltViewModel
class DevicesViewModel @Inject constructor(
    repository: DeviceRepository,
    private val connect: ConnectDeviceUseCase,
) : ViewModel() {

    private val query = MutableStateFlow("")
    private val transient = MutableStateFlow(Transient())

    val state: StateFlow<DevicesUiState> = combine(
        repository.observeDevices(),
        query,
        transient,
    ) { devices, q, t ->
        DevicesUiState(
            devices = devices.filter { it.name.contains(q, ignoreCase = true) }
                .map { it.toUi() }
                .toImmutableList(),
            query = q,
            connectingId = t.connectingId,
        )
    }
        .catch { emit(DevicesUiState(error = UiError.Storage)) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), DevicesUiState())

    fun onQueryChange(value: String) { query.value = value }

    fun onConnect(id: DeviceId) {
        viewModelScope.launch {
            transient.update { it.copy(connectingId = id) }
            try {
                connect(id)
            } finally {
                transient.update { it.copy(connectingId = null) }
            }
        }
    }
}
```

- `stateIn` once per property, not in a getter.
- `combine` emits only after every source has emitted once. Give sources an initial value.
- `catch` handles upstream errors only. An exception in `collect` is not caught by it.
- After `catch`, the flow completes. For a stream that must continue, handle errors inside a
  `flatMapLatest` or `retryWhen`.

## Operators that matter

```kotlin
// flowOn changes the context of everything ABOVE it
repository.rawReadings()
    .map { parse(it) }          // runs on io
    .flowOn(io)
    .filter { it.isValid }      // runs on the collector's context

// Search: cancel the previous request on each new query
query
    .debounce(300)
    .distinctUntilChanged()
    .flatMapLatest { q -> repository.search(q) }
```

- `flatMapLatest` requires `@OptIn(ExperimentalCoroutinesApi::class)`; `debounce` requires
  `@OptIn(FlowPreview::class)`.
- `conflate()` or `sample()` (`FlowPreview`) for high-frequency sensor or BLE notifications that the UI cannot render at
  full rate.
- `distinctUntilChanged()` is redundant on a `StateFlow`.

## Wrapping callbacks

```kotlin
// Caller holds BLUETOOTH_SCAN; ScanFailedException is an app-defined type
fun BluetoothLeScanner.scanFlow(filters: List<ScanFilter>, settings: ScanSettings): Flow<ScanResult> =
    callbackFlow {
        val callback = object : ScanCallback() {
            override fun onScanResult(callbackType: Int, result: ScanResult) {
                trySend(result) // called on a binder thread, never assume main
            }
            override fun onScanFailed(errorCode: Int) {
                close(ScanFailedException(errorCode))
            }
        }
        startScan(filters, settings, callback)
        awaitClose { stopScan(callback) }
    }
```

- `awaitClose` is mandatory. Without it the flow completes immediately and the listener leaks.
- `trySend` from callbacks; `send` only inside the producer coroutine.
- Pick a buffer policy deliberately: `.buffer(capacity, BufferOverflow.DROP_OLDEST)` for latest-wins data.
- One-shot callbacks use `suspendCancellableCoroutine` and unregister in `invokeOnCancellation`.

## One-off events

Prefer modelling the event as state the UI consumes and acknowledges:

```kotlin
data class EditUiState(val saved: Boolean = false)
// UI: LaunchedEffect(state.saved) { if (state.saved) { onSaved(); viewModel.onSavedHandled() } }
```

If a `Channel` is used, expose it with `receiveAsFlow()` and collect it in `LaunchedEffect` or
`repeatOnLifecycle`, so events are not delivered to a stopped UI.

## Views and Fragments

```kotlin
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        launch { viewModel.state.collect(::render) }
        launch { viewModel.events.collect(::handle) }
    }
}
```

- Fragments use `viewLifecycleOwner`, not the Fragment itself.
- `launchWhenStarted` and `launchWhenResumed` are deprecated. Replace with `repeatOnLifecycle`.
