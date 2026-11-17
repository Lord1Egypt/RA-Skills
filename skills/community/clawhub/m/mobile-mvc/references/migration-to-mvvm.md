# Migrating MVC or MVP screens to MVVM

Load this when moving an existing controller-based screen to a ViewModel. The approach is a strangler:
the old screen keeps working while state and logic move behind it, one screen and one slice at a time.
Each step is a separate, shippable MR.

## Choose the screen

- Start with the screen that changes most often or produces the most bugs, not the easiest one.
- Skip screens that are stable, simple or scheduled for removal (see "When MVC is still fine" in the
  skill).
- One screen per migration. Shared base classes (`BaseActivity`, `BaseViewController`) are migrated last.

## Steps

1. Characterization tests. Pin current behaviour before touching it: formatting output, validation
   results, state after each user action, error messages. If the logic cannot be tested in place,
   extract it into a pure function with no other change, and test that.
2. Extract pure logic. Formatting, validation and mapping move into plain types with unit tests. The
   controller calls them. Behaviour is unchanged.
3. Introduce the ViewModel behind the existing controller. Empty or nearly empty, injected, created by
   the platform's mechanism. The controller holds a reference; nothing reads from it yet.
4. Move state one piece at a time. For each field: add it to the ViewModel's UI state, make the
   controller render from the ViewModel, delete the controller's field. Never keep both.
5. Move actions. Controller event handlers call ViewModel methods instead of services.
6. Move navigation. The ViewModel exposes navigation as state or a one-off event; the controller or a
   coordinator performs it.
7. Delete the presenter, the contract and dead code. Remove the old tests only after the new ones cover
   the same behaviour.
8. Optionally replace the view layer later (XML to Compose, UIKit to SwiftUI) as its own project. The
   ViewModel does not change for that.

Each step keeps the app releasable. If a step cannot be shipped alone, it is too big.

## Android: MVP or god Activity to ViewModel

Step 3, ViewModel behind the Activity:

```kotlin
data class DevicesUiState(
    val loading: Boolean = false,
    val rows: List<DeviceRow> = emptyList(),
    val error: DevicesError? = null,
)

@HiltViewModel
class DevicesViewModel @Inject constructor(
    private val repository: DeviceRepository,
) : ViewModel() {
    private val _state = MutableStateFlow(DevicesUiState())
    val state: StateFlow<DevicesUiState> = _state.asStateFlow()

    fun load() {
        viewModelScope.launch {
            _state.update { it.copy(loading = true, error = null) }
            try {
                val rows = DeviceRow.from(repository.devices())
                _state.update { it.copy(loading = false, rows = rows) }
            } catch (e: IOException) {
                _state.update { it.copy(loading = false, error = DevicesError.Network) }
            }
        }
    }
}
```

Step 4, the Kotlin Activity renders from the ViewModel:

```kotlin
@AndroidEntryPoint
class DevicesActivity : AppCompatActivity() {
    private val viewModel: DevicesViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
        if (savedInstanceState == null) viewModel.load()
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect(::render)
            }
        }
    }
}
```

The same screen in a Java Activity, while the Activity itself is not yet converted:

```java
// Kotlin side: val stateLiveData = state.asLiveData()  (lifecycle-livedata-ktx)
DevicesViewModel viewModel = new ViewModelProvider(this).get(DevicesViewModel.class);
viewModel.getStateLiveData().observe(this, this::render);
```

Notes:
- The ViewModel survives rotation, so the "load in onCreate" call is guarded or moved into the
  ViewModel's `init`. The rotation bug that MVP had is gone after step 4.
- State that must survive process death (form input, selected tab) goes in `SavedStateHandle`.
- During the migration a Java Activity can host a Kotlin ViewModel; convert the Activity to Kotlin
  separately.
- Do not wrap the old presenter inside a ViewModel to "make it survive rotation". The presenter still
  holds a view reference that is now retained across Activity instances: a leak.

## iOS: UIKit MVC to a ViewModel

Step 3, an observable ViewModel the view controller owns:

```swift
@MainActor @Observable
final class DevicesViewModel {
    private(set) var rows: [DeviceRow] = []
    private(set) var isLoading = false
    private(set) var error: DevicesError?
    private let service: DeviceService

    init(service: DeviceService) { self.service = service }

    func load() async {
        isLoading = true
        defer { isLoading = false }
        do {
            rows = try await service.devices().map(DeviceRow.init)
            error = nil
        } catch is CancellationError {
        } catch {
            self.error = .network
        }
    }
}
```

Step 4, binding the view controller. Pick the option that fits the deployment target:

- iOS 26 and later: UIKit tracks `@Observable` properties read in `updateProperties()` and re-runs it
  when they change.

```swift
override func updateProperties() {
    super.updateProperties()
    apply(viewModel.rows)
    rootView.spinner.isHidden = !viewModel.isLoading
}
```

- Earlier deployment targets: keep the ViewModel as an `ObservableObject` with `@Published` state and
  bind with Combine, or render explicitly after each ViewModel call.

```swift
viewModel.$state
    .receive(on: DispatchQueue.main)
    .sink { [weak self] state in self?.render(state) }
    .store(in: &cancellables)
```

Notes:
- The ViewModel does not import UIKit and does not hold the view controller.
- Navigation leaves through closures to a coordinator, as in [UIKit](uikit.md).
- A migrated screen can later be rendered with SwiftUI inside a `UIHostingController` while the
  coordinator and ViewModel stay the same.

## Flutter: State logic to controller to ViewModel

1. Move logic from the `State` into a `ChangeNotifier` controller, as in [Flutter controllers](flutter.md).
2. Inject the repository instead of constructing clients inside the controller.
3. When the project uses provider, Riverpod or Bloc, expose the controller through it so widgets stop
   owning it. At that point it is a ViewModel; follow `mobile-mvvm` or `mobile-mvi`.

## MR plan for one screen

```text
test(devices): characterization tests for device list formatting and states
refactor(devices): extract DeviceRow formatting from DevicesActivity
refactor(devices): add DevicesViewModel behind DevicesActivity
refactor(devices): render device list from DevicesViewModel state
refactor(devices): route device selection through DevicesViewModel
refactor(devices): remove DevicesPresenter and DevicesContract
```

## Definition of done per screen

- [ ] Characterization tests passed before and after every step
- [ ] Each piece of state has one owner: the ViewModel
- [ ] Controller or Activity contains only view binding, rendering and lifecycle
- [ ] Rotation and process death tested (Android); background and foreground tested (iOS)
- [ ] Old presenter, contract and dead code removed
- [ ] No behaviour change shipped inside a refactor MR
