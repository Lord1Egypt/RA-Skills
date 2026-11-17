# iOS performance reference

Load this for launch time, hangs, hitches, SwiftUI update cost, memory, energy, network and size work
in Swift apps, and for the host side of Flutter apps on iOS.

## Ground rules for iOS numbers

- Profile with Product > Profile, which builds the Release configuration by default. Check the scheme.
- Use a physical device, ideally the oldest model you support. The simulator never issues memory
  warnings or out-of-memory terminations and runs on Mac hardware.
- Launch varies with device state (cold after reboot or memory pressure, warm after a force quit).
  Measure several runs per state and say which state you measured.

## Launch time

Field data:
- Xcode Organizer > Launch Time: milliseconds from icon tap to first frame after the launch screen,
  50th and 90th percentile, per device and release.
- Organizer > Launches: the slowest functions during launch, with stack traces.
- MetricKit `MXAppLaunchMetric`: `histogrammedTimeToFirstDraw`, `histogrammedOptimizedTimeToFirstDraw`,
  `histogrammedApplicationResumeTime`, and `histogrammedExtendedLaunch` (iOS 16+).

Lab:
- Instruments App Launch template: time profile plus thread states during launch. Blocked main thread
  time shows waits on locks, I/O or IPC.
- Time Profiler template: the App Life Cycle track splits launch into process initialization, UIKit
  initialization, initial scene rendering and initial frame rendering.
- dyld Activity instrument: time spent loading libraries and running static initializers.

```swift
final class LaunchTests: XCTestCase {
    func testColdLaunch() {
        measure(metrics: [XCTApplicationLaunchMetric()]) {
            XCUIApplication().launch()
        }
    }

    func testLaunchUntilResponsive() {
        measure(metrics: [XCTApplicationLaunchMetric(waitUntilResponsive: true)]) {
            XCUIApplication().launch()
        }
    }
}
```

What makes launch slow, in the order to check:
1. Many embedded dynamic frameworks. Merge them (mergeable libraries, Xcode 15+), link statically, or
   drop the dependency.
2. Static initializers: C++ static constructors, Objective-C `+load`, `__attribute__((constructor))`.
3. Work in `application(_:didFinishLaunchingWithOptions:)`, `App.init` or the first view's `init` and
   `body`: database migration, network, SDK setup, large file reads.
4. A complex first screen. Show cached or placeholder content and fill it in after the first frame.

Extended launch (content actually ready), iOS 16+:

```swift
@MainActor
func loadInitialContent() async {
    let id = MXLaunchTaskID("initial-content")
    try? MXMetricManager.extendLaunchMeasurement(forTaskID: id)
    defer { try? MXMetricManager.finishExtendedLaunchMeasurement(forTaskID: id) }
    await feed.load()
}
```

- Start the first task before the first scene becomes active; at most 16 tasks.
- For your own lab view of post-launch work, wrap it in an `OSSignposter` interval on a log with the
  `.pointsOfInterest` category; it appears in the Points of Interest track in Instruments.

## Hangs

- A delay over about 100 ms in a discrete interaction (tap, key press) is noticeable. Assume the main
  thread has under half of that.
- On device: Settings > Developer > Hang Detection reports hangs in development and TestFlight builds.
- Instruments: Time Profiler and the Hitches template include the Hangs instrument (iOS 16+).
- Field: Organizer Hangs, and `MXHangDiagnostic` (`hangDuration`, `callStackTree`) in
  `MXDiagnosticPayload.hangDiagnostics`, delivered immediately on iOS 15+.

```swift
// BAD: synchronous work in a Task created in a view inherits the main actor
Button("Export") { Task { let file = export(items); share(file) } }

// GOOD: CPU work in a function that leaves the caller's actor
@concurrent nonisolated func export(_ items: [Item]) async -> URL { /* ... */ }
Button("Export") { Task { share(await export(items)) } }
```

`@concurrent` is Swift 6.2. With the `NonisolatedNonsendingByDefault` feature on, a plain
`nonisolated async` function runs on the caller's actor; see `mobile-swift`, references/concurrency.md.

## Hitches and SwiftUI update cost

- Hitch: a frame not ready by its deadline (8.3 ms at 120 Hz, 16.7 ms at 60 Hz). Commit hitches come
  from main-thread work; render hitches from a scene too complex for the render server.
- Organizer hitch rate in ms of pause per second: at or below 10 ms/s is good; Apple lists 25 and 50
  ms/s as the warning and critical levels.
- Instruments Animation Hitches template; record on an older device while scrolling.
- Keep per-frame main-thread work, including table and collection data source calls, under about 5 ms.

SwiftUI template in Instruments (Product > Profile > SwiftUI):
- View Body Updates lanes per module show long `body` evaluations; select one and read the Time
  Profiler call tree for that range.
- Update Groups and the cause-and-effect graph ("Show Causes") show why a view updated. Frequent
  updates from an `ObservableObject` with many `@Published` properties usually disappear after moving to
  `@Observable`.
