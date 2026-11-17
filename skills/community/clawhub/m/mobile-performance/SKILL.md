---
name: mobile-performance
description: "Measures and fixes Android, iOS and Flutter app performance: startup (Baseline Profiles, App Startup, iOS launch time), jank (Compose recomposition, SwiftUI body cost, Flutter UI vs raster thread), memory leaks, app size, battery and network use. Uses Macrobenchmark, Perfetto, LeakCanary, Instruments, MetricKit, Flutter DevTools and Android vitals. Use when an app is slow to start, janky, leaking, too big or draining battery, or when asked to profile or benchmark."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile performance

Find and fix the performance problems users actually feel: slow launch, dropped frames, hangs, memory
growth, large downloads and battery drain. The agent measures first on a release-like build on a real
low or mid-range device, changes one thing, measures again under the same conditions, and reports the
numbers, not impressions.

## When to use

- "The app is slow to start", "scrolling stutters", "the UI freezes", "memory keeps growing".
- Android vitals, the Xcode Organizer or MetricKit show slow starts, ANRs, hangs, hitches or high memory.
- The APK, AAB or IPA grew, or users complain about battery or mobile data use.
- Setting up Macrobenchmark, Baseline Profiles, XCTest performance tests or Flutter profiling.
- Reviewing a change that touches the startup path, a scrolling list, images, background work or sync.

Not for: general code review (use `mobile-code-review`), Compose, SwiftUI or widget API usage without a
measured problem (use `mobile-kotlin`, `mobile-swift`, `mobile-flutter`), BLE throughput and connection
tuning (use `mobile-ble`), or CI pipeline setup (use `mobile-ci-cd`).

## Workflow

1. Name the symptom and the one metric that captures it (see the table below). "Feels slow" is not a
   metric; "cold start TTID median 1 850 ms on a Galaxy A15" is.
2. Fix the test conditions before measuring, and keep them for the "after" run.
   - Build: release-like. Android `benchmark` build type (non-debuggable, `profileable`, R8 on). iOS
     Release configuration through Profile. Flutter `--profile`.
   - Device: a real low or mid-range phone your users own. Never an emulator or simulator for numbers.
   - State: charged above 50 %, not hot, other apps closed, same OS version, same network.
   - Details in [references/measuring.md](references/measuring.md).
3. Measure the baseline with enough runs to trust it (startup at least 10 iterations, frames over a
   scripted scroll of at least 5 runs). Record median and P90, not the best run.
4. Find the cause with a trace (Perfetto, Instruments, DevTools), not by reading code alone. Load the
   platform reference: [Android](references/android.md), [iOS](references/ios.md),
   [Flutter](references/flutter.md). Flutter apps also need the host tools for native startup.
5. Change one thing. Several changes at once make it impossible to tell which one helped or hurt.
6. Re-measure with the same build type, device, iterations and statistic. Keep the change only if the
   difference is larger than the run-to-run noise.
7. Lock the gain in: a benchmark or performance test in CI, and field monitoring (Android vitals,
   Organizer, MetricKit) to confirm it in production.
8. Report with the output format below. If a number could not be measured, say so; never estimate it.

## Metrics and thresholds

