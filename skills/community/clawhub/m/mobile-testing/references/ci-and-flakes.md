# CI layout, sharding and flaky tests

Load this when deciding which tests run where in CI, splitting slow suites, or handling flaky tests. For
workflow YAML, SHA-pinned actions, caching keys and report upload, see `mobile-ci-cd`.

## Stages

| Stage | Runs | Target time | Blocks |
|---|---|---|---|
| Pull request | Lint, unit, integration, JVM screen tests, widget tests, screenshot verify | Under 10 min | Merge |
| Merge to main | Instrumented and XCUITest journeys on emulators and simulators, sharded | Under 30 min | Release |
| Nightly | Full journey suite, extra devices and OS versions, quarantined tests, flake hunting | Any | Nothing; reports to the team |
| Release candidate | Device farm or physical devices, BLE rig, manual exploratory checks | Planned | Store upload |

- Upload test reports and failure artifacts on every run, pass or fail, so a red build can be diagnosed
  without re-running it.
- Cache dependencies and build outputs keyed on lockfiles (Gradle, SwiftPM, pub). Never cache test results
  across commits.

## Android

Local tests in parallel on one machine:

```kotlin
tasks.withType<Test>().configureEach {
    maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)
}
```

Instrumented tests, sharded with the AndroidJUnitRunner arguments `numShards` and `shardIndex`
(`shardIndex` is zero-based; run one job per index):

```bash
adb shell am instrument -w -e numShards 4 -e shardIndex 0 \
  com.example.app.test/androidx.test.runner.AndroidJUnitRunner
```

Gradle managed devices give reproducible emulators defined in the build:

```kotlin
android {
    testOptions {
        managedDevices {
            localDevices {
                create("pixel6api34") {
                    device = "Pixel 6"
                    apiLevel = 34
                    systemImageSource = "aosp"
                }
            }
        }
    }
}
```

```bash
./gradlew pixel6api34DebugAndroidTest -Pandroid.testoptions.manageddevices.emulator.gpu=swiftshader_indirect
```

- The GPU flag is needed on CI hosts without hardware rendering (for example hosted GitHub Actions runners).
- Shards per device: `android.experimental.androidTest.numManagedDeviceShards=<n>` in `gradle.properties`.
  Each shard is a separate emulator; large counts can time out while provisioning.
- Automated Test Device images (`systemImageSource = "aosp-atd"` or `"google-atd"`) start faster but disable
  hardware rendering and support only some API levels. Do not run screenshot tests on them.
- Groups (`groups { create("phoneAndTablet") { ... } }`) run the same suite across several devices with
  `phoneAndTabletGroupDebugAndroidTest`.

Isolation between instrumented tests:

```kotlin
android {
    defaultConfig {
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        testInstrumentationRunnerArguments["clearPackageData"] = "true"
    }
    testOptions { execution = "ANDROIDX_TEST_ORCHESTRATOR" }
}
dependencies { androidTestUtil(libs.androidx.test.orchestrator) }
```

The orchestrator restarts the app for every test, so it is slower. Use it where state leaks, not by default.

## iOS

Build once, test many times:

```bash
xcodebuild build-for-testing -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' \
  -derivedDataPath build
xcodebuild test-without-building -xctestrun build/Build/Products/<name>.xctestrun \
  -destination 'platform=iOS Simulator,name=iPhone 16' -resultBundlePath results/shard-0.xcresult
```

- Parallel workers on one machine: `-parallel-testing-enabled YES` and `-parallel-testing-worker-count <n>`
  (or `-maximum-parallel-testing-workers <n>`).
- Several simulators in one job: pass multiple `-destination` values and
  `-parallelize-tests-among-destinations` to split test classes among them instead of running everything
  on each.
- Across CI jobs: list tests with `-enumerate-tests -test-enumeration-style flat`, split the list, and give
  each job its slice with repeated `-only-testing Target/Class` arguments.
- Select a test plan with `-testPlan <name>`, or one configuration with `-only-test-configuration <name>`.
- Timeouts: `-test-timeouts-enabled YES` with `-default-test-execution-time-allowance <seconds>`, so a hung
  test fails instead of hanging the runner.
- Coverage: `-enableCodeCoverage YES`. The result bundle holds coverage and attachments; upload it.
- Variables for the test process need the `TEST_RUNNER_` prefix, for example
  `TEST_RUNNER_SNAPSHOT_TESTING_RECORD=never`.
- Use the test plan option to randomize execution order in at least one scheduled run.

## Flutter

```yaml
# GitHub Actions matrix: one job per shard
strategy:
  matrix:
    shard: [0, 1, 2, 3]
steps:
  - uses: actions/checkout@<sha> # vX.Y.Z
  - uses: subosito/flutter-action@<sha> # vX.Y.Z
    with:
      cache: true
  - run: flutter test --total-shards 4 --shard-index ${{ matrix.shard }} --exclude-tags quarantine
```

- `--shard-index` is zero-based and must be below `--total-shards`.
- `--test-randomize-ordering-seed random` in one job finds order-dependent tests. To reproduce a failure,
  re-run with the same numeric seed (a 32-bit unsigned integer); log the seed the job used.
- `-j` / `--concurrency` sets parallel test processes for unit and widget tests and is ignored for
  integration tests.
- Goldens run only on the pinned platform job (`--tags golden`).

## Flaky tests

A flaky test passes and fails on the same code. It costs every engineer time and teaches the team to ignore
red builds.

### Causes, in order of how often they show up

1. Real time: sleeps, real `delay`, `DateTime.now()`, timeouts tuned to one machine.
2. Missing synchronization: asserting before background work finishes; work the framework cannot see.
3. Shared state: static fakes, a database or preferences left by the previous test, test order.
4. Environment: network, real backend, emulator animations, locale and time zone of the host.
5. Concurrency bugs in production code. These are real defects; the test is doing its job.

### Process

1. Detect: track per-test pass and fail history from CI reports. A test that failed and then passed on
   retry is flaky by definition.
2. Quarantine within a day: move it out of the blocking job with a tag, category or disabled trait that
   names a ticket and an owner. It keeps running in the nightly job.
3. Fix or delete within an agreed time (for example two weeks). A quarantined test with no owner is
   deleted, and the gap it leaves is recorded in the test plan.
4. Reproduce locally by repetition: `xcodebuild test -only-testing <id> -test-iterations 50
   -run-tests-until-failure`; Flutter with a fixed `--test-randomize-ordering-seed`; Android by running the
   class in a loop on a managed device.
5. Fix the cause from the list above. Do not raise timeouts as the fix.

### Retries

Retries are allowed only when they are visible.

```kotlin
// build.gradle.kts, JVM test tasks only; plugin id org.gradle.test-retry
tasks.withType<Test>().configureEach {
    retry {
        maxRetries.set(2)
        maxFailures.set(20)          // stop retrying when the build is genuinely broken
        failOnPassedAfterRetry.set(false)
    }
}
```

- The plugin augments Gradle `Test` tasks (JUnit 4, JUnit 5, Spock, TestNG). It does not cover
  instrumented tests.
- `failOnPassedAfterRetry.set(true)` fails the build on any flake; use it once the suite is clean.
- iOS: `-retry-tests-on-failure` with `-test-iterations <max>` (default maximum 3). The result bundle shows
  which tests needed a retry; publish that list.
- Never wrap the whole CI job in a retry loop. It hides flakes and multiplies cost.
