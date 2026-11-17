# Android legacy: Activity as controller and MVP

Load this when the screen is a Java or Kotlin `Activity` or `Fragment` with logic in it, or uses an MVP
presenter. New Android screens should use MVVM with Compose; this reference is for maintaining and
migrating what exists.

## Symptoms of a god Activity

- `onCreate` longer than one screen; network calls, SQL and string formatting inline.
- State in fields that is lost on rotation, or saved field by field in `onSaveInstanceState`.
- `AsyncTask`, raw `Thread`, or `Handler` callbacks that touch views after `onDestroy`.
- `onActivityResult` with a switch over request codes for camera, permissions and other screens.

## MVP contract

One contract per screen. The view interface is what the presenter may ask of the UI; the presenter
interface is what the UI reports.

Java:
```java
public interface DevicesContract {
    interface View {
        void showLoading(boolean loading);
        void showDevices(List<DeviceRow> rows);
        void showError(@StringRes int message);
        void openDetail(String deviceId);
    }

    interface Presenter {
        void attach(View view);
        void detach();
        void loadDevices();
        void onDeviceClicked(String deviceId);
    }
}
```

`@StringRes` is an annotation from `androidx.annotation`, which is acceptable in a presenter; avoid
anything that needs a `Context`.

## Presenter with lifecycle-safe callbacks

Java:
```java
public final class DevicesPresenter implements DevicesContract.Presenter {
    private final DeviceRepository repository;
    @Nullable private DevicesContract.View view;
    @Nullable private Cancellable pending;

    public DevicesPresenter(DeviceRepository repository) {
        this.repository = repository;
    }

    @Override public void attach(DevicesContract.View view) { this.view = view; }

    @Override public void detach() {
        view = null;
        if (pending != null) pending.cancel();
    }

    @Override public void loadDevices() {
        if (view != null) view.showLoading(true);
        pending = repository.loadDevices(new Callback<List<Device>>() {
            @Override public void onSuccess(List<Device> devices) {
                if (view == null) return;
                view.showLoading(false);
                view.showDevices(DeviceRow.from(devices));
            }
            @Override public void onError(Throwable error) {
                if (view == null) return;
                view.showLoading(false);
                view.showError(R.string.devices_error);
            }
        });
    }

    @Override public void onDeviceClicked(String deviceId) {
        if (view != null) view.openDetail(deviceId);
    }
}
```

`Cancellable` and `Callback` stand for whatever the project's repository returns. The point is that
detach both drops the view and cancels the work.

Callbacks from a repository may arrive on a background thread. Either the repository posts to the main
thread, or the presenter does; never call view methods from a worker thread.

Kotlin presenter with coroutines:
```kotlin
class DevicesPresenter(
    private val repository: DeviceRepository,
    mainDispatcher: CoroutineDispatcher,
) : DevicesContract.Presenter {
    private val scope = CoroutineScope(SupervisorJob() + mainDispatcher)
    private var view: DevicesContract.View? = null

    override fun attach(view: DevicesContract.View) { this.view = view }

    override fun detach() {
        view = null
        scope.coroutineContext.cancelChildren()
    }

    override fun loadDevices() {
        scope.launch {
            view?.showLoading(true)
            val result = runCatchingNonCancellable { repository.devices() }
            view?.showLoading(false)
            result.onSuccess { view?.showDevices(DeviceRow.from(it)) }
                .onFailure { view?.showError(R.string.devices_error) }
        }
    }
}
```

`runCatchingNonCancellable` stands for a project helper that rethrows `CancellationException`; plain
`runCatching` around suspend calls swallows cancellation.

## Wiring in the Activity and Fragment

Java Activity:
```java
@Override protected void onCreate(@Nullable Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    binding = ActivityDevicesBinding.inflate(getLayoutInflater());
    setContentView(binding.getRoot());
    presenter.attach(this);
    presenter.loadDevices();
}

@Override protected void onDestroy() {
    presenter.detach();
    super.onDestroy();
}
```

Fragment: attach in `onViewCreated`, detach in `onDestroyView`, and clear the view binding there too.
The fragment instance outlives its view, so `onDestroy` is too late.

Limitations to state in reviews: an MVP presenter created in `onCreate` is recreated on rotation, so
in-flight work and loaded data are lost. This is the most common reason to migrate the screen to a
ViewModel (see [migration to MVVM](migration-to-mvvm.md)).

## Deprecated APIs to replace while touching legacy screens

| Legacy | Replacement |
|---|---|
| `AsyncTask` | Coroutines in a ViewModel, or an executor owned by a lifecycle-aware component |
| Loaders (`LoaderManager`) | ViewModel with `StateFlow` or `LiveData` |
| `startActivityForResult` / `onActivityResult` | `registerForActivityResult` with an `ActivityResultContract` |
| `requestPermissions` / `onRequestPermissionsResult` | `ActivityResultContracts.RequestPermission` |
| `onBackPressed()` override | `OnBackPressedCallback` on `onBackPressedDispatcher` |
| `Handler()` with no Looper | `Handler(Looper.getMainLooper())`, or coroutines |
| Kotlin synthetics (`kotlin-android-extensions`) | View Binding |
| `ProgressDialog` | An inline progress indicator in the layout |

- Back handling: with predictive back enabled (the default when targeting Android 16), `onBackPressed()`
  is not called. Legacy screens that override it must move to `OnBackPressedCallback`.
- Orientation: when targeting Android 16, large-screen devices ignore orientation locks and
  resizability restrictions. A legacy Activity that locked portrait to avoid losing state on rotation
  will now lose it on tablets and foldables. Fix the state handling, do not rely on the lock.

## Testing presenters

```kotlin
@Test fun `shows devices after load`() = runTest {
    val view = mockk<DevicesContract.View>(relaxed = true)
    val presenter = DevicesPresenter(FakeDeviceRepository(listOf(device)), StandardTestDispatcher(testScheduler))
    presenter.attach(view)

    presenter.loadDevices()
    advanceUntilIdle()

    verifyOrder {
        view.showLoading(true)
        view.showLoading(false)
        view.showDevices(DeviceRow.from(listOf(device)))
    }
}

@Test fun `no view calls after detach`() = runTest {
    val view = mockk<DevicesContract.View>(relaxed = true)
    val presenter = DevicesPresenter(SlowDeviceRepository(), StandardTestDispatcher(testScheduler))
    presenter.attach(view)
    presenter.loadDevices()
    presenter.detach()
    advanceUntilIdle()

    verify(exactly = 0) { view.showDevices(any()) }
}
```

The second test is the leak guard: it fails if detach does not cancel the work.
