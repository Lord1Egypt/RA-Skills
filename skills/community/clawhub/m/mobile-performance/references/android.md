# Android performance reference

Load this for startup, jank, memory, battery, network and size work in Kotlin or Java apps, and for the
host side of Flutter apps. Use version catalog aliases for the coordinates below and take current
versions from the Jetpack release notes.

## Benchmark and Baseline Profile modules

Android Studio: File > New > New Module > Baseline Profile Generator (AGP 8.2+). It creates a
`com.android.test` module, applies the Baseline Profile Gradle plugin and adds a generator and a startup
benchmark. Manual setup:

```kotlin
// :baselineprofile/build.gradle.kts
plugins {
    alias(libs.plugins.android.test)
    alias(libs.plugins.androidx.baselineprofile) // id "androidx.baselineprofile"
}
android { targetProjectPath = ":app" }
dependencies {
    implementation(libs.androidx.benchmark.macro.junit4) // androidx.benchmark:benchmark-macro-junit4
    implementation(libs.androidx.test.ext.junit)
}

// :app/build.gradle.kts
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.androidx.baselineprofile)
}
dependencies {
    implementation(libs.androidx.profileinstaller) // androidx.profileinstaller:profileinstaller
    baselineProfile(project(":baselineprofile"))
}
```

```xml
<!-- app AndroidManifest.xml, inside <application>: lets the shell profile a release build -->
<profileable android:shell="true" tools:targetApi="29" />
```

Generator, covering startup and the main journeys:

```kotlin
@RunWith(AndroidJUnit4::class)
@LargeTest
class BaselineProfileGenerator {
    @get:Rule val rule = BaselineProfileRule()

    @Test fun generate() = rule.collect(
        packageName = "com.example.app",
        includeInStartupProfile = true,
    ) {
        pressHome()
        startActivityAndWait()
        device.findObject(By.res("device_list")).fling(Direction.DOWN)
    }
}
```

- Generate: `./gradlew :app:generateBaselineProfile` (or `generate<Variant>BaselineProfile`), on a
  physical device or a Gradle managed device.
- Output: `src/<variant>/generated/baselineProfiles/baseline-prof.txt` and `startup-prof.txt`. Commit
  them. Startup profiles need R8 (`isMinifyEnabled = true`); DEX layout optimization is on by default
  from AGP 8.3.
- Profiles are installed only for release builds. On Android 7 to 8.1 `profileinstaller` installs them
  on first run; from Android 9 Play also uses them at install time.
- Libraries can ship their own Baseline Profiles; startup profiles cannot come from libraries.

## Startup benchmark

```kotlin
@RunWith(AndroidJUnit4::class)
@LargeTest
class StartupBenchmark {
    @get:Rule val rule = MacrobenchmarkRule()

    @Test fun startupNone() = startup(CompilationMode.None())

    @Test fun startupBaselineProfile() =
        startup(CompilationMode.Partial(baselineProfileMode = BaselineProfileMode.Require))

    private fun startup(mode: CompilationMode) = rule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(StartupTimingMetric()),
        compilationMode = mode,
        iterations = 10,
        startupMode = StartupMode.COLD,
        setupBlock = { pressHome() },
    ) {
        startActivityAndWait()
    }
}
```

- `None` is the worst case (fresh install, no profile). `Partial(BaselineProfileMode.Require)` fails if
  no profile is present, so it also guards against a lost profile. `Full` is not what users get.
- Output: `timeToInitialDisplayMs` and `timeToFullDisplayMs` as min, median and max. Compare medians.
- Macrobenchmark refuses debuggable or non-profileable targets and emulators by default. Do not silence
  this with `androidx.benchmark.suppressErrors` for numbers you report.
- Results and Perfetto traces land in the connected device output folder
  (`build/outputs/connected_android_test_additional_output/`). Open traces in Android Studio or
  ui.perfetto.dev.

## Frame benchmark

