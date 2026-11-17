# Kotlin and Android review reference

Load this when the change contains `.kt` or `.kts` files. Each item lists what to look for and the usual severity.

## Quick scan

Search the diff for these first. Each hit needs a closer look, not an automatic finding.

| Pattern | Why | Usual severity |
|---|---|---|
| `GlobalScope`, `CoroutineScope(` in a class with no `cancel()` | Unowned work, leaks | Major |
| `runBlocking` outside tests and `main` | Blocks the calling thread, ANR on main | Major |
| `runCatching {` around suspend calls | Swallows `CancellationException` | Major |
| `catch (e: Exception)` / `catch (e: Throwable)` in suspend code | Same, unless it rethrows cancellation | Major |
| `Dispatchers.IO` / `Dispatchers.Default` hardcoded in a class | Untestable, hidden threading | Minor |
| `!!` | Crash on unexpected null | Major if input is external |
| `lateinit var` read before guaranteed init | `UninitializedPropertyAccessException` | Major |
| `collectAsState()` | Collects while app is backgrounded | Minor |
| `launchWhenStarted`, `launchWhenResumed` | Deprecated, suspends instead of cancelling | Minor |
| `fallbackToDestructiveMigration` | Deletes user data on schema change | Blocker in release builds |
| `allowMainThreadQueries` | Jank and ANR | Major |
| `registerReceiver(` without an export flag | Crash when targeting Android 14+ | Blocker |
| `Log.d(` / `println(` with tokens, emails, device IDs | Personal data in logs | Major, see `mobile-security` |

## Coroutines and Flow

- Every `launch` and `async` runs in a scope tied to a lifecycle: `viewModelScope`, `lifecycleScope`,
  or an injected application scope for work that must outlive a screen.
- Prefer `suspend` functions over functions that launch internally and return `Unit`. The caller owns the scope.
- Injected dispatchers, so tests can replace them.
- `CancellationException` is rethrown. A generic `catch` in suspend code must rethrow it:

```kotlin
// BAD
try { repo.refresh() } catch (e: Exception) { log(e) }

// GOOD
try {
    repo.refresh()
} catch (e: CancellationException) {
    throw e
} catch (e: IOException) {
    log(e)
}
```

- Mutable state is private; the public type is read-only.

```kotlin
// BAD: anyone can push state, and read-modify-write races
val state = MutableStateFlow(UiState())
fun select(id: String) { state.value = state.value.copy(selected = id) }

// GOOD
private val _state = MutableStateFlow(UiState())
val state: StateFlow<UiState> = _state.asStateFlow()
fun select(id: String) = _state.update { it.copy(selected = id) }
```

- Cold flows exposed to UI are converted once, not per collector:

```kotlin
// BAD: new upstream per collector, restarts on rotation
val items: Flow<List<Item>> get() = repo.observe()

// GOOD
val items: StateFlow<List<Item>> = repo.observe()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
```

- `flowOn` changes the upstream context only. Check it is placed after the operators that need it.
- One-off events: prefer modelling them as state the UI consumes and acknowledges. If a `Channel` is used,
  check it is collected with `repeatOnLifecycle` so events are not delivered to a stopped UI.
- Fragments collect with `viewLifecycleOwner.lifecycleScope` plus `repeatOnLifecycle(Lifecycle.State.STARTED)`,
  never `lifecycleScope` alone.

## Jetpack Compose

- Composables do not perform side effects in the body. Use `LaunchedEffect`, `DisposableEffect`,
  or event callbacks.

```kotlin
// BAD: runs on every recomposition
@Composable fun Screen(vm: ScreenViewModel) {
    vm.load()
}

// GOOD
@Composable fun Screen(vm: ScreenViewModel) {
    LaunchedEffect(Unit) { vm.load() }
}
```

- `LaunchedEffect` keys match the inputs the effect reads. `LaunchedEffect(Unit)` that reads a changing
  parameter is a bug; use the parameter as key or `rememberUpdatedState`.
- `remember` keys include every input of the calculation, otherwise the cached value is stale.
- High-frequency state (scroll, animation) is read in a lambda modifier or `derivedStateOf`:

```kotlin
// BAD: recomposes on every scroll pixel
val showFab = listState.firstVisibleItemIndex > 0

// GOOD
val showFab by remember { derivedStateOf { listState.firstVisibleItemIndex > 0 } }
```

- Stability: with strong skipping (default since Kotlin 2.0.20), unstable parameters are compared by
  instance. A list rebuilt on every recomposition defeats skipping. Hoist it, `remember` it, or use
  `kotlinx.collections.immutable`.
- Lazy lists use `key` and, for mixed rows, `contentType`.
- Reusable composables take `modifier: Modifier = Modifier` as the first optional parameter and apply it
  to the root element only.
- Composables below the screen level receive state and lambdas, not the ViewModel.
- `rememberSaveable` for user input that must survive process death and rotation.

## Lifecycle and Android components

- No `Activity`, `Fragment`, `View` or `Context` (other than application context) in singletons, companion
  objects or ViewModels.
- Fragment view bindings are cleared in `onDestroyView`.
- Broadcast receivers registered at runtime use `ContextCompat.registerReceiver` with
  `RECEIVER_EXPORTED` or `RECEIVER_NOT_EXPORTED`, and are unregistered.
- Foreground services declare `android:foregroundServiceType` and the matching permission (required when
  targeting Android 14+). Check the type matches what the service actually does.
- Deferrable background work uses WorkManager, not a service or a coroutine in `Application`.
- New permissions in the manifest are justified in the MR and requested at the point of use.

## Hilt and dependency injection

- `@ApplicationContext` for context in singletons.
- Scope annotations match lifetime: no `@Singleton` holding screen state.
- No service locator calls (`EntryPoints.get`) inside business logic.

## Room and persistence

- DAO functions are `suspend` or return `Flow`.
- Every schema version bump has a `Migration` or `AutoMigration`, and `exportSchema = true`.
- Transactions wrap multi-step writes (`@Transaction` or `withTransaction`).

## Error handling and nullability

- `!!` only where the invariant is local and obvious; otherwise `requireNotNull(x) { "reason" }` or a
  safe call with a fallback.
- Network and IO results are mapped to a domain error type the UI can render, not raw exceptions.
- `Result` or sealed result types are not mixed with thrown exceptions in the same layer.

## Testing

- `runTest` for coroutines; `StandardTestDispatcher(testScheduler)` injected; `Dispatchers.setMain` in a
  rule or extension when `viewModelScope` is used.
- Turbine (`flow.test { ... }`) for Flow assertions instead of `toList()` with timing hacks.
- MockK: `coEvery` / `coVerify` for suspend functions. Prefer fakes for repositories.
- Compose UI tests find nodes by semantics (text, content description, test tag), not by position.

## Build and dependencies

- New dependencies are added to `libs.versions.toml`, not hardcoded in module build files.
- KSP preferred over kapt for new annotation processors.
- R8 keep rules added for new reflection, serialization or JNI code.
- `minSdk`, `targetSdk` or `compileSdk` changes are called out explicitly in the MR.
