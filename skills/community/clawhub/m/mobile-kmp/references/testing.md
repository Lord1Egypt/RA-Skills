# Testing reference

Load this when writing tests for shared code, choosing between fakes and mocks in KMP, or running tests on
the Android and iOS targets.

## Source sets and dependencies

| Source set | Runs on | Use for |
|---|---|---|
| `commonTest` | every target (JVM for Android host tests, Kotlin/Native runner for iOS) | domain, repositories, ViewModels, serialization |
| `androidHostTest` | JVM (enable with `withHostTest { }` in `kotlin { android { } }`) | Android implementations, JVM-only tools such as MockK |
| `androidDeviceTest` | device or emulator (`withDeviceTest { }`) | Android-specific database or platform tests |
| `iosTest` | iOS simulator | iOS implementations, Kotlin/Native behaviour |

```kotlin
kotlin {
    sourceSets {
        commonTest.dependencies {
            implementation(libs.kotlin.test)
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.turbine)
            implementation(libs.ktor.client.mock)
        }
    }
}
```

- `kotlin.test` gives `@Test`, `@BeforeTest`, `@AfterTest` and assertions on every target.
- Turbine (`app.cash.turbine:turbine`) is multiplatform, including iOS targets.
- MockK is JVM-only. It may be used in `androidHostTest`, never in `commonTest`.

## Fakes over mocks

```kotlin
// commonTest
class FakeDeviceRepository(
    devices: List<Device> = emptyList(),
    private val failWith: DeviceError? = null,
) : DeviceRepository {
    private val state = MutableStateFlow(devices)
    val refreshCalls = mutableListOf<Unit>()

    override fun observe(): Flow<List<Device>> = state
    override suspend fun refresh(): DeviceResult {
        refreshCalls += Unit
        return failWith?.let { DeviceResult.Failed(it) } ?: DeviceResult.Ok(state.value)
    }
    fun emit(devices: List<Device>) { state.value = devices }
}
```

- A fake is a working, in-memory implementation of the interface the production code depends on. It
  runs on every target and makes the interface design honest.
- Because platform services are interfaces (see Rule 3 in the skill), every platform dependency in
  shared code can be faked this way.

## Coroutines and ViewModels

```kotlin
class DevicesViewModelTest {
    private val dispatcher = StandardTestDispatcher()

    @BeforeTest fun setUp() = Dispatchers.setMain(dispatcher)
    @AfterTest fun tearDown() = Dispatchers.resetMain()

    @Test fun refreshFailureShowsError() = runTest {
        val repo = FakeDeviceRepository(failWith = DeviceError.Offline)
        val vm = DevicesViewModel(repo)

        vm.state.test {
            assertEquals(DevicesUiState.Loading, awaitItem())
            vm.refresh()
            assertEquals(DevicesUiState.Error(DeviceError.Offline), awaitItem())
            cancelAndIgnoreRemainingEvents()
        }
        assertEquals(1, repo.refreshCalls.size)
    }
}
```

- `viewModelScope` uses `Dispatchers.Main.immediate`. Set a test Main dispatcher on every target, or the
  iOS test can hang or fail with no main loop.
- With a `TestDispatcher` set as Main, `runTest` shares its scheduler, so virtual time covers the
  ViewModel's coroutines.
- Inject the IO dispatcher into repositories and pass `StandardTestDispatcher(testScheduler)` in tests.
- Never `delay` for real or sleep in a test. Use `advanceTimeBy`, `advanceUntilIdle` or Turbine.

## Ktor with MockEngine

```kotlin
@Test fun mapsServerErrorToResult() = runTest {
    val engine = MockEngine { request ->
        assertEquals("/readings", request.url.encodedPath)
        respond(
            content = """{"error":"down"}""",
            status = HttpStatusCode.ServiceUnavailable,
            headers = headersOf(HttpHeaders.ContentType, "application/json"),
        )
    }
    val api = ReadingsApi(createHttpClient(engine, appJson, FakeTokenProvider()))

    assertEquals(ReadingsResult.ServerError, api.readings())
}
```

- The client factory takes an engine parameter so the same configuration (timeouts, auth, JSON) is under
  test, not a different client.
- Add serialization tests for every DTO with a captured real payload, including unknown fields and
  unknown enum values.

## Databases

- Room KMP: build an in-memory database per platform through a test-only `expect fun` in `commonTest`
  with actuals in `androidDeviceTest` (or host tests set up for Room) and `iosTest`. Use the bundled
  driver so behaviour matches production.
- Every schema version bump ships a migration test that opens the old schema, migrates and checks the
  data.
- SQLDelight: JVM tests can use `JdbcSqliteDriver(JdbcSqliteDriver.IN_MEMORY)` from
  `app.cash.sqldelight:sqlite-driver`; iOS tests use `NativeSqliteDriver`.

## Running

```sh
./gradlew :shared:allTests                  # every target, combined report for common and iOS tests
./gradlew :shared:iosSimulatorArm64Test     # iOS simulator only
./gradlew :shared:tasks --group verification # find the Android host test task for the project
```

- iOS tests need a macOS host with Xcode. CI must run them on a macOS runner; a Linux-only pipeline
  silently skips the iOS target (see `mobile-ci-cd`).
- The `allTests` report does not include Android test reports; check both.
- Swift-side tests (Swift Testing or XCTest in the iOS app) cover the bridge: a Flow is collected and
  cancelled, a `@Throws` error arrives as a Swift `Error`, a sealed type switch is exhaustive.

## Checklist for a shared change

- [ ] New domain and data logic has `commonTest` tests with fakes
- [ ] ViewModel tests set a test Main dispatcher and use Turbine
- [ ] Network code tested through `MockEngine` with the production client configuration
- [ ] DTO round-trip and unknown-field tests
- [ ] Migration test for every database version bump
- [ ] `allTests` passes, iOS simulator included
