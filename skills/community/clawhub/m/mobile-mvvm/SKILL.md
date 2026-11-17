---
name: mobile-mvvm
description: "Designs, implements and tests screens with MVVM on Android (Compose, ViewModel, StateFlow, Hilt; legacy LiveData), iOS (SwiftUI, @Observable, @MainActor) and Flutter (Riverpod, ChangeNotifier): single immutable UI state, one-off events, lifecycle-aware collection and ViewModel tests. Use when building or refactoring a screen's state handling, or choosing between MVVM, MVI and MVC."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# MVVM for mobile apps

Build screens where the UI is a plain function of one immutable state object, the ViewModel owns that state
and the screen-scoped work, and data comes from repositories that the ViewModel receives by injection.
The result survives rotation and process death, renders the same state the same way every time, and is
testable without a device.

## When to use

- A new screen or feature needs a ViewModel, state holder or presentation layer.
- An existing screen has state bugs: lost input on rotation or process death, double loads, stale UI,
  snackbars shown twice or never.
- Migrating Java + LiveData + XML screens to Kotlin + StateFlow + Compose, `ObservableObject` to
  `@Observable`, or `setState` screens to Riverpod or provider.
- Reviewing a ViewModel for layer leaks, lifecycle issues or untestable code.
- Choosing between MVVM, MVI and MVC for a screen or a codebase.

Not for: screens with many interacting events, strict event ordering or debounced concurrent requests
(use `mobile-mvi`), or legacy UIKit and Activity-centric code you only maintain (use `mobile-mvc`).

## When to choose MVVM vs MVI vs MVC

| | MVVM | MVI | MVC |
|---|---|---|---|
| State | One `UiState` per screen (or a few observable properties) | One immutable `State`, changed only by a reducer | Spread across controller and views |
| How UI talks to logic | Calls named ViewModel functions (`onRefresh()`) | Sends one sealed `Intent` type | Controller handles view callbacks directly |
| Side effects | Inside ViewModel functions | Explicit effects outside a pure reducer | Inside the controller |
| Boilerplate | Low | Medium to high | Lowest at first, grows fast |
| Testing | ViewModel tests with fakes | Pure reducer tests plus effect tests | Hard, logic bound to views |
| Good fit | Most screens: lists, details, forms, settings | Search with debounce, editors, wizards, chat, real-time device dashboards | Prototypes, small UIKit or Activity code already in that style |
| Platform fit | Android Architecture guidance, SwiftUI `@Observable`, Riverpod, provider | Compose + `StateFlow` store, TCA, Bloc | UIKit `UIViewController`, legacy Activities |

Rules of thumb:
- Default to MVVM with a single `UiState`. It already gives unidirectional data flow.
- Move a screen to MVI when ViewModel functions start racing each other or the state transitions need
  to be auditable and tested as pure functions.
- Do not mix patterns inside one screen. Mixing across screens is fine.

## Layers

```
UI (Composable, SwiftUI View, Widget)  renders UiState, forwards user events
   | events                ^ UiState
   v                       |
ViewModel                  owns screen state and screen-scoped work, maps domain data to UiState
   |
   v
Use cases (optional)       business rules reused by several ViewModels, or too complex for one
   |
   v
Repository                 single source of truth, merges sources, maps DTOs and entities to domain models
   |
   v
Data sources               network, database, BLE, files, platform APIs
```

- Dependencies point down only. Lower layers never import UI or ViewModel types.
- Use cases are optional. Add one when the logic is shared or non-trivial, not as a pass-through.
- The ViewModel lives as long as the screen (navigation destination), not as long as the view instance.

## Workflow

1. Confirm MVVM fits the screen using the table above.
2. Load the reference for the platform before writing code:
   [Kotlin and Compose](references/kotlin.md), [Java with LiveData and ViewBinding](references/java.md),
   [Swift and SwiftUI](references/swift.md), [Dart with Riverpod or provider](references/dart.md).
3. Write the `UiState`: everything the screen renders, with defaults. Derive values (filtered lists,
   button enabled flags) instead of storing them twice.
4. List the user events and name one ViewModel function per event (`onRefresh`, `onFavoriteClick`).
5. Define the repository interface in domain types, plus a fake for tests and previews.
6. Implement the ViewModel: combine sources into `UiState`, handle events, map errors to state.
7. Wire DI and ownership (Hilt, `@State`, Riverpod provider, `ChangeNotifierProvider`).
8. Build the UI as a stateless function of `UiState` plus callbacks. Preview it with fake states.
9. Save small user input that must survive process death (filters, query, selected id).
10. Write ViewModel tests with fakes, run the existing test suite and report failures.

