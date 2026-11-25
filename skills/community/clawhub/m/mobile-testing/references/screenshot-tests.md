# Screenshot tests

Load this when adding or fixing screenshot tests (also called snapshot or golden tests). Pick one tool
per platform and module. Check each library's README for the current version before adding it; do not
copy version numbers from this file.

## What to snapshot

- Design-system components in every variant: enabled, disabled, error, loading.
- Key screen states with fixed fake data: empty, loaded, error, long text, many items.
- The same states in dark theme, the largest supported font scale and one RTL locale.
- Not: every screen with live data, animations mid-flight, or content with timestamps you did not fix.

Keep the count small enough that every diff gets reviewed. A diff nobody looks at is a test that cannot fail.

## Pin the environment

| Input | Android | iOS | Flutter |
|---|---|---|---|
| Device size and density | `@Config(qualifiers = ...)` (Roborazzi), `DeviceConfig` (Paparazzi) | `.image(on:)` or `layout: .device(config:)` | `tester.view.physicalSize`, `devicePixelRatio` |
| Locale | Robolectric qualifiers, `DeviceConfig(locale = ...)` | Scheme or test plan language, or inject the locale | `MaterialApp(locale: ...)` |
| Theme and font scale | `+night` qualifier, `DeviceConfig.copy(nightMode, fontScale)` | `traits:` with a `UITraitCollection` | `MediaQuery` or theme in the test tree |
| Fonts | Bundled app fonts render on the JVM | Bundled fonts | Load with `FontLoader`; the default test font is Ahem (boxes) |
| Host | Record and verify on the same CI image | Same simulator model and OS version | Same OS (usually the Linux CI image) |

Paparazzi's `DeviceConfig.locale` defaults to a value detected from the environment. Set it explicitly.

## Android: Roborazzi (Robolectric)

Runs on the JVM as a local test, so it also captures screens after interactions.

```kotlin
// module build.gradle.kts
plugins { id("io.github.takahirom.roborazzi") }

android {
    testOptions { unitTests { isIncludeAndroidResources = true } }
}

roborazzi {
    outputDir.set(file("src/screenshots")) // default is build/outputs/roborazzi, which is not committed
}

dependencies {
    testImplementation(libs.roborazzi)
    testImplementation(libs.roborazzi.compose)
    testImplementation(libs.roborazzi.junit.rule)
    testImplementation(libs.robolectric)
}
```

```kotlin
@RunWith(AndroidJUnit4::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(qualifiers = RobolectricDeviceQualifiers.Pixel5)
class DeviceCardScreenshotTest {

    @Test fun deviceCard() {
        captureRoboImage { AppTheme { DeviceCard(sampleDevice) } }
    }

    @Config(qualifiers = "+night")
    @Test fun deviceCardDark() {
        captureRoboImage { AppTheme { DeviceCard(sampleDevice) } }
    }
}
```

- After interactions in a Compose UI test: `composeRule.onNodeWithTag("device-card").captureRoboImage()`.
- Tasks: `recordRoborazziDebug`, `compareRoborazziDebug`, `verifyRoborazziDebug`,
  `verifyAndRecordRoborazziDebug`. Equivalent properties on `testDebugUnitTest`:
  `-Proborazzi.test.record=true`, `-Proborazzi.test.compare=true`, `-Proborazzi.test.verify=true`.
- A small tolerance is set through `RoborazziOptions(compareOptions = RoborazziOptions.CompareOptions(changeThreshold = 0.01F))`.
  Keep it near zero; a large threshold hides real regressions.
- The README states there is no guarantee of identical rendering across environments and recommends
  recording and verifying on CI. It also needs Robolectric native graphics on API 28 or higher, and
  documents the Robolectric `robolectric.pixelCopyRenderMode` option (`hardware`) for more accurate
  captures; check the README for how to set it for your version.

## Android: Paparazzi

Renders composables and views without a device, emulator or Robolectric.

```kotlin
plugins { id("app.cash.paparazzi") }
```

```kotlin
import com.android.resources.NightMode

class DeviceCardPaparazziTest {
    @get:Rule val paparazzi = Paparazzi(
        deviceConfig = DeviceConfig.PIXEL_5.copy(locale = "en", nightMode = NightMode.NIGHT, fontScale = 1.5f),
        theme = "android:Theme.Material.Light.NoActionBar",
    )

    @Test fun deviceCard() {
        paparazzi.snapshot { AppTheme { DeviceCard(sampleDevice) } }
    }
}
```

- Tasks: `recordPaparazziDebug` writes references to `src/test/snapshots`; `verifyPaparazziDebug` compares
  and writes diffs to `build/paparazzi/failures`; `testDebug` produces an HTML report under
  `build/reports/paparazzi/`.
- The project recommends Git LFS for snapshots: `git lfs track "**/snapshots/**/*.png"`.
- Recent releases are 2.0 alphas; check the changelog before choosing a version.

