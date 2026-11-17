# MVVM with Java, LiveData, XML and ViewBinding (legacy)

Load this when maintaining Java screens. New screens should be Kotlin + Compose (see
[the Kotlin reference](kotlin.md)); this file shows how to keep legacy code correct until it is migrated.

The feature is the same device list: observe devices, refresh, "online only" filter that survives process
death, and a message when refresh fails.

## Contract

```java
public interface DeviceRepository {
    LiveData<List<Device>> observeDevices();          // for example a Room DAO returning LiveData

    /** Callbacks are delivered on the main thread. */
    Cancellable refresh(Callback callback);

    interface Callback {
        void onSuccess();
        void onError(@NonNull IOException error);
    }

    interface Cancellable {
        void cancel();
    }
}
```

- The repository runs IO on its own `ExecutorService` and posts results to the main thread, so the
  ViewModel only uses `setValue` and never races on read-modify-write.

## UI state

```java
public enum UserMessage { REFRESH_FAILED }

public final class DeviceListUiState {
    public final List<Device> devices;
    public final boolean onlineOnly;
    public final boolean isRefreshing;
    @Nullable public final UserMessage userMessage;

    public DeviceListUiState(List<Device> devices, boolean onlineOnly, boolean isRefreshing,
                             @Nullable UserMessage userMessage) {
        this.devices = Collections.unmodifiableList(new ArrayList<>(devices));
        this.onlineOnly = onlineOnly;
        this.isRefreshing = isRefreshing;
        this.userMessage = userMessage;
    }
}
```

- Immutable fields and an unmodifiable list. Override `equals` and `hashCode` if the state is compared
  (tests, `distinctUntilChanged`).

## ViewModel

```java
@HiltViewModel
public final class DeviceListViewModel extends ViewModel {

    static final String KEY_ONLINE_ONLY = "online_only";

    private final DeviceRepository repository;
    private final SavedStateHandle savedStateHandle;
    private final MediatorLiveData<DeviceListUiState> uiState = new MediatorLiveData<>();

    private List<Device> allDevices = Collections.emptyList();
    private boolean onlineOnly;
    private boolean isRefreshing;
    @Nullable private UserMessage userMessage;
    @Nullable private DeviceRepository.Cancellable inFlight;

    @Inject
    public DeviceListViewModel(DeviceRepository repository, SavedStateHandle savedStateHandle) {
        this.repository = repository;
        this.savedStateHandle = savedStateHandle;
        uiState.addSource(repository.observeDevices(), devices -> {
            allDevices = devices;
            publish();
        });
        uiState.addSource(savedStateHandle.getLiveData(KEY_ONLINE_ONLY, false), value -> {
            onlineOnly = value;
            publish();
        });
    }

    public LiveData<DeviceListUiState> getUiState() {
        return uiState;
    }

    public void refresh() {
        if (isRefreshing) return;
        isRefreshing = true;
        publish();
        inFlight = repository.refresh(new DeviceRepository.Callback() {
            @Override public void onSuccess() {
                isRefreshing = false;
                publish();
            }

            @Override public void onError(@NonNull IOException error) {
                isRefreshing = false;
                userMessage = UserMessage.REFRESH_FAILED;
                publish();
            }
        });
    }

    public void setOnlineOnly(boolean value) {
        if (value != onlineOnly) savedStateHandle.set(KEY_ONLINE_ONLY, value);
    }

    public void userMessageShown() {
        userMessage = null;
        publish();
    }

    private void publish() {
        List<Device> visible = new ArrayList<>();
        for (Device device : allDevices) {
            if (!onlineOnly || device.isOnline()) visible.add(device);
        }
        uiState.setValue(new DeviceListUiState(visible, onlineOnly, isRefreshing, userMessage));
    }

    @Override
    protected void onCleared() {
        if (inFlight != null) inFlight.cancel();
    }
}
```

Notes:
- `MediatorLiveData` observes its sources only while it has an active observer, so it follows the
  Fragment's view lifecycle automatically.
- The anonymous callback holds the ViewModel, not the Fragment, and is cancelled in `onCleared()`.
- No `SingleLiveEvent`: the message is state, cleared by `userMessageShown()`.

## Fragment

