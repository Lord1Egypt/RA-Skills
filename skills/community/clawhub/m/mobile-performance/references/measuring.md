# Measuring reference

Load this before taking any number that will go into a report. Bad method produces numbers that move
by more than the change being measured.

## Lab vs field

| | Lab | Field |
|---|---|---|
| Tools | Macrobenchmark, Perfetto, Instruments, XCTest metrics, DevTools | Android vitals, Play Console, Xcode Organizer, MetricKit |
| Good for | Finding the cause, comparing two builds, blocking regressions in CI | Knowing which problem users actually have, confirming a fix |
| Weakness | One device, one state, synthetic journey | Days of delay, aggregated, no traces for most metrics |

Start from field data to pick the problem, use lab data to fix it, and go back to field data to confirm.

## Device choice

- Real hardware. Emulators and simulators share the host CPU, GPU and memory; their numbers are not
  representative, and Macrobenchmark refuses to run on an emulator by default.
- Pick the device from your field data: a common low or mid-range model in your user base (check the
  device list in Android vitals or the Organizer filters). A flagship hides most problems.
- Keep one dedicated benchmark device per platform for CI so results stay comparable over months.

## Build

| Platform | Measure on | Why |
|---|---|---|
| Android | `benchmark` build type: `initWith(release)`, non-debuggable, `<profileable android:shell="true"/>`, R8 on | Debuggable builds disable ART optimizations |
| iOS | Release configuration via Product > Profile or a performance test scheme | Debug builds add checks and no optimization |
| Flutter | `--profile` (frames, startup trace), release for size | Debug is JIT-compiled with asserts |

Same build for "before" and "after", except for the one change under test. Note the commit hashes.

## Conditions

- Battery above 50 % and not charging during the run unless charging is the scenario. Low battery
  enables power saving; Macrobenchmark errors on low battery by default.
- Let the device cool down between long runs; thermal throttling makes later runs slower.
- Close other apps, disable auto-updates, keep the same network (or airplane mode if the journey allows).
- Same OS version, same language and font scale, same account and data set. A feed with 20 items and
  one with 2 000 are different benchmarks.
- Android: say which compilation state you measured (`CompilationMode.None()`, `Partial` with a
  Baseline Profile, or `DEFAULT`). First launch after install and after an update is the
  user-relevant worst case.
- iOS: say whether the launch was after a reboot, after a force quit, or after other heavy apps; Apple
  treats warm and cold launch as a spectrum.

## How many runs and which statistic

- Startup: at least 10 iterations per variant; report median and P90 (or median and max if only
  min/median/max are available, as with `StartupTimingMetric`).
- Frames: at least 5 iterations of the same scripted journey; report P50, P90 and P99 of
  `frameOverrunMs` or `frameDurationCpuMs`, the hitch metric, or `missed_frame_*_budget_count`.
- XCTest: the block runs `iterationCount + 1` times and the first run is discarded as warm-up; raise
  `iterationCount` for noisy metrics. Set a baseline per device in Xcode so regressions fail the test.
- Never report a single run or the best run.
- Noise check: run the unchanged build twice. If the two medians differ by more than the improvement
  you are claiming, you need more runs or calmer conditions, not a conclusion.

## Startup states

| State | Android | iOS |
|---|---|---|
| Cold | Process not running; `StartupMode.COLD` kills it between iterations | Process not running and dependencies paged out (after reboot or memory pressure) |
| Warm | Process alive, Activity recreated; `StartupMode.WARM` | Process start with system caches warm (for example right after a force quit) |
| Hot | Activity brought to front; `StartupMode.HOT` | Resume of a suspended process, reported separately as resume time |

Android vitals and Macrobenchmark use TTID (first frame) and TTFD (`reportFullyDrawn`). The iOS launch
metric is time to first frame after the launch screen; extended launch covers content loaded after it.

## Reading a trace

1. Find the region: startup from process start to first frame, or one janky frame in the frames track.
2. Look at the main (UI) thread state, not only CPU samples: Running is your code, Runnable means the
   thread waits for a CPU, Sleeping or Blocked means it waits on a lock, I/O, binder or IPC.
3. Expand the longest slices first. Add custom trace sections (`trace("...")` on Android,
   `OSSignposter` on iOS, `Timeline.timeSync` in Dart) around suspects and record again.
4. Write down the slice name and duration; that is the evidence in the report.

Android quick capture without Android Studio: Developer options > System Tracing > Record trace, then
open the `.perfetto-trace` file at ui.perfetto.dev. Pull from `/data/local/traces/` with `adb pull` if
sharing from the device is not possible.

## Report

Use the table from the main skill. Example with full context:

~~~markdown
Device: Samsung Galaxy A15, Android 15. Build: benchmark variant, commit a1b2c3d vs d4e5f6a.
Tool: Macrobenchmark StartupTimingMetric, COLD, CompilationMode.Partial(Require). Runs: 15 per side.

| Issue | Metric before | Change | Metric after |
|---|---|---|---|
| Analytics SDK init on main thread | TTID median 1 640 ms, max 1 910 ms | Deferred init with App Startup + AppInitializer after first frame | TTID median 1 210 ms, max 1 380 ms |
| No startup profile | TTID median 1 210 ms | includeInStartupProfile = true | TTID median 1 150 ms (within noise of 70 ms, kept for field check) |
~~~

- Every "after" uses the same device, build type, tool, mode and run count as its "before".
- Say "within noise" when the change is smaller than the noise check; do not claim it as a win.
- Attach or name the trace files that show the cause.
- List what was not measured and why (no device available, metric requires API 31+, field data not
  yet in).
