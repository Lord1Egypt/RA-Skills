---
name: mobile-testing
description: "Plans, writes and reviews test strategies for Android, iOS and Flutter apps: mobile test pyramid, fakes over mocks, virtual time, Compose UI tests, XCUITest, Flutter integration_test, screenshot tests with Roborazzi, Paparazzi, swift-snapshot-testing and goldens, flaky-test quarantine, coverage that matters and CI sharding. Use when deciding what to test where, writing a test plan, fixing flaky or slow suites, or reviewing tests."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile testing

Decide what to test at which layer, keep every test deterministic, and give the team a suite that is fast
on every pull request and trusted when it fails. A good result is a test plan or review that names the
layers, what each one covers, the gaps, and how CI runs it.

## When to use

- Planning tests for a new feature or app, or auditing an existing suite.
- Choosing between a unit test, a screen test, a screenshot test and an end-to-end test.
- Adding screenshot tests (Roborazzi, Paparazzi, swift-snapshot-testing, Flutter goldens).
- Writing Compose UI tests, XCUITests or Flutter `integration_test` flows.
- Flaky, slow or order-dependent tests; deciding on retries, quarantine and CI sharding.
- Setting a coverage policy, or reviewing tests in a merge request.

Not for: framework syntax for one language (use `mobile-kotlin`, `mobile-java`, `mobile-swift`,
`mobile-flutter`; each has a references/testing.md), pipeline YAML, signing and caching details
(use `mobile-ci-cd`).

## Workflow

1. Map the feature: entry points, state holders, data sources, platform boundaries (network, BLE,
   storage, permissions, clock) and the user journeys that cost money or support tickets when they break.
2. Read the existing tests and CI config. Note frameworks in use, test run time, known flaky tests and
   coverage reports. Extend what exists before adding a new framework.
3. Assign every behavior to the lowest layer that can catch its bug (see the table below). Write the
   list down before writing code.
4. Put seams at boundaries: interfaces or protocols for data sources, injected dispatchers and clocks,
   launch flags for UI tests. Write fakes once per boundary.
5. Write the tests. For language-level syntax, load the matching language skill's reference by name:
   `mobile-kotlin`, references/testing.md (coroutines, Turbine, MockK, Room, Compose);
   `mobile-java`, references/testing.md (LiveData, Mockito, Espresso, IdlingResource);
   `mobile-swift`, references/testing.md (Swift Testing, confirmations, XCTest UI and performance);
   `mobile-flutter`, references/testing.md (mocktail, fake_async, Riverpod, Bloc, widget tests).
   For ViewModel and reducer tests, `mobile-mvvm` rule 11 and `mobile-mvi` rule 9.
6. Screen and journey tests: load [ui-tests.md](references/ui-tests.md).
7. Visual regressions: load [screenshot-tests.md](references/screenshot-tests.md).
8. CI layout, sharding, retries and the flaky-test process: load [ci-and-flakes.md](references/ci-and-flakes.md).
9. Run the suite twice, once in random order where the runner supports it. Report failures honestly; never
   mark the work done with a red or skipped-without-ticket test.
10. Deliver the result in the output format below.

## Test layers

| Layer | Catches | Android | iOS | Flutter | Runs |
|---|---|---|---|---|---|
| Unit | Logic: validation, mapping, parsing, CRC, reducers, ViewModels | JUnit, coroutines-test, Turbine | Swift Testing | `package:test`, `flutter_test` | Every PR, seconds |
| Integration | Real collaborators together: repository + DB, serializer + fixtures, DI graph | Room in-memory, Robolectric | Swift Testing with in-memory SwiftData | `flutter_test` with in-memory fakes | Every PR |
| Screen (UI behavior) | One screen renders state and sends events | Compose UI test on Robolectric or device | XCUITest on a screen with fixed data | `testWidgets` | Every PR (JVM, widget), merge (device) |
| Screenshot | Layout, theme, dark mode, large fonts, RTL | Roborazzi or Paparazzi | swift-snapshot-testing | `matchesGoldenFile` | Every PR, pinned image |
| End-to-end | A critical journey across screens and process boundaries | Compose UI or Espresso on emulator | XCUITest | `integration_test` | Merge or nightly |