| Area | Lab metric | Field source | Reference values |
|---|---|---|---|
| Startup (Android) | `timeToInitialDisplayMs`, `timeToFullDisplayMs` (`StartupTimingMetric`) | Android vitals | Vitals flags slow cold start at 5 s or more, warm 2 s or more, hot 1 s or more |
| Startup (iOS) | `XCTApplicationLaunchMetric`, App Launch template | Organizer Launch Time, `MXAppLaunchMetric` | Time to first frame after the launch screen; compare release over release |
| Startup (Flutter) | `--trace-startup` `timeToFirstFrameMicros` | Host platform vitals | Same as the host platform |
| Jank (Android) | `frameDurationCpuMs`, `frameOverrunMs` (`FrameTimingMetric`) | Vitals slow and frozen frames | Slow session: more than 50 % of frames over 16 ms. Frozen: more than 0.1 % over 700 ms |
| Jank (iOS) | `XCTOSSignpostMetric.scrollingAndDecelerationMetric`, Animation Hitches | Organizer hitch rate | Hitch rate at or below 10 ms/s is good. Main-thread work per frame under about 5 ms |
| Hangs | Main thread blocked | ANR rate, Organizer hangs, `MXHangDiagnostic` | ANR core vital 0.47 % overall, 8 % per phone model. iOS: delays over 100 ms are noticeable |
| Frames (Flutter) | UI and raster time per frame in DevTools | Host platform vitals | About 16 ms per frame at 60 Hz, 8 ms at 120 Hz |
| Memory | Heap and leaks in LeakCanary, Allocations, DevTools | Vitals memory metrics, `memoryMetrics` | No retained screens after navigating back |
| Battery | Wake locks, wakeups, background network | Vitals battery metrics, `cpuMetrics` | Vitals: background network over 50 MB per day, Wi-Fi scans over 4 per hour |
| Size | Download and install size per variant | Play Console, App Store Connect | Track every release; investigate any jump |

Thresholds change. Check the current Android vitals and Apple pages before quoting them to a team.

## Rules

### 1. Numbers come only from release-like builds on real devices

Debug builds run with JIT, assertions and debugger hooks. Their numbers are meaningless.

Kotlin (Gradle):
```kotlin
// BAD: benchmarking the debug variant on an emulator
// GOOD: release-like and debug-signed; add <profileable android:shell="true"/> to the manifest
create("benchmark") {
    initWith(getByName("release"))
    signingConfig = signingConfigs.getByName("debug")
    matchingFallbacks += listOf("release")
}
```

Swift:
```swift
// BAD: timing launch with print(Date()) in a Debug run from Xcode
// GOOD: XCTest performance test, Release configuration, physical device
func testLaunch() {
    measure(metrics: [XCTApplicationLaunchMetric()]) { XCUIApplication().launch() }
}
```

Dart:
```sh
flutter run            # BAD: debug, JIT, asserts
flutter run --profile  # GOOD: AOT, with tracing for DevTools
```

### 2. Android ships a Baseline Profile and a startup profile

Without one, a fresh install interprets and JIT-compiles the startup path. Google reports about 30 %
faster execution of covered code from the first launch.

```kotlin
// BAD: no profile, first launches after every update run cold code
// GOOD: generated by the Baseline Profile Gradle plugin (androidx.baselineprofile)
@get:Rule val rule = BaselineProfileRule()

@Test fun generate() = rule.collect(
    packageName = "com.example.app",
    includeInStartupProfile = true,
) {
    pressHome()
    startActivityAndWait()
}
```

- Profiles are installed only for release builds. Regenerate them when the startup path or main user
  journeys change. Full setup in [references/android.md](references/android.md).
- Flutter apps: the Dart code is already AOT-compiled; a profile helps only the Kotlin and Java side.

### 3. Nothing non-critical runs before the first frame

Kotlin:
```kotlin
// BAD: every SDK initialized on the main thread before any UI
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        Analytics.init(this); RemoteConfig.fetchBlocking(); Maps.init(this)
    }
}

// GOOD: only what the first screen needs; the rest is lazy or deferred
@HiltAndroidApp
class App : Application() {
    @Inject lateinit var analytics: Lazy<Analytics> // dagger.Lazy, created on first use
}
```

Swift:
```swift
// BAD: synchronous network and database work in didFinishLaunchingWithOptions or App.init
init() { try? database.migrateAndSyncNow() }
// GOOD: show cached content, refresh after the first frame
.task { await model.refreshInBackground() }
```

Dart:
```dart
// BAD: await analytics.init(); await remoteConfig.fetchAndActivate(); before runApp
// GOOD: await only what the first frame needs
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final settings = await Settings.load();
  runApp(App(settings: settings));
  unawaited(analytics.init());
}
```

- App Startup (`androidx.startup`) replaces many library content providers with one, and lets you turn
  off automatic initialization and call `AppInitializer` later. It does not make slow init fast by itself.
- iOS: fewer embedded dynamic frameworks, no `+load` or static initializers, and mergeable libraries
  (Xcode 15+) reduce pre-`main` time.