```kotlin
@Test fun scrollFeed() = rule.measureRepeated(
    packageName = "com.example.app",
    metrics = listOf(FrameTimingMetric()),
    iterations = 5,
    startupMode = StartupMode.WARM,
    setupBlock = { pressHome(); startActivityAndWait() },
) {
    val list = device.findObject(By.res("feed"))
    list.setGestureMargin(device.displayWidth / 5)
    list.fling(Direction.DOWN)
    device.waitForIdle()
}
```

- `frameDurationCpuMs`: CPU time per frame (UI thread and RenderThread), P50 to P99.
- `frameOverrunMs` (API 31+): how late each frame was. Positive values are janky frames. Track P90 and P99.
- Expose test tags as resource ids for UI Automator: `Modifier.semantics { testTagsAsResourceId = true }`
  on the root composable.

## Startup path

- Read the system log line `Displayed <package>/<activity>: +<time>` (TTID) for a quick check; it is
  logged by the system, so disable Logcat filters. Never use it as the reported number.
- Report TTFD: `ComponentActivity.reportFullyDrawn()`, or in Compose `ReportDrawn()`,
  `ReportDrawnWhen { }`, `ReportDrawnAfter { }`. Calling it too early makes TTFD equal TTID.
- Lazy initialization: inject `dagger.Lazy<T>` or `Provider<T>`, create singletons on first use, and
  defer non-critical SDKs until after the first frame.

App Startup (`androidx.startup:startup-runtime`):

```kotlin
class LoggerInitializer : Initializer<Logger> {
    override fun create(context: Context): Logger = Logger.init(context)
    override fun dependencies(): List<Class<out Initializer<*>>> = emptyList()
}
```

```xml
<provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    android:exported="false"
    tools:node="merge">
    <!-- turn off automatic init for one component, then call it later -->
    <meta-data android:name="com.example.LoggerInitializer" tools:node="remove" />
</provider>
```

```kotlin
// later, off the startup path
AppInitializer.getInstance(context).initializeComponent(LoggerInitializer::class.java)
```

- Audit the merged manifest (APK Analyzer) for library `ContentProvider`s; each one runs before
  `Application.onCreate`.
- `StrictMode` with `detectDiskReads()` and `detectNetwork()` in debug builds finds I/O on the main thread.

## Tracing

- Custom sections: `trace("loadFeed") { ... }` from `androidx.tracing`. They appear in Perfetto,
  Android Studio System Trace and Macrobenchmark traces. The app must be `profileable` or debuggable.
- On-device capture: Developer options > System Tracing > Record trace (Quick Settings tile available).
  Traces are `.perfetto-trace` files on Android 10+; open them at ui.perfetto.dev.
- Compose composition tracing: add `androidx.compose.runtime:runtime-tracing` (API 30+ device); system
  traces then show composable names. Strip the strings from production builds with the ProGuard rule
  from the Compose tracing guide.
- What to look for in a startup trace: `bindApplication`, `activityStart`, `Choreographer#doFrame`,
  long `inflate` or composition slices, and main-thread state "Runnable" or "Sleeping" while waiting on a
  lock or binder call.

## Compose jank

The coding rules live in `mobile-kotlin`, references/compose.md. Diagnosis:

- Layout Inspector shows recomposition and skip counts per composable. Count, scroll, count again.
- Compose compiler reports (release build) show which classes are unstable and which composables are
  not skippable:

```kotlin
composeCompiler {
    reportsDestination = layout.buildDirectory.dir("compose_compiler")
    metricsDestination = layout.buildDirectory.dir("compose_compiler")
}
```

- Use reports only when a trace shows recomposition cost. Strong skipping already handles most lambdas.

## Memory and leaks

```kotlin
dependencies {
    debugImplementation(libs.leakcanary.android) // com.squareup.leakcanary:leakcanary-android
}
```

- No code needed. It watches destroyed Activities, Fragments and their Views, cleared ViewModels and
  destroyed Services, and prints the reference chain (Logcat tag `LeakCanary`).
- Fix the first reference in the chain that should not exist (singleton, static, registered listener,
  coroutine in a global scope), not the leaked object.