## Rules

### 1. One immutable UiState per screen, exposed read-only

Several independent mutable properties drift out of sync and let the UI write state.

Kotlin:
```kotlin
// BAD: public mutable state, three flows that can disagree
val devices = MutableStateFlow<List<Device>>(emptyList())
val isLoading = MutableStateFlow(false)
val error = MutableStateFlow<String?>(null)

// GOOD
data class DeviceListUiState(
    val devices: List<Device> = emptyList(),
    val isLoading: Boolean = false,
    val userMessage: UserMessage? = null,
)

private val _uiState = MutableStateFlow(DeviceListUiState())
val uiState: StateFlow<DeviceListUiState> = _uiState.asStateFlow()

fun onRefresh() = _uiState.update { it.copy(isLoading = true) }
```

Swift:
```swift
// BAD: the view can write any of these
@Observable final class DeviceListModel { var devices: [Device] = []; var isLoading = false }

// GOOD
@MainActor @Observable
final class DeviceListModel {
    private(set) var state = DeviceListState()
}
```

Dart:
```dart
// BAD: mutable fields, callers mutate the list in place
class DeviceListController extends ChangeNotifier { List<Device> devices = []; }

// GOOD: immutable state, replaced as a whole
class DeviceListNotifier extends Notifier<DeviceListState> {
  @override
  DeviceListState build() => const DeviceListState();
}
```

Java:
```java
// BAD
public final MutableLiveData<List<Device>> devices = new MutableLiveData<>();

// GOOD
private final MediatorLiveData<DeviceListUiState> uiState = new MediatorLiveData<>();
public LiveData<DeviceListUiState> getUiState() { return uiState; }
```

- Swift: separate `private(set)` properties also work and `@Observable` tracks them individually.

### 2. Events go up, state comes down

The UI calls a named function for each user event and renders whatever state comes back.
Composables, Views and Widgets below the screen level receive state and lambdas, not the ViewModel.

```kotlin
// BAD: leaf composable owns the ViewModel, cannot be previewed or reused
@Composable fun DeviceRow(id: String, vm: DeviceListViewModel = hiltViewModel()) { ... }

// GOOD
@Composable fun DeviceRow(device: Device, onFavoriteClick: () -> Unit, modifier: Modifier = Modifier) { ... }
```

```swift
// BAD: view mutates model internals, no place for validation or side effects
Toggle("Online only", isOn: $model.onlineOnly)

// GOOD: the change goes through the model
Toggle("Online only", isOn: Binding(get: { model.state.onlineOnly }, set: { model.setOnlineOnly($0) }))
```

- A direct `@Bindable` binding to a model property is acceptable for plain form fields with no logic.

### 3. The ViewModel knows no UI framework types

- No `Context`, `Activity`, `View`, `NavController`, `UIViewController` or `BuildContext` in a ViewModel.
- No resolved strings. Expose an enum or id; the UI maps it to localized text.

```kotlin
// BAD: leaks the Activity, breaks on locale change, needs Robolectric to test
class DeviceListViewModel(private val context: Context) : ViewModel() {
    fun error() = context.getString(R.string.refresh_failed)
}

// GOOD
enum class UserMessage { RefreshFailed }
// UI: UserMessage.RefreshFailed -> stringResource(R.string.refresh_failed)
```

- Flutter: notifier methods never take a `BuildContext`. Set state (`saved: true`) and let the widget
  navigate from `ref.listen`.

### 4. Expose observed data as hot state, started by the UI

Kotlin: convert repository flows once with `stateIn` and `WhileSubscribed(5_000)`. Collection stops five
seconds after the last subscriber leaves (survives rotation, stops in the background).

```kotlin
// BAD: loads in init, ignores lifecycle, hard to test the initial state
init { viewModelScope.launch { _uiState.value = DeviceListUiState(devices = repo.load()) } }

// GOOD
val uiState: StateFlow<DeviceListUiState> = repository.observeDevices()
    .map { DeviceListUiState(devices = it) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), DeviceListUiState(isLoading = true))
```

Swift: start loading from `.task`, which cancels when the view disappears, not from `init`.
Dart: load in `AsyncNotifier.build`; use `autoDispose` providers for screen state.

### 5. Collect state with the lifecycle