Most tests sit in the first two rows. End-to-end tests are few, one per critical journey (sign-in,
pairing, purchase, firmware update), never one per screen detail.

## Rules

### 1. Test each behavior at the lowest layer that can catch its bug

A UI test that checks a validation rule is slow, flaky and points nowhere when it fails.

Kotlin:
```kotlin
// BAD: an instrumented UI test to prove one validation rule
composeRule.onNodeWithTag("pin").performTextInput("12")
composeRule.onNodeWithText("PIN too short").assertIsDisplayed()

// GOOD: the rule is a plain function, tested on the JVM in milliseconds
@Test fun `rejects pin shorter than six digits`() {
    assertEquals(PinError.TooShort, validatePin("12"))
}
```

Swift:
```swift
// BAD: XCUITest launches the app to check a parser
func testBatteryFrame() { app.launch(); /* navigate to a screen that shows the parsed value */ }

// GOOD
@Test func decodesBatteryLevel() throws {
    #expect(try FrameDecoder().decode(Fixtures.batteryFrame).battery == 87)
}
```

Dart:
```dart
// BAD: an integration_test on a device for a mapper
// GOOD
test('maps 0xFF to unknown battery', () {
  expect(Battery.fromRaw(0xFF), Battery.unknown);
});
```

- The screen test then checks once that an error state is rendered, not every rule behind it.

### 2. Fakes at boundaries you own; mocks only for interactions

Kotlin:
```kotlin
// BAD: a mock of your own repository, re-stubbed in every test, breaks on every refactor
val repo = mockk<DeviceRepository>()
every { repo.devices } returns flowOf(listOf(gateway))

// GOOD: one fake per boundary, reused by every test of the feature
class FakeDeviceRepository : DeviceRepository {
    private val state = MutableStateFlow<List<Device>>(emptyList())
    var refreshError: Throwable? = null
    override val devices: Flow<List<Device>> = state
    override suspend fun refresh() { refreshError?.let { throw it } }
    fun emit(list: List<Device>) { state.value = list }
}
```

Swift:
```swift
// GOOD: protocol at the boundary, fake in the test target
struct FakeTransport: BLETransport {
    var responses: [Data] = []
    func write(_ frame: Data) async throws -> Data { responses.first ?? Data() }
}
```

Dart:
```dart
// GOOD: implements the interface; no per-test stubbing
class FakeDeviceRepository implements DeviceRepository {
  List<Device> devices = [];
  @override
  Future<List<Device>> fetch() async => devices;
}
```

- Mock when the interaction is the behavior (an analytics event sent exactly once, a write never issued).
- Wrap third-party clients (HTTP, BLE stacks, billing) behind your interface; fake the interface.
- Never mock value types, data classes or the class under test.

### 3. Time, dispatchers and randomness are injected

Kotlin:
```kotlin
// BAD: hardcoded dispatcher and real delay; the test waits 30 seconds or races
class Poller(private val api: Api) {
    suspend fun run() = withContext(Dispatchers.IO) { while (true) { api.poll(); delay(30_000) } }
}

// GOOD: same class with `io: CoroutineDispatcher` injected and used in withContext(io)
@Test fun `polls every 30 seconds`() = runTest {
    val api = FakeApi()
    backgroundScope.launch { Poller(api, StandardTestDispatcher(testScheduler)).run() }
    advanceTimeBy(60_001)
    assertEquals(3, api.pollCount)
}
```

Swift:
```swift
try await Task.sleep(for: .seconds(30)) // BAD: real time, no seam
// GOOD: the clock is a dependency; tests pass a manual test clock
struct Poller {
    let clock: any Clock<Duration>
    func waitForNextPoll() async throws { try await clock.sleep(for: .seconds(30)) }
}
```