```java
@AndroidEntryPoint
public final class DeviceListFragment extends Fragment {

    @Nullable private FragmentDeviceListBinding binding;
    private DeviceListViewModel viewModel;
    private final DeviceAdapter adapter = new DeviceAdapter(); // ListAdapter with a DiffUtil.ItemCallback

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentDeviceListBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        viewModel = new ViewModelProvider(this).get(DeviceListViewModel.class);
        binding.list.setAdapter(adapter);
        binding.swipeRefresh.setOnRefreshListener(viewModel::refresh);
        binding.onlineOnly.setOnCheckedChangeListener((button, checked) -> viewModel.setOnlineOnly(checked));
        viewModel.getUiState().observe(getViewLifecycleOwner(), this::render);
    }

    private void render(DeviceListUiState state) {
        adapter.submitList(state.devices);
        binding.swipeRefresh.setRefreshing(state.isRefreshing);
        if (binding.onlineOnly.isChecked() != state.onlineOnly) {
            binding.onlineOnly.setChecked(state.onlineOnly);
        }
        if (state.userMessage == UserMessage.REFRESH_FAILED) {
            Snackbar.make(binding.getRoot(), R.string.devices_refresh_failed, Snackbar.LENGTH_SHORT).show();
            viewModel.userMessageShown();
        }
    }

    @Override
    public void onDestroyView() {
        binding = null;
        super.onDestroyView();
    }
}
```

- `getViewLifecycleOwner()`, not `this`, so observers do not pile up after back navigation.
- `render` is idempotent: it sets every view from state, guarding listeners that would echo back.
- The binding is cleared in `onDestroyView` to avoid leaking the view hierarchy.

## Tests

```java
public class DeviceListViewModelTest {

    @Rule public InstantTaskExecutorRule instantTaskExecutorRule = new InstantTaskExecutorRule();

    private final FakeDeviceRepository repository = new FakeDeviceRepository();
    private final Observer<DeviceListUiState> observer = state -> { };
    private DeviceListViewModel viewModel;

    @Before
    public void setUp() {
        viewModel = new DeviceListViewModel(repository, new SavedStateHandle());
        viewModel.getUiState().observeForever(observer); // MediatorLiveData needs an active observer
    }

    @After
    public void tearDown() {
        viewModel.getUiState().removeObserver(observer);
    }

    @Test
    public void refreshFailureShowsMessageUntilAcknowledged() {
        repository.nextRefreshError = new IOException("offline");

        viewModel.refresh();

        DeviceListUiState state = viewModel.getUiState().getValue();
        assertEquals(UserMessage.REFRESH_FAILED, state.userMessage);
        assertFalse(state.isRefreshing);

        viewModel.userMessageShown();
        assertNull(viewModel.getUiState().getValue().userMessage);
    }

    @Test
    public void onlineOnlyHidesOfflineDevices() {
        repository.devices.setValue(Arrays.asList(Devices.ONLINE, Devices.OFFLINE));

        viewModel.setOnlineOnly(true);

        assertEquals(Collections.singletonList(Devices.ONLINE), viewModel.getUiState().getValue().devices);
    }
}

final class FakeDeviceRepository implements DeviceRepository {
    final MutableLiveData<List<Device>> devices = new MutableLiveData<>(Collections.emptyList());
    @Nullable IOException nextRefreshError;

    @Override public LiveData<List<Device>> observeDevices() { return devices; }

    @Override public Cancellable refresh(Callback callback) {
        if (nextRefreshError != null) callback.onError(nextRefreshError); else callback.onSuccess();
        return () -> { };
    }
}
```

- `Devices.ONLINE` and `Devices.OFFLINE` are test fixtures (one online, one offline `Device`).
- `InstantTaskExecutorRule` (from `androidx.arch.core:core-testing`) runs LiveData work synchronously.
- The fake calls back synchronously, matching the "main thread" contract without real executors.

## Migration path to Kotlin

1. Convert the state class to a Kotlin `data class`; Java callers keep working.
2. Convert the ViewModel; expose `StateFlow` and, for remaining Java Fragments, `uiState.asLiveData()`.
3. Replace the Fragment with a Compose screen hosted in the same navigation graph.
4. Delete the `LiveData` bridge when no Java observer is left.