```kotlin
// BAD: keeps collecting while the app is in the background
val state by viewModel.uiState.collectAsState()

// GOOD
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

```java
// BAD: Fragment lifecycle outlives its view, observers pile up after back navigation
viewModel.getUiState().observe(this, this::render);

// GOOD
viewModel.getUiState().observe(getViewLifecycleOwner(), this::render);
```

- Fragments with flows: `viewLifecycleOwner.lifecycleScope` plus `repeatOnLifecycle(Lifecycle.State.STARTED)`.
- SwiftUI: async work in `.task` / `.task(id:)`; `@Observable` reads in `body` are tracked automatically.
- Flutter: `ref.watch` in `build`, `ref.read` in callbacks, `ref.listen` for side effects.

### 6. One-off events are state that the UI acknowledges

Snackbars, navigation after save and dialogs are modelled as nullable state. The UI performs the effect,
then tells the ViewModel it is done. Nothing is lost if the UI is not collecting at that moment.

Kotlin:
```kotlin
// BAD: SharedFlow without replay drops events when nobody collects (rotation, background)
private val _events = MutableSharedFlow<String>()

// GOOD
fun onUserMessageShown() = userMessage.update { null }

// UI
state.userMessage?.let { message ->
    val text = message.toText()
    LaunchedEffect(message) {
        snackbarHostState.showSnackbar(text)
        viewModel.onUserMessageShown()
    }
}
```

Swift:
```swift
.alert(model.state.userMessage?.title ?? "", isPresented: Binding(
    get: { model.state.userMessage != nil },
    set: { if !$0 { model.userMessageShown() } }
)) { Button("OK", role: .cancel) {} }
```

Dart:
```dart
ref.listen(deviceListProvider.select((s) => s.value?.userMessage), (_, message) {
  if (message == null) return;
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message.text(context))));
  ref.read(deviceListProvider.notifier).userMessageShown();
});
```

Channel trade-offs, if the team still prefers an event stream:
- `Channel(Channel.BUFFERED)` + `receiveAsFlow()` keeps events while no one collects, but an event can
  still be lost if the collector is cancelled between receiving and handling it.
- Collect it in `repeatOnLifecycle(STARTED)` on `Dispatchers.Main.immediate` to shrink that window.
- Never use `SingleLiveEvent` in new code; it supports one observer and hides the same race.

### 7. Dependencies come in through the constructor

```kotlin
// BAD: hidden dependency, cannot be faked
class DeviceListViewModel : ViewModel() { private val repo = DeviceRepositoryImpl(ApiClient.instance) }

// GOOD
@HiltViewModel
class DeviceListViewModel @Inject constructor(
    private val repository: DeviceRepository,
    private val savedStateHandle: SavedStateHandle,
) : ViewModel()
```

- Swift: the owning view creates the model once with its dependencies:
  `_model = State(initialValue: DeviceListModel(repository: repository))` in the view's `init`.
- Dart: notifiers read dependencies with `ref.watch(deviceRepositoryProvider)`; tests override that provider.
- Screen state is never held by a `@Singleton`, a global or an app-wide provider.
- Navigation arguments reach the ViewModel through `SavedStateHandle` or assisted injection, not a setter
  called from the UI after creation.

### 8. Small user input survives process death

Rotation is handled by the ViewModel. Process death is not: the ViewModel is recreated empty.

| Platform | ViewModel-owned input | View-only state |
|---|---|---|
| Android | `SavedStateHandle` (`getStateFlow`, `set`) | `rememberSaveable` |
| iOS | Restore from the view on appear | `@SceneStorage` |
| Flutter | Pass restored values in from the widget | `RestorationMixin`, `RestorableInt`, `RestorableTextEditingController` |

```kotlin
// BAD: filter resets after process death
private val onlineOnly = MutableStateFlow(false)

// GOOD
private val onlineOnly = savedStateHandle.getStateFlow(KEY_ONLINE_ONLY, false)
fun onToggleOnlineOnly() { savedStateHandle[KEY_ONLINE_ONLY] = !onlineOnly.value }
```

- Save ids, queries, filters and draft text. Never save lists, images or anything the repository can reload.
- Saved state is not a secure store. Never put tokens or personal data in it.

### 9. The repository is the single source of truth

```kotlin
// BAD: ViewModel talks to Retrofit and Room, maps DTOs, decides caching
class DeviceListViewModel(private val api: DeviceApi, private val dao: DeviceDao) : ViewModel()