- Android Studio Memory Profiler: heap dump after forcing GC, filter by your package, look for several
  instances of one Activity or Fragment.
- Bitmaps: decode with the image loader at view size; Play vitals now reports bitmap memory as well.

## Battery and background work

- WorkManager for deferrable work; constraints: `setRequiredNetworkType`, `setRequiresCharging`,
  `setRequiresBatteryNotLow`, `setRequiresDeviceIdle`, `setRequiresStorageNotLow`.
- Periodic work: minimum interval 15 minutes. Use `enqueueUniquePeriodicWork` so restarts do not stack
  duplicate jobs. Backoff defaults to exponential, 30 seconds; the minimum is 10 seconds.
- Doze suspends network, ignores wake locks, defers alarms and jobs until maintenance windows. Use
  `setAndAllowWhileIdle()` only for alarms that must fire; they fire at most once per 9 minutes.
- Push instead of polling: FCM high priority only for user-visible notifications.
- Android 15+: `dataSync` and `mediaProcessing` foreground services get 6 hours per 24 hours;
  `Service.onTimeout(int, int)` is called and the service must stop within seconds.
- Android 16: regular and expedited jobs follow runtime quotas by standby bucket, including jobs started
  while the app is visible and jobs running beside a foreground service. Log
  `WorkInfo.getStopReason()` (`stopReason` in Kotlin) to see why a job stopped.
- Do not ask for `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` unless the core function needs it (Play policy
  lists cases such as companion apps for peripheral devices that keep a persistent connection).

Test commands:

```sh
adb shell dumpsys deviceidle force-idle        # enter Doze
adb shell dumpsys deviceidle unforce
adb shell dumpsys battery reset
adb shell am set-standby-bucket com.example.app rare
adb shell am get-standby-bucket com.example.app
adb shell am compat enable FGS_INTRODUCE_TIME_LIMITS com.example.app   # FGS timeouts on Android 15
```

- Power Profiler (Android Studio, inside System Trace): per-rail power from ODPM on Pixel 6 and later,
  Android 10+. Device-level, so close other apps.
- `PowerMetric` in Macrobenchmark (experimental, Pixel 6 or newer) gives energy per subsystem per run.

## Network

- One `OkHttpClient` per app (shared connection pool and cache). OkHttp requests gzip transparently.
- HTTP cache plus server `Cache-Control` and `ETag` turns repeat loads into 304 responses.
- Paging 3 for long lists; request only fields the screen needs.
- Batch telemetry and BLE logs into one upload job with constraints; never one request per event.

## App size

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}
```

- Ship an AAB. Play generates per-device APKs; the compressed download limit for bundles is 200 MB.
- APK Analyzer: Build > Analyze APK, or drag the APK or AAB into the editor. Compare with previous APK
  shows what grew. Command line: `apkanalyzer` in the SDK command-line tools.
- Play Console app size report shows real download sizes per device configuration.
- WebP for raster images, vector drawables for small icons, and the locale filter of your AGP version
  (`resourceConfigurations` in the size guide) to drop unused translations from libraries.

## Android vitals

| Metric | Bad behavior threshold | Core vital |
|---|---|---|
| User-perceived crash rate | 1.09 % overall, 8 % per phone model | Yes |
| User-perceived ANR rate | 0.47 % overall, 8 % per phone model | Yes |
| Excessive partial wake locks | 5 % of battery sessions (partial wake locks over 3 hours in total) | Yes (beta) |
| Slow cold / warm / hot start | Start of 5 s / 2 s / 1 s or more | No |
| Slow frames | Sessions with more than 50 % of frames over 16 ms | No |
| Frozen frames | Sessions with more than 0.1 % of frames over 700 ms | No |
| Background Wi-Fi scans | More than 4 per hour | No |
| Background network usage | More than 50 MB per day | No |

- Play evaluates over 28 days. Memory and bitmap memory metrics by RAM tier are being added with
  store visibility impact announced for February 2027; read the current vitals overview for the numbers.
- Verify all values on the current Android vitals pages before using them in a report; they change.
