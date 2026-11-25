# Versioning, rollout and rollback

Load this when choosing version numbers, writing release notes, planning a staged or phased rollout, or
preparing a rollback plan. Store facts are from the pages named in the other two references, checked on
2026-10-15.

## Version numbers

Two numbers per platform. The marketing version is for people; the build number is for the store and the OS.

| | Android | iOS | Flutter (`pubspec.yaml`) |
|---|---|---|---|
| Marketing version | `versionName` (string, shown to users) | `CFBundleShortVersionString` (three period-separated integers) | `version: 2.4.1+...` (build name) |
| Build number | `versionCode` (positive integer, max 2100000000, never reused on Play) | `CFBundleVersion` (one to three period-separated integers) | `version: ...+20401` (build number) |

Rules:
- Marketing version follows semantic versioning `MAJOR.MINOR.PATCH`. It comes from the release tag.
- Build numbers strictly increase across every upload, on every track and branch, including hotfixes.
  Android uses `versionCode` to block downgrades; Play rejects a reused code.
- One build-number scheme for both platforms makes crash reports and support tickets easier to match.
  A common scheme: `MAJOR * 10000 + MINOR * 100 + PATCH` with room for rebuilds, or a CI run number
  with an offset (see `mobile-ci-cd`). Check the scheme cannot overflow or collide with past uploads.
- Flavors that share one Play listing need disjoint `versionCode` ranges.
- KMP and Flutter: one source of truth (tag or `pubspec.yaml`), passed to both native builds.

```kotlin
// GOOD: build.gradle.kts -- fail the build instead of uploading a wrong number
val versionCodeProp = providers.gradleProperty("versionCode").orNull?.toIntOrNull()
    ?: error("Pass -PversionCode=<int>")
android {
    defaultConfig {
        versionCode = versionCodeProp
        versionName = providers.gradleProperty("versionName").get()
    }
}
```

```text
# GOOD: iOS -- Config/Version.xcconfig, overridden from CI
MARKETING_VERSION = 2.4.1
CURRENT_PROJECT_VERSION = 20401
```

## Release notes

- Written per release, per store language, from the merged changes. User-facing changes only; no ticket
  numbers or internal names.
- Mention security fixes without exploit details. Mention required actions (re-pair the device, update the
  gateway firmware) first.
- Play release notes and App Store "What's New" have length limits. Check the current limit in the console.
- Keep the source text in the repo (for example `fastlane/metadata/`) so it is reviewed with the release.

```text
BAD:  "Bug fixes and performance improvements. JIRA-1234, refactored BleManager."
GOOD: "Pairing with the Gateway 2 is faster and retries automatically if the connection drops.
       Fixed a crash when opening history without a network connection."
```

## Rollout plan

### Android (Play)

1. Upload to internal testing. Smoke test on real devices, including the oldest supported Android version
   and the newest one.
2. Promote to closed (and optionally open) testing. Review the pre-launch report.
3. Production staged rollout. Suggested steps: 1% or 5%, 20%, 50%, 100%. Staged rollout is for updates
   only; the first production release goes to everyone.
4. Raise the percentage manually after each gate passes. It never increases automatically.

### iOS (App Store)

1. TestFlight internal for every release candidate; external groups for field tests.
2. Submit with phased release on. Seven days at 1%, 2%, 5%, 10%, 20%, 50%, 100% of users with automatic
   updates; manual updates are not limited.
3. Pause (up to 30 days in total) if a gate fails. "Release to All Users" only after the gate passes.

### Gates

Decide the numbers before the rollout starts, and write them in the release ticket.

| Gate | Android source | iOS source | Example stop condition |
|---|---|---|---|
| Crash rate | Play Console vitals, Crashlytics | Xcode Organizer, MetricKit, crash reporter | Crash-free users below previous release, or user-perceived crash rate approaching 1.09% |
| ANR or hang rate | Play Console vitals | Organizer hangs, MetricKit hang diagnostics | ANR rate approaching 0.47%, or hangs up vs previous release |
| Per-device spikes | Vitals per phone model (8% threshold) | Organizer by device | One model far above the rest |
| Feature health | Backend metrics, BLE connect success rate, firmware update success rate | Same | Pairing or update success drops |
| Support signals | Reviews, tickets | Same | New issue cluster |

The 1.09%, 0.47% and 8% figures are Play's bad behavior thresholds (developer.android.com "Android
vitals"). A release gate should trigger well below them; a threshold breach is already a store penalty.

## Rollback

Neither store can put an older build back on devices that already updated. Plan for fixing forward, and
make risky features switchable from the server.

### Android

1. Halt the staged rollout in Play Console. No new users get the version; users who have it keep it.
2. Turn off the faulty feature with its remote flag if one exists.
3. Build the fix with a higher `versionCode` (a rebuild of the previous code also needs a higher
   `versionCode`). Release it, staged again.
4. Resuming a halted rollout targets the same set of users, so only resume a version you trust.

### iOS

1. Pause the phased release. Users with automatic updates stop receiving it; manual updates still work.
2. Turn off the faulty feature remotely.
3. Submit a fix. For a critical bug, request an expedited review with steps to reproduce on the current
   version. It is not guaranteed.
4. If the release is harmful and no fix is ready, removing the app from sale is a last resort with
   side effects (the phased release cannot be restarted for that version). Check the current App Store
   Connect Help before doing it.

### Kill switches and minimum version

- Every risky change (new BLE stack, firmware update flow, sync engine, payment) ships behind a remote flag
  with an in-app default that keeps the old behavior when the config cannot be fetched.
- A minimum supported version from the backend forces an update when a build is unsafe (Play In-App
  Updates immediate flow on Android, a blocking screen with the App Store link on iOS).
- Flags are configuration, not secrets. Do not put keys or credentials in remote config.
- Remove flags after the rollout completes, or they become permanent forks of the code.

```kotlin
// GOOD: flag with safe default; evaluated once per session, off the main thread
class FeatureFlags @Inject constructor(private val remote: RemoteConfigSource) {
    suspend fun newBleSyncEnabled(): Boolean =
        runCatching { remote.getBoolean("new_ble_sync_enabled") }.getOrDefault(false)
}
```

```swift
// GOOD: same on iOS
func newBleSyncEnabled() async -> Bool {
    (try? await remoteConfig.bool(for: "new_ble_sync_enabled")) ?? false
}
```

```dart
// GOOD: Flutter
Future<bool> newBleSyncEnabled() async {
  try {
    return await remoteConfig.getBool('new_ble_sync_enabled');
  } catch (_) {
    return false;
  }
}
```

## Release ticket template

```text
Release: <app> <version> (<versionCode> / <CFBundleVersion>)
Owner: <name>          Approver: <name>
Scope: <merged MRs>    Risky changes and their flags: <list>
Gates: crash <x>, ANR/hang <y>, feature metric <z>, checked at <times>
Android: internal <date>, closed <date>, production 5% <date>, 20%, 50%, 100%
iOS: TestFlight <date>, submitted <date>, phased release start <date>
Rollback: halt / pause, flags to turn off, hotfix branch, expedited review criteria
```