// GOOD: ViewModel sees domain models only
class DeviceListViewModel(private val repository: DeviceRepository) : ViewModel()
```

- Repositories expose domain models, not network DTOs or database entities.
- Data that changes over time is observed (`Flow`, `AsyncSequence`, `Stream`), so writes elsewhere update
  the screen without a manual reload.

### 10. Errors become state; cancellation is not an error

```kotlin
// BAD: runCatching swallows CancellationException; catch-all hides bugs
runCatching { repository.refresh() }

// GOOD
try {
    repository.refresh()
} catch (e: IOException) {
    userMessage.value = UserMessage.RefreshFailed
}
```

```swift
do {
    state.devices = try await repository.fetchDevices()
} catch is CancellationError {
    return
} catch {
    state.userMessage = .loadFailed
}
```

- Dart: catch specific types (`on DeviceException`). In `AsyncNotifier`, `AsyncValue.guard` turns a thrown
  error into `AsyncError` for the screen to render.

### 11. Test the ViewModel with fakes and virtual time

```kotlin
@get:Rule val mainDispatcherRule = MainDispatcherRule()

@Test fun `refresh failure shows message until acknowledged`() = runTest {
    repository.refreshError = IOException("offline")
    val viewModel = DeviceListViewModel(repository, SavedStateHandle())
    viewModel.uiState.test {
        viewModel.onRefresh()
        advanceUntilIdle()
        assertEquals(UserMessage.RefreshFailed, expectMostRecentItem().userMessage)
        viewModel.onUserMessageShown()
        assertNull(awaitItem().userMessage)
    }
}
```

- Swift: a `@MainActor` Swift Testing suite awaits the model's async functions directly and uses `#expect`.
- Dart: a `ProviderContainer` with the repository provider overridden by a fake; `container.listen` keeps
  `autoDispose` providers alive. Full examples are in each reference file.
- Fakes over mocks for repositories. Mocks only to verify an interaction that has no visible state.
- Test state transitions and messages, not private functions.
- No `Thread.sleep`, `Task.sleep` or real timers in ViewModel tests.

## Anti-patterns

- A ViewModel per composable or per row. One per screen or navigation destination.
- Sharing one ViewModel across unrelated screens as a global state bag. Share a repository instead.
- `LiveData` or `ObservableObject` in new code without a reason (interop with legacy screens is a reason).
- UI state copied into local `remember` or `@State` and then edited there, so two sources of truth exist.
- Business logic in composables, `body` or `build` (sorting, filtering, validation).
- Use cases that only forward one repository call.
- Calling ViewModel functions from the composable body or `body` instead of an effect or event handler.
- Hardcoded `Dispatchers.IO` in the ViewModel. Repositories own their dispatchers.
- `@ObservedObject var model = Model()`: a new model on every parent redraw. `@State var model = Model()`
  is correct, but its initializer still runs on every parent redraw (only the first instance is kept),
  so keep `init` cheap and start work in `.task`.

## Checklist

- [ ] MVVM chosen deliberately (not a screen that needs `mobile-mvi`)
- [ ] One immutable `UiState` per screen, exposed read-only
- [ ] Derived values computed, not stored twice
- [ ] UI below screen level receives state and callbacks, not the ViewModel
- [ ] No `Context`, `View`, `NavController`, `BuildContext` or resolved strings in the ViewModel
- [ ] Repository flows converted with `stateIn(viewModelScope, WhileSubscribed(5_000), initial)`
- [ ] Collected with `collectAsStateWithLifecycle`, `getViewLifecycleOwner()`, `.task` or `ref.watch`
- [ ] One-off events modelled as state and acknowledged by the UI
- [ ] Dependencies injected by constructor; screen state not held in singletons
- [ ] Filters, query, selected id and draft input survive process death; no secrets in saved state
- [ ] Repository is the source of truth; DTOs mapped at the data layer
- [ ] Errors mapped to user-facing state; cancellation rethrown or ignored, never reported
- [ ] ViewModel tests with fakes and virtual time; existing tests pass

## Related skills

- `mobile-mvi` -- when the screen needs a reducer, explicit intents and effects
- `mobile-mvc` -- maintaining UIKit or Activity-centric screens
- `mobile-design-patterns` -- repository, factory, adapter and other building blocks used here
- `mobile-kotlin`, `mobile-java`, `mobile-swift`, `mobile-flutter` -- language rules for each platform
- `mobile-code-review` -- reviewing the resulting ViewModels and screens
- `mobile-testing` -- where ViewModel tests sit in the overall test strategy
- `mobile-kmp` -- sharing ViewModels between Android and iOS
