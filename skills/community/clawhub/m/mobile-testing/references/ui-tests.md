# UI and end-to-end tests

Load this when writing screen tests or journey tests: Compose UI tests, XCUITest and Flutter
`integration_test`. For Espresso and `IdlingResource` in Java or View-based code, see `mobile-java`,
references/testing.md. For widget-test basics (`pump`, finders), see `mobile-flutter`, references/testing.md.

## Choosing the runtime

| Need | Android | iOS | Flutter |
|---|---|---|---|
| Screen behavior, fast, every PR | Compose UI test on Robolectric (`src/test`) | Model test plus snapshot; XCUITest only if the screen logic is in the view | `testWidgets` |
| Real rendering, IME, permissions, process death | Compose UI test on emulator (`src/androidTest`) | XCUITest on simulator | `integration_test` on emulator or simulator |
| Journey across screens | Instrumented test on a Gradle managed device | XCUITest with launch flags | `integration_test` |

## Compose UI tests

Dependencies (versions in `libs.versions.toml`):

```kotlin
androidTestImplementation(libs.androidx.compose.ui.test.junit4)
debugImplementation(libs.androidx.compose.ui.test.manifest) // needed for createComposeRule()
```

Use the v2 rule factories. The v1 factories are deprecated; v2 runs composition on a
`StandardTestDispatcher`, so launched coroutines are queued until the test clock advances.

| Deprecated (v1) | Use (v2) |
|---|---|
| `androidx.compose.ui.test.junit4.createComposeRule` | `androidx.compose.ui.test.junit4.v2.createComposeRule` |
| `androidx.compose.ui.test.junit4.createAndroidComposeRule` | `androidx.compose.ui.test.junit4.v2.createAndroidComposeRule` |
| `androidx.compose.ui.test.runComposeUiTest` | `androidx.compose.ui.test.v2.runComposeUiTest` |

```kotlin
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule

class PairingScreenTest {
    // Empty host activity: setContent is allowed and string resources are reachable
    @get:Rule val composeRule = createAndroidComposeRule<ComponentActivity>()

    @Test fun showsErrorWhenPairingFails() {
        composeRule.setContent {
            AppTheme { PairingScreen(state = PairingUiState(error = PairingError.Timeout), onRetry = {}) }
        }
        val retry = composeRule.activity.getString(R.string.retry)
        composeRule.onNodeWithText(retry).assertIsDisplayed().assertHasClickAction()
    }
}
```

- Migrating to v2: a test that asserted state right after triggering work may now see the old state. Call
  `composeRule.waitForIdle()` or wrap the assertion in `runOnIdle { }`.
- Tests that combine a compose rule with `runTest` should move to `runComposeUiTest`, which runs the block in
  its own `runTest` scope with a shared clock. Check whether your version still needs an opt-in annotation.
- Hilt: `@HiltAndroidTest`, `HiltAndroidRule` ordered before the compose rule, production modules replaced
  with `@TestInstallIn`. See `mobile-kotlin`, references/testing.md.

### Synchronization

```kotlin
// Animations and time-based UI: drive the clock yourself
composeRule.mainClock.autoAdvance = false
composeRule.onNodeWithText("Scan").performClick()
composeRule.mainClock.advanceTimeBy(300)
composeRule.onNodeWithTag("scan-progress").assertIsDisplayed()

// Work outside Compose (data loading, a fake transport callback)
composeRule.waitUntilAtLeastOneExists(hasText("Gateway A"), timeoutMillis = 5_000)
composeRule.waitUntil(timeoutMillis = 5_000) { fakeTransport.connected }
```

- Also `waitUntilDoesNotExist`, `waitUntilExactlyOneExists`, `waitUntilNodeCount`.
- Background work the rule cannot see: implement an `IdlingResource` and register it with
  `composeRule.registerIdlingResource(...)`; unregister in teardown.
- The docs warn that external latches (`CountDownLatch`) instead of `waitUntil` can misbehave because the
  test clock does not advance.
- Merged semantics: a `Row` with `Modifier.semantics(mergeDescendants = true)` hides child nodes; pass
  `useUnmergedTree = true` to the finder when asserting on a child.