### 4. Report when the screen is really usable

TTID ends at the first frame, often a spinner. Mark the point where real content is shown.

Kotlin (Compose):
```kotlin
// BAD: no signal, TTFD is never reported
// GOOD
ReportDrawnWhen { state.items.isNotEmpty() }
```

Swift (iOS 16+):
```swift
// GOOD: extended launch counted in MetricKit until content is ready
let id = MXLaunchTaskID("load-feed")
try MXMetricManager.extendLaunchMeasurement(forTaskID: id) // main thread, before the first scene is active
await model.loadFeed()
try MXMetricManager.finishExtendedLaunchMeasurement(forTaskID: id)
```

Flutter: mark the moment with a `dart:developer` `Timeline` event for lab traces; field launch numbers
come from the host platform ([references/flutter.md](references/flutter.md)).

### 5. Frame work stays inside the frame budget

Parsing, sorting, image decoding and disk access belong off the main thread or UI isolate.

Kotlin:
```kotlin
// BAD: 2 MB JSON parsed on the main thread during scroll
val items = json.decodeFromString<List<Item>>(body)
// GOOD
val items = withContext(defaultDispatcher) { json.decodeFromString<List<Item>>(body) }
```

Swift:
```swift
// BAD: Task inherits the main actor, the parse still blocks the UI
Button("Load") { Task { items = parse(data) } }
// GOOD: @concurrent (Swift 6.2) always leaves the caller's actor
@concurrent nonisolated func parse(_ data: Data) async -> [Item] { /* ... */ }
Button("Load") { Task { items = await parse(data) } }
```

Dart:
```dart
// BAD
final items = parseItems(body);
// GOOD
final items = await Isolate.run(() => parseItems(body));
```

### 6. Update only what changed

Compose, SwiftUI and Flutter all redo work for every reader of changed state. Narrow the readers.

Kotlin (Compose):
```kotlin
// BAD: reads scroll offset in composition, recomposes every pixel
Box(Modifier.offset(y = (scroll.value / 2).dp))
// GOOD: read in the layout phase, no recomposition
Box(Modifier.offset { IntOffset(0, scroll.value / 2) })
```

Swift (SwiftUI):
```swift
// BAD: ObservableObject, every @Published change re-evaluates every observing body
final class Feed: ObservableObject { @Published var items = [Item](); @Published var clock = Date() }
// GOOD: @Observable tracks only the properties each body reads
@Observable final class Feed { var items = [Item](); var clock = Date() }
```

Dart (Flutter):
```dart
// BAD: whole screen rebuilds when the counter changes
final state = context.watch<CartModel>();
// GOOD: only this widget rebuilds, and only when count changes
final count = context.select((CartModel c) => c.count);
```

More patterns: `mobile-kotlin` references/compose.md, `mobile-swift` references/swiftui.md,
`mobile-flutter` references/performance.md.

### 7. Images are decoded at display size

A 4000x3000 photo is about 48 MB of pixels, whatever size it is drawn at.

Kotlin:
```kotlin
// BAD
val bmp = BitmapFactory.decodeFile(path)
// GOOD: let the image loader size it to the view, or downsample yourself
AsyncImage(model = url, contentDescription = null, modifier = Modifier.size(48.dp)) // Coil
```

Swift:
```swift
// BAD
let image = UIImage(contentsOfFile: path)
// GOOD: ImageIO thumbnail at the target pixel size (48 pt at 3x)
let source = CGImageSourceCreateWithURL(url as CFURL, nil)!
let options = [kCGImageSourceCreateThumbnailFromImageAlways: true,
               kCGImageSourceThumbnailMaxPixelSize: 144] as CFDictionary
let thumb = CGImageSourceCreateThumbnailAtIndex(source, 0, options)
```

Dart:
```dart
// BAD
Image.file(file, width: 48);
// GOOD
Image.file(file, width: 48, cacheWidth: (48 * MediaQuery.devicePixelRatioOf(context)).round());
```

### 8. Leaks are found with a tool, then fixed at the reference

Navigate into and out of a screen five times. If its objects are still alive, something holds them.