Dart:
```dart
final expiresAt = DateTime.now().add(ttl); // BAD
// GOOD: inject the clock; drive timers with fakeAsync or tester.pump(duration)
class TokenCache {
  TokenCache({DateTime Function()? now}) : _now = now ?? DateTime.now;
  final DateTime Function() _now;
}
```

- Same for UUIDs, random backoff jitter, locale and time zone: pass them in, fix them in tests.

### 4. Screen tests drive a stateless screen with plain state

Kotlin (Compose, v2 test APIs):
```kotlin
// BAD: real ViewModel, Hilt graph and network inside a screen test
composeRule.setContent { DevicesRoute(viewModel = hiltViewModel()) }

// GOOD
import androidx.compose.ui.test.junit4.v2.createComposeRule
@get:Rule val composeRule = createComposeRule()

@Test fun clickingDeviceReportsId() {
    var clicked: DeviceId? = null
    composeRule.setContent {
        AppTheme { DevicesScreen(state = DevicesUiState(devices = listOf(gateway)), onDeviceClick = { clicked = it }) }
    }
    composeRule.onNodeWithText("Gateway A").performClick()
    assertEquals(gateway.id, clicked)
}
```

Swift (SwiftUI):
```swift
// BAD: one XCUITest per screen state. GOOD: model test for logic, snapshot per visual state
@MainActor @Test func emptyListShowsPairPrompt() async {
    let model = DeviceListModel(repository: FakeDeviceRepository(stubbedDevices: []))
    await model.load()
    #expect(model.state == .empty)
}
```

Dart:
```dart
// GOOD: widget test with the repository overridden by a fake
await tester.pumpWidget(ProviderScope(
  overrides: [deviceRepositoryProvider.overrideWithValue(FakeDeviceRepository())],
  child: const MaterialApp(home: DevicesScreen()),
));
```

- The v1 rule factories (`androidx.compose.ui.test.junit4.createComposeRule`) are deprecated. v2 runs
  composition on `StandardTestDispatcher`; queued work runs after `waitForIdle()` or `runOnIdle`.

### 5. Find elements the way a user or assistive technology does

Kotlin:
```kotlin
composeRule.onAllNodesWithTag("row")[3].performClick()                    // BAD: tree position
composeRule.onNodeWithContentDescription("Delete Gateway A").performClick() // GOOD: what a user hears
```

Swift:
```swift
app.buttons["Pair"].tap()        // BAD: visible text breaks in every locale
app.buttons["pair-device"].tap() // GOOD: accessibilityIdentifier
```

Dart:
```dart
await tester.tap(find.byType(IconButton).at(2));       // BAD
await tester.tap(find.byTooltip('Delete Gateway A')); // GOOD
```

### 6. Wait on conditions, never on wall-clock time

Kotlin:
```kotlin
Thread.sleep(2_000) // BAD
composeRule.waitUntilAtLeastOneExists(hasText("Connected"), timeoutMillis = 5_000) // GOOD
```

Swift:
```swift
sleep(3) // BAD
XCTAssertTrue(app.staticTexts["paired-status"].waitForExistence(timeout: 5)) // GOOD
```

Dart:
```dart
await Future<void>.delayed(const Duration(seconds: 2)); // BAD
// GOOD: pump fake time; pumpAndSettle throws on endless animations such as spinners
await tester.pump(const Duration(milliseconds: 300));
```

- Background work the test framework cannot see gets an idling resource, not a sleep (details in
  [ui-tests.md](references/ui-tests.md)).

### 7. Screenshot tests pin everything that changes pixels

Device size, density, locale, font scale, theme, fonts, OS or simulator version and renderer.

Kotlin (Paparazzi):
```kotlin
@get:Rule val paparazzi = Paparazzi() // BAD: locale comes from the machine running the test
// GOOD
@get:Rule val paparazzi = Paparazzi(
    deviceConfig = DeviceConfig.PIXEL_5.copy(locale = "en", nightMode = NightMode.NIGHT),
)
```

