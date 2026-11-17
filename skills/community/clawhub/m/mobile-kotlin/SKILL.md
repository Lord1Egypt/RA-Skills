---
name: mobile-kotlin
description: "Writes idiomatic modern Kotlin for Android: Kotlin 2.x, null safety, sealed and value classes, structured coroutines with injected dispatchers, Flow and StateFlow, Jetpack Compose state and stability, Hilt, Room, KSP, Gradle version catalogs, R8 and tests with MockK and Turbine, plus Android 15 and 16 changes. Use when writing or refactoring Kotlin ViewModels, composables, repositories, DAOs, DI modules or build.gradle.kts files."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Kotlin for Android

Write Kotlin the way a senior Android engineer would in a current codebase: null-safe, immutable by default,
structured concurrency everywhere, Compose that skips work it does not need to do, and a build that is
reproducible from the version catalog. Prefer the boring, documented API over a clever one.

## When to use

- Writing new Kotlin code in an Android app: ViewModels, use cases, repositories, composables, DAOs, workers.
- Refactoring Java, callback or RxJava code to coroutines and Flow.
- Migrating XML screens to Jetpack Compose, kapt to KSP, Groovy Gradle to Kotlin DSL.
- Fixing recomposition, lifecycle, coroutine-leak or nullability bugs.
- Updating code for a new `targetSdk` (edge-to-edge, predictive back, foreground service rules).

Not for: architecture choice (use `mobile-mvvm`, `mobile-mvi`), a security audit (use `mobile-security`),
legacy Java maintenance (use `mobile-java`), or reviewing someone else's diff (use `mobile-code-review`).

## Workflow

1. Read the project before writing code.
   - `gradle/libs.versions.toml`: Kotlin, AGP, Compose BOM, coroutines, Hilt, Room versions.
   - Module `build.gradle.kts`: `minSdk`, `targetSdk`, `compileSdk`, KSP or kapt, Compose enabled.
   - Existing conventions: package layout, base classes, dispatcher qualifiers, error types, test style.
2. Match the existing stack. Do not add a library the project does not use without saying so.
   Do not change `minSdk`, `targetSdk` or `compileSdk` without asking.
3. Load the reference for the area being touched:
   [Coroutines and Flow](references/coroutines-flow.md), [Compose](references/compose.md),
   [Hilt and Room](references/hilt-room.md), [Build and tooling](references/build.md),
   [Platform changes](references/platform.md), [Testing](references/testing.md).
4. Model first: domain types, UI state, events, errors as sealed or data types. Then data layer, then
   ViewModel, then UI.
5. Write the code following the Rules below. Keep functions small, `private` by default, and public API
   explicit about types.