Kotlin:
```kotlin
// BAD: singleton keeps the listener, and through it the Activity
override fun onStart() { super.onStart(); DeviceHub.addListener(listener) }
// GOOD: paired registration
override fun onStop() { DeviceHub.removeListener(listener); super.onStop() }
```

Swift:
```swift
// BAD: infinite async loop keeps self alive forever
Task { for await value in stream { self.render(value) } }
// GOOD: owned by the view lifecycle, cancelled when it disappears
.task { for await value in model.stream { model.render(value) } }
```

Dart:
```dart
// BAD: controller never disposed, ticker and listeners leak
late final _controller = AnimationController(vsync: this, duration: _d);
// GOOD
@override
void dispose() { _controller.dispose(); super.dispose(); }
```

Tools: LeakCanary (debug builds only), Xcode Memory Graph and Instruments Leaks and Allocations
generations, DevTools Memory view Diff Snapshots.

### 9. Background work is batched, constrained and deferrable

Every wakeup and radio power-up costs battery. Let the OS schedule work when it is cheap.

Kotlin:
```kotlin
// BAD: own timer, wakes the device every minute on any network
handler.postDelayed(syncRunnable, 60_000)
// GOOD: one unique periodic job, unmetered network, battery not low
val request = PeriodicWorkRequestBuilder<SyncWorker>(6, TimeUnit.HOURS)
    .setConstraints(Constraints.Builder()
        .setRequiredNetworkType(NetworkType.UNMETERED)
        .setRequiresBatteryNotLow(true)
        .build())
    .build()
WorkManager.getInstance(context)
    .enqueueUniquePeriodicWork("sync", ExistingPeriodicWorkPolicy.KEEP, request)
```

Swift:
```swift
// BAD: large upload started on a default session over cellular
// GOOD: background session the system schedules, or a BGProcessingTask
let config = URLSessionConfiguration.background(withIdentifier: "com.example.upload")
config.isDiscretionary = true
let request = BGProcessingTaskRequest(identifier: "com.example.cleanup")
request.requiresExternalPower = true
request.requiresNetworkConnectivity = true
try BGTaskScheduler.shared.submit(request)
```

- iOS: `BGTaskScheduler` identifiers must be listed under `BGTaskSchedulerPermittedIdentifiers` in
  Info.plist, with the Background Modes capability. Call out that Info.plist and capability change.
- Android 15+: `dataSync` and `mediaProcessing` foreground services are limited to 6 hours per 24 hours.
  Android 16 applies job runtime quotas by standby bucket, also to jobs started in the foreground.
- Test with Doze and standby forced (commands in [references/android.md](references/android.md)).

### 10. Network traffic is small, cached and not polled

Kotlin:
```kotlin
// BAD: no cache, the same 300 KB list downloaded on every screen open
val client = OkHttpClient()
// GOOD: HTTP cache honours Cache-Control and ETag from the server
val client = OkHttpClient.Builder()
    .cache(Cache(File(context.cacheDir, "http"), 20L * 1024 * 1024))
    .build()
```

Swift:
```swift
// BAD: prefetching on a default session over cellular and in Low Data Mode
// GOOD: discretionary traffic waits for a cheap network
config.allowsConstrainedNetworkAccess = false
config.allowsExpensiveNetworkAccess = false
config.waitsForConnectivity = true
```

- Paginate; request only the fields the screen shows; let the server compress responses.
- Replace polling with push (FCM, APNs) or with server-driven `Cache-Control` and conditional requests.
- Coalesce telemetry into batches. Device identifiers in payloads are personal data (see
  `mobile-eu-compliance`).

### 11. App size is measured per release and kept down

- Android: `isMinifyEnabled = true` and `isShrinkResources = true` in release (BAD: both off).
  Ship an AAB; inspect with APK Analyzer (Build > Analyze APK, Compare with previous APK).
- iOS: export with "All compatible device variants" and read `App Thinning Size Report.txt`;
  App Store Connect shows the real per-device sizes.
- Flutter: `flutter build appbundle --analyze-size` or `flutter build ios --analyze-size`, then the
  DevTools app size tool. `--split-debug-info` removes symbols from the binary; keep them for crashes.

