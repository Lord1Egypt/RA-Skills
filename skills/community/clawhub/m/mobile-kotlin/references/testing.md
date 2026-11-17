# Testing reference

Load this when writing unit tests for ViewModels, use cases, repositories and flows, or UI tests for
composables and Room migrations.

## What to test where

| Code | Test type | Source set |
|---|---|---|
| Use cases, mappers, validators | Plain JUnit | `test` |
| ViewModels, repositories, flows | JUnit + `kotlinx-coroutines-test` + Turbine | `test` |
| Composables (behavior) | Compose UI test (instrumented, or JVM with Robolectric) | `androidTest` or `test` |
| Room DAOs and migrations | Instrumented with an in-memory DB and `MigrationTestHelper` | `androidTest` |

## Main dispatcher rule

`viewModelScope` uses `Dispatchers.Main`, which does not exist on the JVM. Replace it per test:

```kotlin
class MainDispatcherRule(
    val testDispatcher: TestDispatcher = StandardTestDispatcher(),
) : TestWatcher() {
    override fun starting(description: Description) = Dispatchers.setMain(testDispatcher)
    override fun finished(description: Description) = Dispatchers.resetMain()
}
```

- With `StandardTestDispatcher`, launched coroutines run only when the scheduler advances
  (`advanceUntilIdle()`, `runCurrent()`, or a suspending call such as `awaitItem()`).
- `UnconfinedTestDispatcher` runs eagerly. Use it when a test needs `stateIn` collectors to start immediately,
  not as a default to hide ordering problems.
- Inject the same scheduler into code under test:
  `Repo(io = StandardTestDispatcher(testScheduler))` inside `runTest`, so virtual time is shared.

## ViewModel test with a fake and Turbine

```kotlin
class DevicesViewModelTest {
    @get:Rule val mainRule = MainDispatcherRule()

    private val repository = FakeDeviceRepository()

    @Test
    fun `filters devices by query`() = runTest {
        repository.emit(listOf(device("Gateway A"), device("Sensor B")))
        val vm = DevicesViewModel(repository, ConnectDeviceUseCase(repository))

        vm.state.test {
            assertEquals(DevicesUiState(), awaitItem()) // stateIn initial value
            assertEquals(2, awaitItem().devices.size)
            vm.onQueryChange("gate")
            assertEquals(listOf("Gateway A"), awaitItem().devices.map { it.name })
            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

- The first `awaitItem()` on a `StateFlow` may be the initial value. Assert it or skip it explicitly; do not
  rely on timing.
- `expectNoEvents()` to prove nothing else was emitted; `awaitError()` for failing flows.
- `turbineScope { }` with `testIn(backgroundScope)` when asserting several flows together.

## Fakes vs mocks

- Prefer fakes for repositories and data sources: a small class backed by a `MutableStateFlow`. They test
  behavior and survive refactors.
- Use MockK for collaborators that are hard to fake, or to verify an interaction that is the behavior itself.

```kotlin
private val api = mockk<DeviceApi>()

@Test
fun `maps network failure to domain error`() = runTest {
    coEvery { api.devices() } throws IOException("offline")
    val repo = NetworkDeviceRepository(api, io = StandardTestDispatcher(testScheduler))

    val result = repo.refresh()

    assertEquals(RefreshResult.Failure(DeviceError.Network), result)
    coVerify(exactly = 1) { api.devices() }
}
```

- `coEvery` / `coVerify` for suspend functions; `every` / `verify` for regular ones.
- `relaxed = true` hides missing stubs. Use it only for collaborators whose return value does not matter.
- Do not mock types you own just to return data. Write a fake.
- Do not mock data classes or value classes.

## Time and delays

```kotlin
@Test
fun `retries after backoff`() = runTest {
    val api = FlakyApi(failures = 1)
    val repo = Repo(api, io = StandardTestDispatcher(testScheduler))

    val result = async { repo.loadWithRetry() }
    advanceTimeBy(1_000)
    runCurrent()

    assertEquals(expected, result.await())
}
```

- `runTest` skips `delay` with virtual time. Never `Thread.sleep` in a test.
- `runTest` waits for every child coroutine. A collector that never completes makes the test fail on timeout,
  which surfaces leaked work; launch such collectors in `backgroundScope`.

## Compose UI tests

Use the v2 test APIs (`androidx.compose.ui.test.junit4.v2`, ui-test 1.11 and later). The v1 factories in
`androidx.compose.ui.test.junit4` are deprecated.

```kotlin
import androidx.compose.ui.test.junit4.v2.createComposeRule

class DevicesScreenTest {
    @get:Rule val composeRule = createComposeRule()

    @Test
    fun clickingDeviceReportsId() {
        var clicked: DeviceId? = null
        composeRule.setContent {
            AppTheme {
                DevicesScreen(
                    state = DevicesUiState(devices = persistentListOf(deviceUi("Gateway A"))),
                    onQueryChange = {},
                    onDeviceClick = { clicked = it },
                )
            }
        }

        composeRule.onNodeWithText("Gateway A").performClick()

        assertEquals(DeviceId("gateway-a"), clicked)
    }
}
```

- Test the stateless screen with plain state and lambdas. No ViewModel, no Hilt, no network.
- Find nodes by semantics: `onNodeWithText`, `onNodeWithContentDescription`, `onNodeWithTag` as a last resort.
- Assertions: `assertIsDisplayed()`, `assertIsEnabled()`, `assertTextEquals()`, `assertCountEquals()` on
  `onAllNodes...`.
- `createAndroidComposeRule<MainActivity>()` only when the test needs the Activity (resources, Hilt entry
  point). With Hilt, add `@HiltAndroidTest` and `HiltAndroidRule` ordered before the compose rule.
- The rule waits for idle. Use `waitUntil { }` for asynchronous conditions instead of sleeps.
- v2 runs composition coroutines on `StandardTestDispatcher`: launched work is queued, not run immediately.
  Call `composeRule.waitForIdle()` or assert inside `runOnIdle { }` after triggering work. For tests that
  also need coroutine control, prefer `runComposeUiTest { }` over mixing the rule with `runTest`, which
  creates two clocks.

## Room

```kotlin
@get:Rule
val helper = MigrationTestHelper(
    InstrumentationRegistry.getInstrumentation(),
    AppDb::class.java,
)

@Test
fun migrate2To3() {
    helper.createDatabase(TEST_DB, 2).use { db ->
        db.execSQL("INSERT INTO device (id, serial, name) VALUES ('1', 'S1', 'A')")
    }
    helper.runMigrationsAndValidate(TEST_DB, 3, true, MIGRATION_2_3)
}
```

- DAO tests use `Room.inMemoryDatabaseBuilder(...)` and close the database in `@After`.
- Migration tests need the exported schema JSON files available to the test APK.

## Test hygiene

- Test names describe behavior: `` `emits error when token expired` ``.
- One behavior per test; arrange, act, assert separated by blank lines.
- No shared mutable state between tests; build fresh fakes per test.
- New domain and data logic ships with tests in the same change.