6. Add or update unit tests for new domain and data logic, and a Compose test for new interactive UI.
7. Run the build, the tests and the linters (`./gradlew detekt ktlintCheck testDebugUnitTest` or the
   project's equivalents). Report failures honestly; do not declare done on a red build.
8. Summarize what changed, any new dependency, and any manifest, permission or SDK impact.

## Baseline stack

| Area | Default | Avoid in new code |
|---|---|---|
| Language | Kotlin 2.x, K2 compiler | Kotlin 1.x language versions, synthetic view imports |
| UI | Jetpack Compose + Material 3 | New XML layouts, `findViewById` |
| State | `StateFlow` + immutable data class | `LiveData` in new ViewModels, mutable public state |
| Async | Coroutines + Flow | `AsyncTask`, raw threads, new RxJava |
| DI | Hilt with constructor injection | Manual singletons, service locators |
| Persistence | Room (suspend + Flow), DataStore | `SharedPreferences` for new code |
| Serialization | kotlinx.serialization | Reflection-based parsers without keep rules |
| Codegen | KSP | kapt where a KSP processor exists |
| Build | Kotlin DSL + `libs.versions.toml` | Hardcoded versions in module files |

## Rules

### 1. No `!!`. Fail with a message or handle the null

```kotlin
// BAD: NullPointerException with no context
val id = savedStateHandle.get<String>("id")!!

// GOOD: invariant violation explains itself
val id = requireNotNull(savedStateHandle.get<String>("id")) { "id nav argument missing" }

// GOOD: absence is a normal case
val name = user?.displayName ?: context.getString(R.string.anonymous)
```

- `checkNotNull` for state invariants, `requireNotNull` for arguments. Java platform types are nullable.
- `lateinit` only for framework-injected fields (`@Inject lateinit var` in an entry point), never for data.

### 2. State is immutable; variants are sealed

```kotlin
// BAD: mutable fields, impossible states (loading and error at once)
class ProfileState { var loading = false; var error: String? = null; var user: User? = null }

// GOOD
sealed interface ProfileUiState {
    data object Loading : ProfileUiState
    data class Content(val user: User, val isRefreshing: Boolean = false) : ProfileUiState
    data class Error(val reason: UiError) : ProfileUiState
}
```

- `when` over a sealed type has no `else`, so a new variant is a compile error, not a silent fallthrough.
- Use `val` and read-only collection types in data classes. Change state with `copy`.
- Guard conditions in `when` (stable since Kotlin 2.2) replace nested `if` inside a branch:
  `is ProfileUiState.Content if it.isRefreshing -> ...`.

### 3. Typed IDs use value classes

```kotlin
// BAD: easy to swap arguments, compiler cannot help
fun assign(deviceId: String, userId: String)
assign(user.id, device.id) // compiles, wrong

// GOOD: zero-cost wrapper on the JVM
@JvmInline value class DeviceId(val value: String)
@JvmInline value class UserId(val value: String)
fun assign(deviceId: DeviceId, userId: UserId)
```

- Keep value classes in the domain layer. Map to primitives at DTO and entity boundaries unless the
  library supports them (kotlinx.serialization does).
- Validate in `init` when the wrapper carries an invariant: `init { require(value.isNotBlank()) }`.

### 4. Every coroutine has an owner. No `GlobalScope`

```kotlin
// BAD: outlives the screen, cannot be cancelled or tested
GlobalScope.launch { repository.sync() }

// GOOD: tied to the ViewModel
viewModelScope.launch { repository.sync() }

// GOOD: work that must outlive a screen uses an injected application scope or WorkManager
class SyncTrigger @Inject constructor(@ApplicationScope private val scope: CoroutineScope)
```

- Repositories and use cases expose `suspend` functions or `Flow`. They do not launch and return `Unit`.
- `runBlocking` only in `main` functions and legacy bridges, never on the main thread.

### 5. Suspend functions are main-safe; dispatchers are injected

```kotlin
// BAD: hardcoded dispatcher, caller must remember to switch threads
class FileStore { fun read(): ByteArray = file.readBytes() }

// GOOD
class FileStore @Inject constructor(
    @IoDispatcher private val io: CoroutineDispatcher,
) {
    suspend fun read(): ByteArray = withContext(io) { file.readBytes() }
}
```

- The function that does the blocking work switches context. Callers never wrap it again.
- `Dispatchers.Default` for CPU work, IO dispatcher for blocking IO. Main is only for UI.

### 6. `CancellationException` is always rethrown

```kotlin
// BAD: runCatching and catch-all both swallow cancellation
val result = runCatching { api.fetch() }
try { api.fetch() } catch (e: Exception) { log(e) }

// GOOD
try {
    api.fetch()
} catch (e: CancellationException) {
    throw e
} catch (e: IOException) {
    _state.update { it.copy(error = UiError.Network) }
}
```

Catch the narrowest exception that can be handled. Use `ensureActive()` in long loops.

### 7. Use `supervisorScope` when children fail independently

```kotlin
// BAD: one failed widget cancels all the others
suspend fun loadDashboard() = coroutineScope {
    val a = async { api.weather() }
    val b = async { api.news() }
    Dashboard(a.await(), b.await())
}

// GOOD: each child failure is handled at its await
suspend fun loadDashboard() = supervisorScope {
    val a = async { api.weather() }
    val b = async { api.news() }
    Dashboard(weather = a.awaitOrNull(), news = b.awaitOrNull())
}
```

`awaitOrNull` is a local helper that catches the expected exception types and rethrows cancellation.
Use `coroutineScope` when the result is all-or-nothing.

### 8. Mutable state is private; updates are atomic

```kotlin
// BAD: public mutable state and a read-modify-write race
val state = MutableStateFlow(UiState())
fun select(id: ItemId) { state.value = state.value.copy(selected = id) }

// GOOD
private val _state = MutableStateFlow(UiState())
val state: StateFlow<UiState> = _state.asStateFlow()
fun select(id: ItemId) = _state.update { it.copy(selected = id) }
```

### 9. Cold flows become state once, and UI collects with the lifecycle

```kotlin
// BAD: new upstream per collector, keeps running in the background
val items: Flow<List<Item>> get() = repository.observeItems()
val items by viewModel.items.collectAsState(initial = emptyList())

// GOOD
val items: StateFlow<List<Item>> = repository.observeItems()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

val items by viewModel.items.collectAsStateWithLifecycle()
```

- `WhileSubscribed(5_000)` keeps the upstream alive across configuration changes, stops it in background.
- Views and Fragments collect inside `repeatOnLifecycle(Lifecycle.State.STARTED)`.
- Details on `flowOn`, `catch`, `combine` and SharedFlow: [Coroutines and Flow](references/coroutines-flow.md).

### 10. Composables are stateless; state is hoisted

```kotlin
// BAD: ViewModel passed deep, no modifier, not previewable
@Composable
fun DeviceRow(vm: DevicesViewModel, id: DeviceId) { /* reads vm.state, calls vm.connect */ }

// GOOD
@Composable
fun DeviceRow(
    device: DeviceUi,
    onConnect: (DeviceId) -> Unit,
    modifier: Modifier = Modifier,
) {
    Row(modifier.clickable { onConnect(device.id) }) { Text(device.name) }
}
```

- Only the screen-level composable touches the ViewModel. Below it: state in, lambdas out.
- `modifier: Modifier = Modifier` is the first optional parameter and is applied to the root only.
- `rememberSaveable` for user input that must survive rotation and process death.

### 11. Parameters are stable so composables can skip

```kotlin
// BAD: List is an interface the compiler treats as unstable; a new list instance
// every emission forces recomposition of every row
data class FeedUi(val posts: List<PostUi>)

// GOOD
@Immutable
data class FeedUi(val posts: ImmutableList<PostUi>)
// built with posts.map(::toUi).toImmutableList()
```

- Strong skipping is the default since Kotlin 2.0.20: unstable parameters are compared by instance,
  stable ones by `equals`. Recreating objects on every emission still defeats skipping.
- Do not sprinkle `@Stable` to silence reports. Annotate only types that keep the contract.

### 12. Effects are keyed by what they read

```kotlin
// BAD: keeps the first deviceId forever
LaunchedEffect(Unit) { viewModel.connect(deviceId) }

// GOOD: restarts when deviceId changes
LaunchedEffect(deviceId) { viewModel.connect(deviceId) }

// GOOD: long-lived effect that must call the latest lambda without restarting
val currentOnTimeout by rememberUpdatedState(onTimeout)
LaunchedEffect(Unit) { delay(30_000); currentOnTimeout() }
```

- Listeners and observers registered in composition go in `DisposableEffect` with `onDispose`.
- No side effects in the composable body. More in [Compose](references/compose.md).

### 13. Dependencies come through the constructor

```kotlin
// BAD: Activity context in a singleton, hidden dependency
object Prefs { lateinit var context: Context }

// GOOD
@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val settings: SettingsRepository,
    private val savedStateHandle: SavedStateHandle,
) : ViewModel()

@Singleton
class SettingsRepository @Inject constructor(
    @ApplicationContext private val context: Context,
)
```

- Bind interfaces with `@Binds` in an abstract module; `@Provides` only for third-party types.
- Scope annotations match lifetime. Details: [Hilt and Room](references/hilt-room.md).

### 14. Room DAOs are suspend or Flow, and schemas migrate

```kotlin
// BAD: blocking DAO, and user data wiped on the next schema change
@Query("SELECT * FROM device") fun all(): List<DeviceEntity>
Room.databaseBuilder(ctx, AppDb::class.java, "app.db").fallbackToDestructiveMigration()

// GOOD
@Query("SELECT * FROM device ORDER BY name") fun observeAll(): Flow<List<DeviceEntity>>
@Upsert suspend fun upsert(device: DeviceEntity)

@Database(entities = [DeviceEntity::class], version = 3, exportSchema = true)
abstract class AppDb : RoomDatabase()
```

- Every version bump ships a `Migration` or `AutoMigration` and a migration test.

### 15. KSP, version catalog, and the Compose compiler plugin

```kotlin
// BAD: kapt and hardcoded versions
plugins { kotlin("kapt") }
dependencies { kapt("com.google.dagger:hilt-compiler:2.51") }

// GOOD
plugins {
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
    alias(libs.plugins.kotlin.compose)
}
dependencies { ksp(libs.hilt.compiler) }
```

- `libs.plugins.kotlin.compose` maps to `org.jetbrains.kotlin.plugin.compose`, versioned with Kotlin.
- Release builds enable R8 and add keep rules for reflection. Details: [Build and tooling](references/build.md).

### 16. Code is ready for the current `targetSdk`

```kotlin
// BAD: content under the status bar when targeting SDK 35+, and onBackPressed is deprecated
// and no longer called when targeting SDK 36 with predictive back
setContent { LazyColumn { items(rows, key = { it.id }) { RowItem(it) } } }
override fun onBackPressed() { if (editing) cancelEdit() else super.onBackPressed() }

// GOOD
enableEdgeToEdge()
setContent {
    Scaffold { innerPadding ->
        LazyColumn(contentPadding = innerPadding) { items(rows, key = { it.id }) { RowItem(it) } }
    }
    BackHandler(enabled = editing) { cancelEdit() }
}
```

Foreground service types, large-screen orientation rules and more: [Platform changes](references/platform.md).

### 17. New logic ships with deterministic tests

```kotlin
// BAD: real dispatcher and sleep, slow and flaky
@Test fun loads() { vm.load(); Thread.sleep(1000); assertEquals(3, vm.state.value.items.size) }

// GOOD: virtual time, Turbine for the flow
@Test fun loads() = runTest {
    coEvery { repo.items() } returns listOf(a, b, c)
    val vm = ItemsViewModel(repo)
    vm.state.test {
        assertEquals(ItemsUiState.Loading, awaitItem())
        assertEquals(3, (awaitItem() as ItemsUiState.Content).items.size)
    }
}
```

Main dispatcher rule, fakes vs mocks and Compose tests: [Testing](references/testing.md).

## Anti-patterns

- `!!` "because it cannot be null here". If it truly cannot, the type should say so.
- `GlobalScope`, `runBlocking` on the main thread, or a `CoroutineScope(...)` field nobody cancels.
- `runCatching` or `catch (e: Exception)` around suspend calls without rethrowing cancellation.
- `MutableStateFlow` or `MutableList` exposed from a ViewModel.
- One-off events kept in state that the UI never acknowledges, so the last navigation or toast replays after
  rotation. Clear the event once handled (see `mobile-mvvm`).
- ViewModels importing `android.view`, `Context` (non-application), or Compose UI types.
- Passing a ViewModel into leaf composables, or `hiltViewModel()` called below the screen level.
- `LaunchedEffect(Unit)` reading a parameter that changes.
- `derivedStateOf` wrapping a value that changes as often as its input. It adds cost, not savings.
- Lazy lists without `key`, or keyed by index.
- New kapt processors, versions hardcoded in module files, `kotlinOptions {}` instead of `compilerOptions {}`.
- `fallbackToDestructiveMigration()` in release builds.
- Secrets, tokens or API keys in `BuildConfig`, `strings.xml` or source. Escalate to `mobile-security`.
- Logging device identifiers, emails or tokens with `Log.d`. They are personal data.
- Silently bumping SDK levels or adding manifest permissions without calling it out.

## Checklist

- [ ] Project versions, SDK levels and conventions read before writing code
- [ ] No `!!`; nullable inputs handled or failed with `requireNotNull` and a message
- [ ] UI state is an immutable data class or sealed interface; `when` is exhaustive without `else`
- [ ] Typed IDs are value classes where mix-ups are possible
- [ ] Every coroutine has an owner scope; no `GlobalScope`
- [ ] Dispatchers injected; blocking work wrapped in `withContext` at the source
- [ ] `CancellationException` rethrown in every catch around suspend code
- [ ] Mutable flows private; updates use `update {}`
- [ ] Cold flows converted with `stateIn(..., WhileSubscribed(5_000), ...)`; UI uses `collectAsStateWithLifecycle`
- [ ] Composables stateless below the screen; `modifier` parameter first optional and applied to root
- [ ] Composable parameters stable; immutable collections where lists are passed
- [ ] Effects keyed correctly; `rememberUpdatedState` for long-lived lambdas; listeners in `DisposableEffect`
- [ ] Lazy lists have stable `key` and `contentType` for mixed rows
- [ ] Hilt constructor injection; `@ApplicationContext` only; scopes match lifetimes
- [ ] Room DAOs suspend or Flow; migrations and `exportSchema = true`
- [ ] KSP instead of kapt; new dependencies in `libs.versions.toml`
- [ ] R8 keep rules for reflection or serialization added and release build verified
- [ ] Edge-to-edge insets and predictive back handled for the current `targetSdk`
- [ ] Unit tests for new domain and data logic; tests and linters pass

## Related skills

- `mobile-mvvm`, `mobile-mvi` -- where ViewModels, state and events fit in the architecture
- `mobile-design-patterns` -- repository, use case, adapter and factory patterns in Kotlin
- `mobile-code-review` -- reviewing Kotlin changes against these rules
- `mobile-security` -- storage, network, crypto and logging rules for the same code
- `mobile-ci-cd` -- running detekt, ktlint, tests and release builds in CI
- `mobile-java` -- legacy Java code and Java-Kotlin interop
- `mobile-kmp` -- sharing Kotlin code with iOS
- `mobile-ble` -- Android Bluetooth Low Energy rules
- `mobile-testing` -- cross-platform test strategy and screenshot tests
- `mobile-performance` -- Baseline Profiles, Macrobenchmark and Android vitals