### 12. Regressions are caught before users see them

- Run Macrobenchmark or XCTest performance tests on a fixed device in CI, nightly at least.
- iOS: set XCTest baselines per device; the test fails when a metric regresses past the baseline.
- Subscribe to MetricKit and watch Android vitals after each staged rollout step.
- Flutter: `flutter drive --profile` with `traceAction` gives a frame summary per run
  ([references/flutter.md](references/flutter.md)). MetricKit subscriber: [references/ios.md](references/ios.md).

## Anti-patterns

- Optimizing without a baseline number, or claiming an improvement without an "after" number.
- Measuring a debug build, an emulator, a simulator or a flagship phone only.
- Reporting the single best run. Use median and P90 over repeated runs.
- Changing several things, then crediting the one you expected to help.
- Adding `remember`, `@Stable`, `RepaintBoundary`, `const` or caching everywhere "for performance"
  without a trace showing the problem.
- Treating a splash screen as a startup fix. It hides TTID; it does not shorten it.
- Moving startup work to a background thread that the first screen then waits on.
- Keeping LeakCanary, StrictMode penalties or verbose tracing in release builds.
- Requesting a battery optimization exemption instead of using WorkManager, FCM or BGTaskScheduler.
- Polling a server every few seconds from the foreground or a foreground service.
- Comparing app sizes between a universal APK or IPA and a thinned or Play-delivered download.

## Checklist

- [ ] Symptom expressed as one metric, with device, OS version and build type written down
- [ ] Release-like build (non-debuggable, `profileable`, R8 on / Release / `--profile`) on a real device
- [ ] Baseline measured with enough iterations; median and P90 recorded
- [ ] Cause located in a trace (Perfetto, Instruments, DevTools), not guessed from code
- [ ] One change at a time; same conditions for the "after" run
- [ ] Android: Baseline Profile and startup profile generated and checked with `CompilationMode`
- [ ] Startup path free of non-critical SDK init, network and disk work; TTFD or extended launch reported
- [ ] No parsing, decoding or I/O on the main thread or UI isolate during scroll or animation
- [ ] Images decoded at display size
- [ ] Repeated navigation leaves no retained screens (LeakCanary, Memory Graph, DevTools diff)
- [ ] Background work uses WorkManager or BGTaskScheduler with constraints; no polling; HTTP cache on
- [ ] Size measured per variant and compared with the previous release
- [ ] Regression guard added: benchmark or performance test, plus field metric to watch

## Output format

~~~markdown
## Performance report: <scope>

Device: <model, OS version>. Build: <benchmark variant | Release via Profile | --profile>.
Tool: <Macrobenchmark | Instruments App Launch | DevTools | ...>. Runs: <n per side>. Statistic: <median, P90>.

| Issue | Metric before | Change | Metric after |
|---|---|---|---|
| Cold start blocked by SDK init | TTID median 1 850 ms, P90 2 100 ms | Lazy analytics, Baseline Profile | TTID median 1 120 ms, P90 1 290 ms |
| Feed scroll jank | frameOverrunMs P90 9.8 | Moved date formatting out of composition | frameOverrunMs P90 -2.1 |

### Evidence
- <trace file or screenshot name, and what it shows>

### Not measured
- <anything that could not be measured, and why>

### Follow-up
- <regression guard added, field metric to watch after release>
~~~

Rules for the report: every "after" number uses the same device, build, tool and run count as its
"before" number. A change that did not beat the run-to-run noise is listed as "no measurable effect".

## Related skills

- `mobile-kotlin`, `mobile-swift`, `mobile-flutter` -- Compose, SwiftUI and widget rules behind most jank fixes
- `mobile-code-review` -- reviewing performance-sensitive changes before merge
- `mobile-testing` -- benchmark and performance test setup alongside unit and UI tests
- `mobile-ci-cd` -- running benchmarks on devices in CI and storing results
- `mobile-ble` -- BLE throughput, connection intervals and background scanning cost
- `mobile-release` -- staged rollouts and watching vitals after release
- `mobile-eu-compliance` -- telemetry payloads that contain device identifiers