### Permissions on a device

```kotlin
@get:Rule val permissions: GrantPermissionRule =
    GrantPermissionRule.grant(Manifest.permission.BLUETOOTH_SCAN, Manifest.permission.BLUETOOTH_CONNECT)
```

- Grant only what the test needs. Test the denied path separately, at screen level, with a fake permission
  checker rather than the system dialog.
- Clear app state between tests with Android Test Orchestrator and `clearPackageData` when tests share
  storage (see [ci-and-flakes.md](ci-and-flakes.md)).

## XCUITest

XCUITest is black-box: the test process drives the app through accessibility. Swift Testing does not run UI
tests; UI test targets use `XCTestCase`.

```swift
final class PairingUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["-ui-testing", "-fake-ble"]
        app.launchEnvironment = ["FIXTURE": "one-gateway"]
        app.launch()
    }

    func testPairingHappyPath() {
        let screen = PairingScreen(app: app)
        screen.pairButton.tap()
        XCTAssertTrue(screen.status.waitForExistence(timeout: 5))
        XCTAssertEqual(screen.status.label, "Paired")
    }
}

// Screen object: one place to update when identifiers change
struct PairingScreen {
    let app: XCUIApplication
    var pairButton: XCUIElement { app.buttons["pair-device"] }
    var status: XCUIElement { app.staticTexts["paired-status"] }
}
```

App side:

```swift
#if DEBUG
let usesFakeBLE = ProcessInfo.processInfo.arguments.contains("-fake-ble")
#else
let usesFakeBLE = false
#endif
```

- Compile test hooks into debug builds only. A launch argument that swaps transports or skips login in a
  release build is a security hole.
- Query by `accessibilityIdentifier`, which is not localized and not read by VoiceOver.
- `waitForExistence(timeout:)` and, in current SDKs, `waitForNonExistence(timeout:)` for disappearing
  spinners. No `sleep`.
- System permission alerts: prefer avoiding them with fakes. When the alert is the subject, handle it
  with `addUIInterruptionMonitor(withDescription:handler:)`, or reset state first with
  `app.resetAuthorizationStatus(for:)`. On a simulator, `xcrun simctl privacy <device> grant location
  <bundle id>` pre-grants supported services (Bluetooth is not one of them; the simulator has no BLE radio,
  so use a fake transport).
- iOS 17 and later: `try app.performAccessibilityAudit()` in one smoke test per main screen catches missing
  labels and small hit targets.
- Run locales and configurations from a test plan (one configuration per language or region) instead of
  duplicating tests.

## Flutter integration_test

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
```

```dart
// integration_test/pairing_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main_test.dart' as app; // test entry point wired to fakes

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('user pairs a gateway', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    await tester.tap(find.text('Add device'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Gateway A'));

    await tester.pump(const Duration(seconds: 1));
    expect(find.text('Paired'), findsOneWidget);
  });
}
```

- Run all: `flutter test integration_test`; one file on one device:
  `flutter test integration_test/pairing_test.dart -d <device-id>`.
- A separate entry point (`lib/main_test.dart`) or `--dart-define-from-file` selects fakes or a test
  backend. Never production.
- `pumpAndSettle` throws if an endless animation is running (indeterminate spinners). Use `pump(duration)`
  around such screens.
- `--concurrency` is ignored for integration tests; split files across CI jobs instead.
- Native dialogs (permissions, system pickers) are outside Flutter. Pre-grant on the device
  (`adb shell pm grant <package> <permission>`, `xcrun simctl privacy ...`) or fake the permission plugin
  behind your own interface.
- Device farms on Android: build `flutter build apk --debug`, then in `android/`
  `./gradlew app:assembleAndroidTest` and `./gradlew app:assembleDebug -Ptarget=integration_test/<name>_test.dart`,
  as described in the `integration_test` package README.

## What a journey test asserts

- The user-visible outcome (status text, navigation to the next screen, item in a list), not internal state.
- One journey per test. Arrange the starting state through launch flags or fixtures, not by tapping through
  onboarding in every test.
- Failure artifacts: screenshot on failure, logs, and the result bundle or test report uploaded by CI.