- `Self._printChanges()` inside `body` prints which input changed. It is an underscored debugging aid;
  never ship it.

```swift
// BAD: sorting and formatter creation on every body evaluation
var body: some View {
    let sorted = readings.sorted { $0.date > $1.date }
    List(sorted) { Text(DateFormatter().string(from: $0.date)) }
}

// GOOD: sorted once in the model, formatting by format style
var body: some View {
    List(model.sortedReadings) { Text($0.date, format: .dateTime.hour().minute()) }
}
```

Scrolling performance test:

```swift
func testFeedScrolling() {
    let app = XCUIApplication()
    app.launch()
    let options = XCTMeasureOptions()
    options.invocationOptions = [.manuallyStop]
    measure(metrics: [XCTOSSignpostMetric.scrollingAndDecelerationMetric], options: options) {
        app.collectionViews.firstMatch.swipeUp(velocity: .fast)
        stopMeasuring()
        app.collectionViews.firstMatch.swipeDown(velocity: .fast)
    }
}
```

- iOS 26 adds `XCTHitchMetric(application:)` for hitch counts in performance tests.
- `XCTMeasureOptions.iterationCount`: the block runs `iterationCount + 1` times; the first run is
  discarded as warm-up.

## Memory and leaks

- Xcode Debug Memory Graph: shows objects and who references them; leaked cycles are flagged. Turn on
  Malloc Stack Logging in the scheme Diagnostics to get allocation stack traces.
- Instruments Allocations: use Mark Generation before and after a feature (open and close a screen five
  times). Objects surviving every generation are the leak or the cache to bound.
- Instruments Leaks: finds memory nothing references any more, including retain cycles. Abandoned
  memory that is still referenced (a screen held by a singleton, an unbounded cache) needs Allocations
  generations or the Memory Graph.
- `XCTMemoryMetric` measures physical memory change across a test block.
- Common causes: closures capturing `self` stored on `self`, timers, `NotificationCenter` block observers
  without removal, delegates declared `strong`, unstructured `Task` loops over infinite sequences.
- Jetsam (out-of-memory) terminations show up in Organizer and as jetsam event reports, not as crashes.

## Energy and background work

- MetricKit battery-related metrics: `cpuMetrics`, `gpuMetrics`, `displayMetrics`,
  `locationActivityMetrics`, `networkTransferMetrics`, `cellularConditionMetrics`.
- Organizer Energy reports show energy issues reported from the field.
- Background work: `BGAppRefreshTaskRequest` for short refresh, `BGProcessingTaskRequest` with
  `requiresExternalPower` and `requiresNetworkConnectivity` for heavy work. Identifiers must be in
  `BGTaskSchedulerPermittedIdentifiers` (Info.plist) and the Background Modes capability must be on.
- Large transfers: `URLSessionConfiguration.background(withIdentifier:)` with `isDiscretionary = true`;
  the system may wait for Wi-Fi and power.
- Location: the lowest accuracy that works, stop updates when not needed, significant-change or visits
  monitoring instead of continuous GPS.

## Network

- `URLCache` with a disk capacity sized for your content; send and honour `Cache-Control` and `ETag`.
- For discretionary traffic: `allowsConstrainedNetworkAccess = false` (Low Data Mode),
  `allowsExpensiveNetworkAccess = false`, `waitsForConnectivity = true`. Test with Settings > Developer
  > Network Override, and Network Link Conditioner for slow networks.
- Instruments Network template shows connections and transfer sizes per request.

## MetricKit subscriber

```swift
import MetricKit

final class MetricsCollector: NSObject, MXMetricManagerSubscriber {
    func start() { MXMetricManager.shared.add(self) } // safe to call during launch

    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads { send(payload.jsonRepresentation()) } // daily
    }

    func didReceive(_ payloads: [MXDiagnosticPayload]) {
        for payload in payloads { send(payload.jsonRepresentation()) } // hangs, crashes, launch
    }

    private func send(_ json: Data) { /* queue for batched upload */ }
}
```

- Metrics arrive at most once per day per source, only on physical devices; diagnostics arrive
  immediately on iOS 15+. `pastPayloads` and `pastDiagnosticPayloads` return earlier reports.
- Payloads include device and OS metadata. If you upload them linked to a user or device identifier,
  treat them as personal data and reflect that in the App Store privacy details.

## App size

- Archive, export as Ad Hoc, Development or Enterprise with "All compatible device variants" for app
  thinning. The export folder contains `App Thinning Size Report.txt` with compressed (download) and
  uncompressed (install) size per variant.
- Automate: `xcodebuild -exportArchive -archivePath App.xcarchive -exportPath out -exportOptionsPlist
  Options.plist`, with the `thinning` key set to `<thin-for-all-variants>` in the plist.
- The `.app`, `.xcarchive` and uploaded `.ipa` are not valid size measurements. App Store Connect shows
  the real per-device sizes.
- Common wins: asset catalogs (enables thinning and compression), remove unused assets and fonts, ODR
  or Background Assets for large optional content, fewer third-party SDKs.