## Android: Compose Preview Screenshot Testing

Google's tool turns `@Preview` functions annotated with `@PreviewTest` in a `screenshotTest` source set into
screenshot tests (`updateDebugScreenshotTest`, `validateDebugScreenshotTest`). It is alpha and experimental,
needs `android.experimental.enableScreenshotTest=true`, and newer AGP versions recommend configuring it
through AGP test suites. Use it only if the team accepts alpha tooling; re-check the official page first.

## iOS: swift-snapshot-testing

Add the package `https://github.com/pointfreeco/swift-snapshot-testing` to the test target only (product
`SnapshotTesting`).

```swift
import SnapshotTesting
import SwiftUI
import Testing
@testable import DeviceFeature

@MainActor
@Suite(.snapshots(record: .missing))
struct DeviceCardSnapshotTests {
    @Test func light() {
        assertSnapshot(of: DeviceCard(device: .sample), as: .image(layout: .device(config: .iPhone13)))
    }

    @Test func dark() {
        assertSnapshot(
            of: DeviceCard(device: .sample),
            as: .image(layout: .device(config: .iPhone13), traits: UITraitCollection(userInterfaceStyle: .dark))
        )
    }

    @Test func accessibilityText() {
        assertSnapshot(
            of: DeviceCard(device: .sample),
            as: .image(layout: .sizeThatFits, traits: UITraitCollection(preferredContentSizeCategory: .accessibilityExtraLarge))
        )
    }
}
```

- UIKit: `assertSnapshot(of: viewController, as: .image(on: .iPhoneSe))`, also `.iPhoneSe(.landscape)`.
- SwiftUI layouts: `.device(config:)`, `.fixed(width:height:)`, `.sizeThatFits` (default).
- `precision` and `perceptualPrecision` default to 1. A `perceptualPrecision` slightly below 1 absorbs
  anti-aliasing noise; never lower `precision` to make layout changes pass.
- Record modes: `.all`, `.failed`, `.missing` (default: records missing references and fails), `.never`
  (missing reference is a failure; the documented choice for CI). Set per assertion (`record:`), per scope
  (`withSnapshotTesting(record:)`), per suite (`.snapshots(record:)`), or with the environment variable
  `SNAPSHOT_TESTING_RECORD`. From `xcodebuild`, prefix it: `TEST_RUNNER_SNAPSHOT_TESTING_RECORD=never`.
- References live in `__Snapshots__` next to the test file. Failure images go to the directory in
  `SNAPSHOT_ARTIFACTS`, or the temporary directory; upload that directory from CI.
- The README warns that snapshots must be compared on the exact simulator that recorded them. Pin the
  simulator model and OS in the CI destination and in the team's recording instructions.

## Flutter: golden files

```dart
testWidgets('device card, dark, large text', (tester) async {
  tester.view.physicalSize = const Size(1080, 2400);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.reset);

  await tester.pumpWidget(MaterialApp(
    theme: AppTheme.dark(),
    home: MediaQuery(
      data: const MediaQueryData(textScaler: TextScaler.linear(1.5)),
      child: Scaffold(body: DeviceCard(device: sampleDevice)),
    ),
  ));

  await expectLater(find.byType(DeviceCard), matchesGoldenFile('goldens/device_card_dark_large.png'));
}, tags: 'golden');
```

Load real fonts once for the whole directory tree. The test framework looks upward from each test file for
`flutter_test_config.dart` and runs `testExecutable` with the test's `main`:

```dart
// test/flutter_test_config.dart
import 'dart:async';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

Future<void> testExecutable(FutureOr<void> Function() testMain) async {
  TestWidgetsFlutterBinding.ensureInitialized();
  final roboto = FontLoader('Roboto')..addFont(rootBundle.load('assets/fonts/Roboto-Regular.ttf'));
  await roboto.load();
  await testMain();
}
```

- The family name passed to `FontLoader` must match the `fontFamily` the theme uses.
- Update references with `flutter test --update-goldens`, only in the recording job or locally on the
  pinned platform. The docs note custom fonts can render differently across platforms and Flutter versions,
  so re-record after a Flutter upgrade in a dedicated merge request.
- Declare the tag in `dart_test.yaml` (`tags: { golden: {} }`) and run goldens only on the pinned
  platform: `flutter test --tags golden` there, `--exclude-tags golden` elsewhere.
- `goldenFileComparator` can be replaced in `flutter_test_config.dart` (for example to add a tolerance).
  Keep any tolerance near zero.

## Reviewing diffs

1. CI runs verify only and uploads the diff images as artifacts on failure.
2. An intended UI change re-records in the same merge request, on the pinned image, through a labelled or
   manual job, and commits the new references.
3. The reviewer opens every changed reference. Unexplained changes block the merge.
4. Re-record everything only in a dedicated merge request (tool upgrade, OS image change, font change).
