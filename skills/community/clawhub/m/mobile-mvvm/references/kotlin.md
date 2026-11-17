# MVVM with Kotlin, Jetpack Compose and Hilt

Load this when building or reviewing a Kotlin ViewModel and Compose screen. Assumes Kotlin 2.x,
Compose with strong skipping, AndroidX Lifecycle 2.8 or newer, Hilt and Turbine in tests.

The feature: a device list that observes devices from a repository, supports pull to refresh,
an "online only" filter that survives process death, favorites, and a snackbar when refresh fails.

## Domain and data contract

```kotlin
data class Device(
    val id: String,
    val name: String,
    val isOnline: Boolean,
    val isFavorite: Boolean,
)

interface DeviceRepository {
    fun observeDevices(): Flow<List<Device>>
    suspend fun refresh()
    suspend fun setFavorite(id: String, favorite: Boolean)
}
```

- The repository implementation owns its dispatcher, caching and DTO mapping. The ViewModel never sees them.

## UI state

```kotlin
enum class UserMessage { RefreshFailed, FavoriteFailed }

data class DeviceListUiState(
    val devices: List<Device> = emptyList(),
    val onlineOnly: Boolean = false,
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val userMessage: UserMessage? = null,
) {
    val isEmpty: Boolean get() = !isLoading && devices.isEmpty()
}
```

- `List<Device>` is unstable for the Compose compiler. With strong skipping it is compared by instance,
  which is fine because each state copy is a new object only when something changed. Use
  `kotlinx.collections.immutable` if profiling shows extra recompositions.

## ViewModel

```kotlin
@HiltViewModel
class DeviceListViewModel @Inject constructor(
    private val repository: DeviceRepository,
    private val savedStateHandle: SavedStateHandle,
) : ViewModel() {

    private val onlineOnly = savedStateHandle.getStateFlow(KEY_ONLINE_ONLY, false)
    private val isRefreshing = MutableStateFlow(false)
    private val userMessage = MutableStateFlow<UserMessage?>(null)

    val uiState: StateFlow<DeviceListUiState> = combine(
        repository.observeDevices(),
        onlineOnly,
        isRefreshing,
        userMessage,
    ) { devices, onlineOnly, refreshing, message ->
        DeviceListUiState(
            devices = if (onlineOnly) devices.filter { it.isOnline } else devices,
            onlineOnly = onlineOnly,
            isRefreshing = refreshing,
            userMessage = message,
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = DeviceListUiState(isLoading = true),
    )

    fun onRefresh() {
        if (isRefreshing.value) return
        viewModelScope.launch {
            isRefreshing.value = true
            try {
                repository.refresh()
            } catch (e: IOException) {
                userMessage.value = UserMessage.RefreshFailed
            } finally {
                isRefreshing.value = false
            }
        }
    }

    fun onToggleOnlineOnly() {
        savedStateHandle[KEY_ONLINE_ONLY] = !onlineOnly.value
    }

    fun onFavoriteClick(device: Device) {
        viewModelScope.launch {
            try {
                repository.setFavorite(device.id, !device.isFavorite)
            } catch (e: IOException) {
                userMessage.value = UserMessage.FavoriteFailed
            }
        }
    }

    fun onUserMessageShown() {
        userMessage.value = null
    }

    companion object {
        internal const val KEY_ONLINE_ONLY = "online_only"
    }
}
```

Notes:
- Local UI flags (`isRefreshing`, `userMessage`) are small private flows combined with repository data,
  so there is still exactly one public state.
- The favorite toggle writes to the repository; the observed flow updates the list. No manual copy of the list.
- `IOException` stands in for the domain error type the repository throws. Never catch `Exception`
  around suspend calls without rethrowing `CancellationException`.

## Passing navigation arguments

- With type-safe Navigation Compose routes, read them from `SavedStateHandle` (`savedStateHandle.toRoute<T>()`).
- With Navigation 3, where the app holds the back stack and the key, pass the key into the ViewModel with
  Hilt assisted injection (`@AssistedInject`, `@AssistedFactory`, `@HiltViewModel(assistedFactory = ...)`)
  and create it with `hiltViewModel<VM, VM.Factory> { factory -> factory.create(key) }`.
- Never pass arguments through a setter the UI calls after creation; it runs again on recomposition and
  is skipped after process death.

## Screen