Swift:
```swift
assertSnapshot(of: DeviceCard(device: .sample), as: .image) // BAD: size depends on the host
// GOOD: fixed device layout, and the same simulator model and OS on every machine
assertSnapshot(of: DeviceCard(device: .sample), as: .image(layout: .device(config: .iPhone13)))
```

Dart:
```dart
// GOOD: fixed surface; real fonts loaded in flutter_test_config.dart, else text renders as boxes
tester.view.physicalSize = const Size(1080, 2400);
tester.view.devicePixelRatio = 3.0;
addTearDown(tester.view.reset);
```

### 8. Reference images are recorded on the CI image and reviewed as diffs

```bash
# BAD: references recorded on a developer laptop, CI records missing ones and passes
# GOOD: CI only verifies; a labelled job on the same image records and uploads for review
./gradlew verifyRoborazziDebug          # or verifyPaparazziDebug
# TEST_RUNNER_ prefix passes SNAPSHOT_TESTING_RECORD=never to the test runner process
TEST_RUNNER_SNAPSHOT_TESTING_RECORD=never xcodebuild test ...
flutter test --tags golden               # --update-goldens only in the recording job
```

- A changed reference image is reviewed in the merge request like code. Unexplained diffs block.

### 9. End-to-end tests run against a controlled world

Swift:
```swift
app.launch() // BAD: real backend, real BLE device, shared test account

// GOOD: launch flags switch the app to fakes and fixed data
app.launchArguments = ["-ui-testing", "-fake-ble"]
app.launch()
```

- Android: replace modules with test doubles (`@TestInstallIn`) or use a test flavor. Flutter: a test
  entry point or `--dart-define-from-file` pointing at a test backend.
- Never production endpoints or real user data. BLE hardware tests live in a separate, manual or
  rig-based suite with its own reporting.

### 10. Every test is isolated and order-independent

Kotlin:
```kotlin
companion object { val repo = FakeDeviceRepository() } // BAD: shared, mutated by earlier tests
private val repo = FakeDeviceRepository()               // GOOD: new per test instance
```

- Swift Testing: a `struct` suite gets a fresh instance per test, and tests run in parallel by default.
- Dart: build state in `setUp`; run with `--test-randomize-ordering-seed random` to expose order
  dependence.
- Android instrumented: Android Test Orchestrator with `clearPackageData` when app state leaks between
  tests (slower; use where needed).

### 11. A flaky test is a bug: quarantine with a ticket, retry only with tracking

Swift:
```swift
@Test func scansInBackground() async { } // BAD: fails one run in ten, everyone re-runs CI
// GOOD: out of the blocking gate, owned, with a deadline
@Test(.disabled("Flaky on CI simulator, MOB-412, fix by 2026-11-01"))
func scansInBackground() async { }
```

Dart:
```dart
testWidgets('reconnects after drop', (tester) async { /* ... */ }, tags: 'quarantine');
// Blocking job: flutter test --exclude-tags quarantine
```

- Kotlin: a team annotation or category excluded from the blocking job, with the ticket in the reason.
- Retries (Gradle test-retry plugin, `xcodebuild -retry-tests-on-failure`) are allowed only when the
  report records which tests passed on retry and someone reviews that list. Never retry silently.

### 12. Coverage gates protect critical logic, not a vanity number

```kotlin
// BAD: one global 90 percent gate over generated code, DI modules and composables
// GOOD: a gate on the modules that hold logic, plus a review of uncovered branches there
kover { reports { verify { rule { minBound(80) } } } } // in the domain and data modules
```

- Exclude generated code (DI, serializers, build config) from reports. Gate domain, data and parsing
  modules; read the uncovered-branch report for ViewModels, reducers and protocol code.
- iOS: `xcodebuild test -enableCodeCoverage YES`. Flutter: `flutter test --coverage`.
- A test that executes code without asserting on it adds coverage and no safety. Look for it in reviews.

### 13. The pull request gate stays fast; slow layers are sharded

