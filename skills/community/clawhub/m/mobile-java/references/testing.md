# Testing Java Android code

Load this when writing or fixing tests for Java classes: ViewModels with `LiveData`, repositories with
executors, and Espresso UI tests.

## Setup

| Test type | Runs on | Typical libraries |
|---|---|---|
| Local unit (`src/test`) | Desktop JVM | JUnit 4 or 5, Mockito, `androidx.arch.core:core-testing`, Robolectric when framework classes are needed |
| Instrumented (`src/androidTest`) | Device or emulator | AndroidX Test (`AndroidJUnit4`), Espresso, `mockito-android`, Hilt testing |

- JUnit 4 is the default for both. JUnit 5 (Jupiter) for local tests requires the Gradle test task to use the
  JUnit Platform. Instrumented tests stay on JUnit 4 unless a third-party plugin is added.
- `InstantTaskExecutorRule` is a JUnit 4 rule. With Jupiter, keep LiveData tests on JUnit 4 through the
  vintage engine, or write an equivalent extension.
- Dependency versions live in `libs.versions.toml`.

## ViewModel with LiveData and an executor

Production code takes its executor as a constructor parameter, so tests can run work synchronously.

```java
/** Runs every task on the calling thread. AbstractExecutorService.submit wraps tasks and calls execute. */
final class DirectExecutorService extends AbstractExecutorService {
    private volatile boolean shutdown;

    @Override public void execute(Runnable command) { command.run(); }
    @Override public void shutdown() { shutdown = true; }
    @Override public List<Runnable> shutdownNow() { shutdown = true; return Collections.emptyList(); }
    @Override public boolean isShutdown() { return shutdown; }
    @Override public boolean isTerminated() { return shutdown; }
    @Override public boolean awaitTermination(long timeout, TimeUnit unit) { return true; }
}
```

```java
public class DevicesViewModelTest {

    @Rule public InstantTaskExecutorRule liveData = new InstantTaskExecutorRule();

    private final DeviceRepository repo = mock(DeviceRepository.class);

    @Test
    public void load_success_emitsLoaded() throws Exception {
        List<Device> devices = Collections.singletonList(new Device("1", "Gateway", Collections.emptyList()));
        when(repo.devices()).thenReturn(devices);
        DevicesViewModel vm = new DevicesViewModel(repo, new DirectExecutorService());

        vm.load();

        assertEquals(UiState.loaded(devices), vm.getState().getValue());
    }

    @Test
    public void load_ioError_emitsError() throws Exception {
        when(repo.devices()).thenThrow(new IOException("offline"));
        DevicesViewModel vm = new DevicesViewModel(repo, new DirectExecutorService());

        vm.load();

        assertEquals(UiState.error(), vm.getState().getValue());
    }
}
```

- With `InstantTaskExecutorRule`, `postValue` delivers immediately, so `getValue()` is up to date.
- To assert a sequence of states, record them with an observer:

```java
List<UiState> seen = new ArrayList<>();
Observer<UiState> observer = seen::add;
vm.getState().observeForever(observer);
try {
    vm.load();
    assertEquals(Arrays.asList(UiState.loading(), UiState.loaded(devices)), seen);
} finally {
    vm.getState().removeObserver(observer);
}
```

`UiState` needs `equals` / `hashCode` (a record works) for these assertions.

## Mockito

- `mockito-core` for local tests, `mockito-android` for instrumented tests. Mockito 5 uses the inline mock
  maker by default, so final classes and records can be mocked; prefer not to.
- Fakes beat mocks for repositories and data sources: a small in-memory implementation is easier to read
  and does not break on refactors.
- Mock only what the class under test talks to directly. Never mock value types.
- `verify(repo).refresh()` for interactions that are the behaviour under test; otherwise assert on state.
- `ArgumentCaptor` for arguments built inside the class under test.

## Framework classes in local tests

- Code that touches `Context`, resources or `SharedPreferences` runs under Robolectric with
  `@RunWith(AndroidJUnit4.class)` and `unitTests.isIncludeAndroidResources = true` in the Gradle test options.
- Better still, keep framework calls at the edges so most logic needs no Android classes at all.

## Espresso

```java
@RunWith(AndroidJUnit4.class)
public class DevicesScreenTest {

    @Rule public ActivityScenarioRule<MainActivity> activity = new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void refresh_showsDevices() {
        onView(withId(R.id.refresh)).perform(click());
        onView(withText("Gateway")).check(matches(isDisplayed()));
    }
}
```

- Espresso waits for the main thread and `AsyncTask` pool only. Work on your own executors needs an
  `IdlingResource`, or Espresso asserts before the data arrives.
- Never `Thread.sleep` in UI tests. It is slow on fast devices and flaky on slow ones.

```java
// Debug or test source set: counts in-flight background work
public final class BackgroundWork {
    public static final CountingIdlingResource IDLING = new CountingIdlingResource("background-work");
    private BackgroundWork() {}
}

// Around asynchronous work in the code under test
BackgroundWork.IDLING.increment();
io.execute(() -> {
    try {
        state.postValue(UiState.loaded(repo.devices()));
    } catch (IOException e) {
        state.postValue(UiState.error());
    } finally {
        BackgroundWork.IDLING.decrement();
    }
});

// Test
@Before public void registerIdling() { IdlingRegistry.getInstance().register(BackgroundWork.IDLING); }
@After public void unregisterIdling() { IdlingRegistry.getInstance().unregister(BackgroundWork.IDLING); }
```

- Cleaner alternative with Hilt: replace the production executor module in tests (`@TestInstallIn` or
  `@UninstallModules`) with one whose executor Espresso can track.
- Lists: `RecyclerViewActions` from `espresso-contrib` to scroll to or click items by position or matcher.
- Fragments in isolation: `FragmentScenario` from `fragment-testing`. Hilt fragments need a Hilt-enabled
  host activity in the debug source set.

## Hilt in instrumented tests

```java
@HiltAndroidTest
public class SyncFlowTest {
    @Rule public HiltAndroidRule hilt = new HiltAndroidRule(this);

    @Before public void setUp() { hilt.inject(); }
}
```

The instrumentation runner must start `HiltTestApplication` (a custom `AndroidJUnitRunner` that overrides
`newApplication`).

## What to test first in legacy Java

1. Pure logic hidden in Activities and Fragments: extract it into plain classes, then unit test.
2. Parsers and mappers (DTOs, byte frames, CRC checks) with table-driven tests including malformed input.
3. ViewModel state transitions for success, error and cancellation.
4. One Espresso smoke test per critical flow, not per screen detail.