```kotlin
@Composable
fun DeviceListRoute(
    onDeviceClick: (String) -> Unit,
    viewModel: DeviceListViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    DeviceListScreen(
        state = uiState,
        onRefresh = viewModel::onRefresh,
        onToggleOnlineOnly = viewModel::onToggleOnlineOnly,
        onFavoriteClick = viewModel::onFavoriteClick,
        onDeviceClick = onDeviceClick,
        onUserMessageShown = viewModel::onUserMessageShown,
    )
}

@Composable
fun DeviceListScreen(
    state: DeviceListUiState,
    onRefresh: () -> Unit,
    onToggleOnlineOnly: () -> Unit,
    onFavoriteClick: (Device) -> Unit,
    onDeviceClick: (String) -> Unit,
    onUserMessageShown: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val snackbarHostState = remember { SnackbarHostState() }

    state.userMessage?.let { message ->
        val text = message.toText()
        LaunchedEffect(message) {
            snackbarHostState.showSnackbar(text)
            onUserMessageShown()
        }
    }

    Scaffold(modifier = modifier, snackbarHost = { SnackbarHost(snackbarHostState) }) { padding ->
        PullToRefreshBox(
            isRefreshing = state.isRefreshing,
            onRefresh = onRefresh,
            modifier = Modifier.padding(padding),
        ) {
            when {
                state.isLoading -> CircularProgressIndicator()
                state.isEmpty -> Text(stringResource(R.string.devices_empty))
                else -> LazyColumn {
                    item {
                        FilterRow(checked = state.onlineOnly, onCheckedChange = { onToggleOnlineOnly() })
                    }
                    items(state.devices, key = { it.id }) { device ->
                        DeviceRow(
                            device = device,
                            onClick = { onDeviceClick(device.id) },
                            onFavoriteClick = { onFavoriteClick(device) },
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun UserMessage.toText(): String = when (this) {
    UserMessage.RefreshFailed -> stringResource(R.string.devices_refresh_failed)
    UserMessage.FavoriteFailed -> stringResource(R.string.devices_favorite_failed)
}
```

- `DeviceListScreen` has no ViewModel parameter, so previews and screenshot tests pass fake states.
- The snackbar is cleared only after it was shown. Rotation while it is visible shows it again instead
  of losing it.
- Navigation on click needs no ViewModel round trip when there is no logic; the route receives a lambda.

## Tests

```kotlin
class MainDispatcherRule(
    private val dispatcher: TestDispatcher = UnconfinedTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(dispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}

class FakeDeviceRepository : DeviceRepository {
    val devices = MutableStateFlow<List<Device>>(emptyList())
    var refreshError: IOException? = null

    override fun observeDevices(): Flow<List<Device>> = devices
    override suspend fun refresh() {
        refreshError?.let { throw it }
    }
    override suspend fun setFavorite(id: String, favorite: Boolean) {
        devices.update { list -> list.map { if (it.id == id) it.copy(isFavorite = favorite) else it } }
    }
}

class DeviceListViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()

    private val repository = FakeDeviceRepository()
    private val online = Device("1", "Gateway", isOnline = true, isFavorite = false)
    private val offline = Device("2", "Sensor", isOnline = false, isFavorite = false)

    @Test
    fun `online only filter hides offline devices and is saved`() = runTest {
        val handle = SavedStateHandle()
        val viewModel = DeviceListViewModel(repository, handle)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect() }
        repository.devices.value = listOf(online, offline)

        viewModel.onToggleOnlineOnly()

        assertEquals(listOf(online), viewModel.uiState.value.devices)
        assertEquals(true, handle.get<Boolean>(DeviceListViewModel.KEY_ONLINE_ONLY))
    }

    @Test
    fun `filter is restored after process death`() = runTest {
        val handle = SavedStateHandle(mapOf(DeviceListViewModel.KEY_ONLINE_ONLY to true))
        val viewModel = DeviceListViewModel(repository, handle)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect() }
        repository.devices.value = listOf(online, offline)

        assertTrue(viewModel.uiState.value.onlineOnly)
        assertEquals(listOf(online), viewModel.uiState.value.devices)
    }

    @Test
    fun `refresh failure shows message until acknowledged`() = runTest {
        repository.refreshError = IOException("offline")
        val viewModel = DeviceListViewModel(repository, SavedStateHandle())

        viewModel.uiState.test {
            viewModel.onRefresh()
            advanceUntilIdle()
            val failed = expectMostRecentItem()
            assertEquals(UserMessage.RefreshFailed, failed.userMessage)
            assertFalse(failed.isRefreshing)

            viewModel.onUserMessageShown()
            assertNull(awaitItem().userMessage)
        }
    }

    @Test
    fun `favorite click updates the observed list`() = runTest {
        val viewModel = DeviceListViewModel(repository, SavedStateHandle())
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect() }
        repository.devices.value = listOf(online)

        viewModel.onFavoriteClick(online)

        assertTrue(viewModel.uiState.value.devices.single().isFavorite)
    }
}
```

- `stateIn` with `WhileSubscribed` does nothing until someone collects. Either collect in `backgroundScope`
  and read `.value`, or use Turbine's `test {}`.
- When `Dispatchers.Main` is a `TestDispatcher`, `runTest` shares its scheduler, so `advanceUntilIdle()`
  also drives `viewModelScope`.
- `SavedStateHandle()` and `SavedStateHandle(map)` work in plain JVM tests; no Robolectric needed.