- PR: unit, integration, JVM screen, widget and screenshot-verify tests, under 10 minutes. Merge or
  nightly: device journeys, sharded. Android `numShards`/`shardIndex` or managed device shards; iOS
  `build-for-testing` then `test-without-building` per shard; Flutter `--total-shards`/`--shard-index`.
  Commands in [ci-and-flakes.md](references/ci-and-flakes.md).

## Anti-patterns

- An inverted pyramid: many end-to-end tests, few unit tests, a suite nobody runs locally.
- Testing private functions or implementation details instead of observable state and output.
- Mocking every collaborator, then asserting the mocks were called in the order the code calls them.
- `Thread.sleep`, `sleep`, `Task.sleep` or `Future.delayed` in tests to "wait for" anything.
- `UnconfinedTestDispatcher` everywhere to hide ordering problems.
- Snapshot references recorded on mixed machines, or CI that records missing snapshots and passes.
- Hundreds of screenshot tests of whole screens with live data; nobody reviews the diffs.
- UI tests that depend on real servers, BLE hardware, network quality or a shared account.
- Retrying the whole job until green; `@Ignore` or `.disabled` with no ticket.
- A coverage target raised by tests that assert nothing.
- Test fixtures containing real device serials, MAC addresses or user data. Use synthetic identifiers.

## Checklist

- [ ] Critical journeys listed; each has exactly one end-to-end test
- [ ] Every behavior assigned to the lowest layer that can catch it
- [ ] Fakes exist for each boundary (network, storage, BLE, clock); mocks only for interactions
- [ ] Dispatchers, clocks, randomness, locale and time zone injected; no real delays in tests
- [ ] Screen tests use stateless screens with plain state; Compose tests use the v2 rule factories
- [ ] Selectors use text, semantics or accessibility identifiers, not tree position
- [ ] No sleeps; waits are condition-based; background work has idling resources
- [ ] Screenshot tests pin device, locale, font scale, theme, fonts and the CI image
- [ ] CI verifies snapshots and never records; reference changes reviewed in the MR
- [ ] Tests pass in random order and in isolation
- [ ] Flaky tests quarantined with a ticket and owner; retried tests reported and reviewed
- [ ] Coverage gated on logic modules, generated code excluded
- [ ] PR gate under 10 minutes; slow layers sharded; reports uploaded on failure
- [ ] Fixtures contain no real personal data or device identifiers
- [ ] Suite run locally and in CI; failures reported, not hidden

## Output format

For a plan:

~~~markdown
## Test plan: <feature or app>

Platforms: <Android | iOS | Flutter>. Existing frameworks: <list>. Current PR suite time: <n> min.

### Critical journeys
1. <journey> -- end-to-end test: <name>, layer runs on <merge | nightly>

### Coverage by layer
| Behavior | Layer | Test (file or name) | Status |
|---|---|---|---|
| PIN validation | Unit | PinValidatorTest | New |
| Device list renders empty state | Screenshot | DeviceListSnapshots | Exists |

### Seams and fakes
- <boundary> -- <fake or launch flag to add>

### Gaps and risks
- <untested behavior> -- <risk> -- <proposed test>

### CI plan
- PR: <jobs, target time>
- Merge / nightly: <jobs, shards, devices>
- Flake policy: <quarantine tag, retry setting, report location>
~~~

For a review of existing tests: list findings as `[Blocker|Major|Minor] path:line -- issue`, then
`Why` and a minimal `Fix`, in the same style as `mobile-code-review`, followed by the gaps table above.
Missing tests for new logic or a sleep-based wait is Major; a test that can never fail is Major.

## Related skills

- `mobile-kotlin`, `mobile-java`, `mobile-swift`, `mobile-flutter` -- language-level test syntax in each
  skill's references/testing.md
- `mobile-mvvm`, `mobile-mvi` -- ViewModel, store and reducer tests
- `mobile-ci-cd` -- pipeline jobs, caching and report upload that run this plan
- `mobile-code-review` -- review of the tests inside a merge request
- `mobile-accessibility` -- semantics and labels that also make UI tests stable
- `mobile-ble` -- transport fakes and hardware-in-the-loop suites
- `mobile-security` -- tests for storage, network and crypto controls
