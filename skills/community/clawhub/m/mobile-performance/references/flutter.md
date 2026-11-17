# Flutter performance reference

Load this for measuring Flutter apps. Widget-level fixes (rebuild scope, lists, images, effects) are in
`mobile-flutter`, references/performance.md; this file covers how to measure, read the tools, and where
the host platform tools take over.

## Build mode and device

- Profile mode for all performance work: `flutter run --profile`. It is AOT-compiled like release, with
  tracing for DevTools. Debug mode (JIT, asserts) numbers are meaningless.
- Physical device only, and the slowest one your users reasonably own. Simulators and emulators do not
  represent release behaviour.
- Release mode for size measurements and final confirmation; it has no DevTools connection.

## Frames: UI thread vs raster thread

Each frame has a UI thread part (Dart: build, layout, paint into a layer tree) and a raster thread part
(the engine draws the layer tree with Impeller or Skia on the GPU). Either can miss the budget of about
16 ms at 60 Hz (8 ms at 120 Hz).

| Slow part | Usual cause | Check |
|---|---|---|
| UI thread | Large rebuilds, heavy `build`, sync parsing or I/O, layout of long non-lazy lists | Track Widget Builds, CPU profiler |
| Raster thread | `saveLayer` from opacity, clips, shader masks, blur; large images; many layers | More debugging options toggles |
| Both, only on first run of an animation | Shader compilation (marked dark red in the frames chart) | Usually gone with Impeller |

DevTools Performance view:
- Flutter frames chart: one bar pair per frame (UI, raster). Frames over budget are red.
- Frame analysis tab: hints for the selected janky frame.
- Timeline events: builds, layouts, paints, GC, HTTP, and your own `Timeline` / `TimelineTask` events
  from `dart:developer`.
- Enhance tracing: Track Widget Builds, Track Layouts, Track Paints. They slow frames down; use them to
  find what runs, not to measure how long it takes.
- More debugging options: turn off Render Clip layers, Render Opacity layers, Render Physical Shape
  layers. If raster time drops sharply, that effect is the cost.

Performance overlay: Performance Overlay button in DevTools, `P` in the `flutter run` terminal, or
`showPerformanceOverlay: true` on `MaterialApp`. Top graph is raster (labelled GPU), bottom is UI. View
it only in profile mode.

## Repeatable frame measurements

```dart
// integration_test/scroll_perf_test.dart
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('feed scroll', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    final list = find.byKey(const ValueKey('feed'));
    await binding.traceAction(() async {
      await tester.fling(list, const Offset(0, -2000), 3000);
      await tester.pumpAndSettle();
    }, reportKey: 'feed_scroll');
  });
}
```

```dart
// test_driver/perf_driver.dart
import 'package:flutter_driver/flutter_driver.dart' as driver;
import 'package:integration_test/integration_test_driver.dart';

Future<void> main() => integrationDriver(
      responseDataCallback: (data) async {
        if (data == null) return;
        final timeline = driver.Timeline.fromJson(data['feed_scroll'] as Map<String, dynamic>);
        final summary = driver.TimelineSummary.summarize(timeline);
        await summary.writeTimelineToFile('feed_scroll', pretty: true, includeSummary: true);
      },
    );
```

```sh
flutter drive --driver=test_driver/perf_driver.dart \
  --target=integration_test/scroll_perf_test.dart --profile
```

- Output in `build/`: `feed_scroll.timeline_summary.json` with `average_frame_build_time_millis`,
  `worst_frame_build_time_millis`, `missed_frame_build_budget_count`,
  `average_frame_rasterizer_time_millis`, `worst_frame_rasterizer_time_millis`,
  `missed_frame_rasterizer_budget_count`, `frame_count`.
- Compare `missed_frame_*_budget_count` and the worst times across runs; report the median of the runs.
- The Flutter docs suggest adding `--no-dds` when running on a mobile device or emulator.

## Startup

```sh
flutter run --profile --trace-startup
```

- Writes `build/start_up_info.json` with timings in microseconds, including `timeToFirstFrameMicros`
  and `timeToFrameworkInitMicros`. Check the current Flutter docs for the full key list.
- The user-visible launch also includes native startup. Measure it with the host tools: Macrobenchmark
  `StartupTimingMetric` on Android and `XCTApplicationLaunchMetric` or Instruments App Launch on iOS
  (see [android.md](android.md) and [ios.md](ios.md)).
- Keep `main()` minimal; defer plugin and SDK init that the first frame does not need.
- Android Baseline Profiles cover only the Kotlin and Java part (embedding, plugins). Dart code is
  already AOT-compiled in profile and release builds.

## Memory

DevTools Memory view (profile mode):
- Profile Memory: current allocation by class; toggle Refresh on GC.
- Diff Snapshots: snapshot, open and close the screen several times, snapshot again, diff. A growing
  count of a `State`, controller or model class is the leak.
- Trace Instances: which call stacks allocate instances of selected classes.

Leak causes in Dart:
- Controllers, `FocusNode`, `AnimationController`, `ScrollController` and stream subscriptions not
  disposed or cancelled.
- Closures that capture a short-lived object (often `BuildContext`) stored in a long-lived object.
  Capture the value you need (`Theme.of(context)`) instead of the context.
- Native memory (images, platform views) does not show in the Dart heap; use Android Studio Memory
  Profiler or Instruments Allocations for the host process.

## Battery and network

- Background work runs on the host: the `workmanager` plugin maps to WorkManager on Android and
  `BGTaskScheduler` on iOS; the constraint and Info.plist rules in the main skill apply.
- Timers and periodic `Stream`s keep running while the app is in the background until the OS suspends
  it. Pause them in `AppLifecycleListener` (`onHide`, `onPause`) and resume on `onResume`.
- Use one HTTP client instance, cache responses where the server allows, paginate, and batch telemetry.
- Decode large JSON in `Isolate.run` so the UI isolate keeps its frame budget.

## App size

```sh
flutter build appbundle --analyze-size
flutter build apk --analyze-size
flutter build ios --analyze-size
```

- Each prints a summary and writes a `*-code-size-analysis_*.json` file. Open it with `dart devtools` >
  Open app size tool; load two files to diff releases.
- On iOS, `--analyze-size` builds a `.app` for relative comparison. For real download size, use the
  Xcode App Thinning Size Report (see [ios.md](ios.md)), starting from
  `flutter build ipa --export-method development`.
- `--split-debug-info=<dir>` moves Dart symbols out of the binary and can reduce code size a lot. Keep
  the symbol files per release for crash symbolication.
- Remove unused packages, fonts and assets; check large transitive native SDKs in the host tools (APK
  Analyzer, size report).

## Impeller

- Impeller is the only renderer on iOS; there is no switch back to Skia.
- On Android it is the default on API 29+ and falls back to OpenGL on devices without Vulkan support.
  Opt out for debugging with `flutter run --no-enable-impeller`, or for a release with the
  `io.flutter.embedding.android.EnableImpeller` meta-data set to `false` in `AndroidManifest.xml`. Treat
  an opt-out as temporary and file the rendering bug.
- Shader warm-up steps written for Skia are not needed with Impeller. Re-measure before keeping them.
