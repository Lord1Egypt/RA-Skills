---
name: mobile-release
description: "Checks store readiness of Android, iOS and Flutter apps for Google Play and the App Store: target API level, Data safety, sensitive permissions, account deletion, Play App Signing, privacy manifest and required-reason APIs, App Review rejections, ATT, TestFlight, versioning, staged and phased rollout, crash gates and rollback. Use before submitting a build, for a store rejection, or to plan a release."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile release

Decide whether a build can ship to Google Play and the App Store, and plan how it ships: check the build
and the project against current store requirements, collect evidence for each item, list the blockers, and
lay out the rollout with stop conditions and a rollback path.

Store policies change several times a year. The agent uses the verified facts below as a starting point,
says when a fact needs re-checking, and never invents a deadline, threshold or guideline number. Anything
not in the table is phrased as "check the current policy" and linked to the console page or guideline name.

## When to use

- "Is this build ready for the Play Store / App Store?" or a release readiness review before a submission.
- A rejection or policy email: Play policy violation, App Review rejection, ITMS-91053 missing API declaration.
- Raising `targetSdk`, adding a sensitive permission or foreground service, or adding a tracking or ad SDK.
- Planning a release: tracks, TestFlight groups, staged or phased rollout, crash gates, rollback.
- Versioning questions: `versionCode`, `CFBundleVersion`, Flutter `version:` in `pubspec.yaml`.

Not for: building the upload pipeline (use `mobile-ci-cd`), GDPR or CRA assessment of the data flows
behind the store forms (use `mobile-eu-compliance`), or a security audit (use `mobile-security`).

## Verified key facts

Checked on 2026-10-15 against the official pages named in the Source column. Re-check before quoting a
date to a customer or planning a release around it.

| Topic | Fact | Source |
|---|---|---|
| Play target API, new apps and updates | Must target Android 16 (API 36) or higher since 31 August 2026. Wear OS and Android Automotive OS: API 35. Android TV and Android XR: API 34 | Play Console Help "Target API level requirements for Google Play apps"; developer.android.com "Meet Google Play's target API level requirement" |
| Play target API, extension | Extension available on request until 1 November 2026 (form in Play Console) | Same pages |
| Play target API, existing apps | Must target API 35 or higher to stay available to new users on devices running a newer Android version | Same pages |
| Play target API, next deadline | No official announcement found for API 37. Check the current policy | Same pages |
| Play App Bundle | Apps created after August 2021 publish app bundles; only legacy apps may still use APKs | Play Console Help "Android App Bundles" |
| Play new personal accounts | Personal accounts created after 13 November 2023 must run a closed test with at least 12 testers opted in for at least 14 consecutive days before production access | Play Console Help "App testing requirements for new personal developer accounts" |
| Android vitals bad behavior thresholds | User-perceived crash rate 1.09% overall, 8% per phone model. User-perceived ANR rate 0.47% overall, 8% per phone model. Excessive partial wake locks 5%. Above a threshold, Play may reduce visibility and show a warning on the listing | developer.android.com "Android vitals" |
| Play staged rollout | Updates only, not the first release. Halting stops new users from getting it; users who have it stay on it. The percentage never increases automatically | Play Console Help "Release app updates with staged rollouts" |
| App Store build requirement | Since 28 April 2026: built with Xcode 26 or later using the iOS 26 (or matching platform 26) SDK | Apple "Upcoming Requirements" |
| App Store minimum deployment target | Since 9 September 2026: iOS and iPadOS apps uploaded must target iOS 13 or later | Apple "Upcoming Requirements" |
| Required reason APIs | Since 1 May 2024, uploads that use a required reason API without an approved reason in the privacy manifest are not accepted | Apple "Describing use of required reason API" |
| Third-party SDK manifests | Since 12 February 2025, submissions must contain a valid privacy manifest for listed commonly used SDKs; binary SDKs on the list also need a signature | Apple "Adding a privacy manifest to your app or third-party SDK"; "Third-party SDK requirements" |
| App Review 4.8 Login Services | Third-party or social login for the primary account requires an equivalent login option that limits data to name and email, lets the user keep the email private, and does not collect interactions for ads without consent. Listed exceptions apply | App Store Review Guidelines 4.8 |
| App Review 5.1.1(v) | Apps that support account creation must offer account deletion within the app | App Store Review Guidelines 5.1.1(v) |
| App Store phased release | 7 days: 1%, 2%, 5%, 10%, 20%, 50%, 100% of users with automatic updates. Pause for up to 30 days in total. Anyone can still download the update manually | App Store Connect Help "Release a version update in phases" |
| TestFlight | Up to 100 internal testers, up to 10,000 external testers. Builds expire after 90 days. The first build for external testers goes to review | App Store Connect Help "TestFlight overview" |

## Workflow

1. **Scope the release.** Platforms, flavors or schemes, store accounts, current live version and build
   number on each store, target date, and who approves. Ask; do not guess store tracks or groups.
2. **Read the build configuration.** Android: `targetSdk`, `minSdk`, `versionCode`, `versionName`,
   signing config, merged manifest permissions and services. iOS: deployment target, Xcode version in CI,
   `CFBundleShortVersionString`, `CFBundleVersion`, `Info.plist` purpose strings, entitlements,
   `PrivacyInfo.xcprivacy`. Flutter: `version:` in `pubspec.yaml`, plus both native projects.
3. **Inventory SDKs and data.** From `libs.versions.toml`, Gradle dependencies, `Package.resolved`,
   `Podfile.lock`, `pubspec.lock`. For each SDK: what it collects, whether it tracks, its privacy manifest.
   This inventory drives the Data safety form, App Privacy details and the privacy manifest.
4. **Check Google Play items** with [Google Play](references/google-play.md): target API, Data safety,
   permission and foreground service declarations, account deletion, app bundle, Play App Signing, tracks,
   pre-launch report.
5. **Check App Store items** with [App Store](references/app-store.md): Xcode and SDK, privacy manifest and
   required reasons, SDK manifests and signatures, App Privacy details, ATT, the common rejection list,
   review notes and demo account, TestFlight.
6. **Plan the rollout** with [Versioning and rollout](references/versioning-and-rollout.md): version
   numbers, release notes, track progression, staged or phased percentages, crash and ANR gates, and the
   rollback plan, including server-side kill switches.
7. **Mark every item** Pass, Fail or N/A with evidence (file and line, console screenshot reference,
   command output). Console-only items the agent cannot see are marked "Not verified" with an owner.
8. **Report** in the output format below. Blockers first. Do not change code, store settings or consoles
   unless asked.

## Rules

### 1. Target API level meets the current Play requirement

```kotlin
// BAD: build.gradle.kts -- uploads rejected for new apps and updates since 31 August 2026
android {
    defaultConfig { targetSdk = 35 }
}

// GOOD: target API 36 or higher, from the version catalog; review behavior changes before raising it
android {
    compileSdk = libs.versions.compileSdk.get().toInt()
    defaultConfig { targetSdk = libs.versions.targetSdk.get().toInt() } // 36
}
```

- Raising `targetSdk` changes runtime behavior (edge-to-edge, foreground services, permissions). Treat it
  as a feature with its own test pass, not a release-day edit. Ask before bumping it.
- Flutter: check `android/app/build.gradle.kts`; `flutter.targetSdkVersion` follows the Flutter SDK
  version, so pin it explicitly if the SDK default lags the Play requirement.

### 2. iOS builds use the required Xcode and SDK

```yaml
# BAD: CI pinned to an old Xcode; App Store Connect rejects the upload
- run: sudo xcode-select -s /Applications/Xcode_16.4.app

# GOOD: Xcode 26 or later (exact path depends on the runner image), checked in the job log
- run: sudo xcode-select -s /Applications/Xcode_26.0.app
- run: xcodebuild -version
```

- `IPHONEOS_DEPLOYMENT_TARGET` of 13.0 or later for uploads since 9 September 2026.

### 3. Build numbers only go up; marketing versions follow semantic versioning

```kotlin
// BAD: same versionCode as the last upload, or a lower one for a hotfix branch
defaultConfig { versionCode = 41; versionName = "2.3" }

// GOOD: versionCode from CI, strictly increasing; versionName is MAJOR.MINOR.PATCH from the tag
defaultConfig {
    versionCode = providers.gradleProperty("versionCode").get().toInt()
    versionName = providers.gradleProperty("versionName").get()
}
```

```yaml
# Flutter pubspec.yaml: build-name+build-number feeds versionName/versionCode and
# CFBundleShortVersionString/CFBundleVersion
version: 2.4.1+20401
```

- Play rejects a `versionCode` already used; the maximum is 2100000000.
- `CFBundleShortVersionString` is three period-separated integers. `CFBundleVersion` must be unique and
  higher for each upload of the same version.

### 4. Sensitive permissions are removed unless they are core and declared

```xml
<!-- BAD: broad permissions "just in case"; each one needs a Play declaration and a review -->
<uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />
<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />
<uses-permission android:name="android.permission.READ_CALL_LOG" />

<!-- GOOD: name the packages you need; BLE scanning without location when no location is derived -->
<queries>
    <package android:name="com.example.vendor.app" />
</queries>
<uses-permission
    android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation" />
```

- Background location: core feature only, Play Console declaration, prominent in-app disclosure before
  the runtime prompt, demo video. Details in [Google Play](references/google-play.md).
- SMS and Call Log: only for the default SMS, Phone or Assistant handler, or a listed exception.
- Check the merged manifest (`app/build/intermediates/merged_manifests/`) and every track: a permission
  pulled in by a library counts, and so does one left in a closed testing release.

### 5. Foreground services declare a type in the manifest and in Play Console

```xml
<!-- BAD: targeting Android 14+ without a type; startForeground() fails at runtime -->
<service android:name=".GatewaySyncService" />

<!-- GOOD: type and matching permission; connectedDevice needs a prerequisite such as BLUETOOTH_CONNECT -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_CONNECTED_DEVICE" />
<service
    android:name=".GatewaySyncService"
    android:foregroundServiceType="connectedDevice"
    android:exported="false" />
```

- Each type used also needs a declaration on the App content page: feature description, user impact if
  deferred, a video of the user triggering it, and the use case.

### 6. Account deletion is in the app, and on Play also on the web

```kotlin
// BAD: deactivation only, or "email support to delete"
fun onDeleteAccount() = api.deactivate(userId)

// GOOD: in-app path in account settings; backend deletes account and associated data
suspend fun deleteAccount() {
    api.deleteAccount()          // server deletes the account record and associated data
    session.clear()
}
```

```swift
// GOOD: iOS -- same path; revoke Sign in with Apple tokens on the server (REST API) when used
func deleteAccount() async throws {
    try await api.deleteAccount()
    await session.clear()
}
```

- Play: also a web link where users can request deletion without the app, entered in the Data safety form.
- App Store: temporary deactivation alone is insufficient. A link to the website is acceptable only if the
  user must finish deletion there, and it must go directly to that page.

### 7. Store privacy forms match the SDK inventory

```text
BAD:  Data safety "No data collected" while Crashlytics and an analytics SDK ship in the bundle.
GOOD: Each SDK in the inventory mapped to data types, purpose, shared or not, optional or not;
      the same answers drive Data safety (Play), App Privacy details (App Store) and PrivacyInfo.xcprivacy.
```

- Both stores hold the developer responsible for third-party SDK collection.
- App Privacy answers can be updated without a new build; Data safety inaccuracies can block updates.

### 8. The privacy manifest declares every required reason API with an approved reason

```xml
<!-- BAD: app uses UserDefaults and file timestamps, no PrivacyInfo.xcprivacy in the target -->

<!-- GOOD: PrivacyInfo.xcprivacy in the app target's resources -->
<key>NSPrivacyTracking</key>
<false/>
<key>NSPrivacyAccessedAPITypes</key>
<array>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array><string>CA92.1</string></array>
    </dict>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array><string>C617.1</string></array>
    </dict>
</array>
```

- Pick reasons that match what the code does; the reason table is in [App Store](references/app-store.md).
- Flutter plugins such as `shared_preferences` wrap `UserDefaults`; use plugin versions that ship their
  own manifest, and declare the app's own use in the Runner target.
- Generate the privacy report from the archive in Xcode Organizer and review it before each submission.

### 9. Third-party SDKs ship their own manifests and signatures

```swift
// BAD: Package.resolved pins an SDK version from before it shipped a privacy manifest
.package(url: "https://github.com/example/analytics-ios", exact: "3.1.0")

// GOOD: version with a bundled PrivacyInfo.xcprivacy (and a signature for binary SDKs on Apple's list)
.package(url: "https://github.com/example/analytics-ios", from: "5.2.0")
```

- An SDK cannot rely on the app's manifest for its own required reason API use, and the app cannot fix a
  missing SDK manifest by declaring it for the SDK. Upgrade or replace the SDK.

### 10. No tracking before App Tracking Transparency authorization

```swift
// BAD: ad SDK started and IDFA read at launch, before any prompt
Ads.start()

// GOOD: ask in context, start tracking features only when authorized
let status = await ATTrackingManager.requestTrackingAuthorization()
if status == .authorized { Ads.enablePersonalizedAds() } else { Ads.enableNonPersonalizedAds() }
```

```xml
<!-- Info.plist: required when requesting authorization; explain the actual use -->
<key>NSUserTrackingUsageDescription</key>
<string>Allows ads based on your activity in other companies' apps and websites.</string>
```

- Do not gate features or offer rewards for allowing tracking (5.1.2(i)). Domains in
  `NSPrivacyTrackingDomains` fail to load until the user grants permission.
- ATT is an Apple requirement on top of, not a replacement for, GDPR consent (see `mobile-eu-compliance`).

### 11. Third-party login comes with an equivalent privacy-preserving option (4.8)

```swift
// BAD: only "Continue with Google" for the primary account
LoginButtons(providers: [.google])

// GOOD: an equivalent option meeting 4.8 (Sign in with Apple meets it), or own accounts only
LoginButtons(providers: [.apple, .google, .email])
```

- Not required for: company-own accounts only, enterprise or education accounts, government eID, or a
  client for a specific third-party service. Quote the guideline exception in the review notes if relied on.

### 12. The submission is complete and reviewable

```text
BAD:  Review notes empty; login required; staging backend down; "Lorem ipsum" in a settings screen;
      screenshots show only the splash screen.
GOOD: Demo account with sample data (or an approved demo mode), backend up for the review window,
      notes explaining hardware-dependent features (BLE device, gateway) with a demo video,
      no placeholder text, screenshots of the app in use, privacy policy URL in metadata and in the app.
```

- Hardware companion apps: reviewers rarely have the device. Explain what works without it and attach a video.
- Play: provide the same test credentials for the pre-launch report and app access.

### 13. Releases go through tracks and a staged or phased rollout with gates

```ruby
# BAD: straight to 100% production from CI
upload_to_play_store(track: "production")

# GOOD: staged rollout fraction; iOS phased release; a human raises the percentage after the gate
upload_to_play_store(track: "production", rollout: "0.05")
upload_to_app_store(phased_release: true, submit_for_review: true)
```

- Gate each increase on crash and ANR rates against the previous release and the vitals thresholds.
- Plan in [Versioning and rollout](references/versioning-and-rollout.md).

### 14. A rollback plan exists before the release starts

```kotlin
// GOOD: risky features behind remote flags with a safe default; a minimum-version gate for emergencies
val newSyncEnabled = remoteConfig.getBoolean("new_ble_sync_enabled") // default false in app defaults
if (BuildConfig.VERSION_CODE < remoteConfig.getLong("min_supported_version_code")) showForceUpdate()
```

```dart
// GOOD: Flutter -- same pattern; the flag defaults to the old path if config cannot be fetched
final useNewSync = remoteConfig.getBool('new_ble_sync_enabled');
```

- Android: halt the staged rollout, fix, ship a higher `versionCode`. There is no downgrade for users who
  already updated.
- iOS: no rollback. Pause the phased release, submit a fix, request an expedited review for a critical bug.
- Server-side kill switches are the only instant rollback on both stores.

## Anti-patterns

- Declaring a build "store ready" without checking the merged manifest and the archived bundle.
- Copying Data safety or App Privacy answers from another app, or answering "no data collected" with
  crash reporting or analytics SDKs in the build.
- Requesting `ACCESS_BACKGROUND_LOCATION` for BLE scanning that does not derive location.
- Using `QUERY_ALL_PACKAGES` to check for one companion app.
- Writing a privacy manifest with reasons that sound acceptable instead of the ones that match the code.
- Hand-editing `versionCode` or `CFBundleVersion`, or reusing build numbers across flavors that share a listing.
- 100% production releases with no staged rollout, no gates and no owner watching vitals.
- Assuming an App Store release can be rolled back, or that a halted Play rollout removes the update
  from users who already have it.
- Shipping a risky BLE or firmware-update change without a remote flag to turn it off.
- Quoting a store deadline, threshold or guideline number from memory instead of the current page.

## Checklist

Google Play:
- [ ] `targetSdk` meets the current requirement for the app's form factor (or an extension is granted)
- [ ] Data safety form matches the SDK inventory; data deletion questions answered
- [ ] Every sensitive permission in the merged manifest is core and declared; none left in test tracks
- [ ] Foreground service types in the manifest and declared in Play Console with a video
- [ ] In-app account deletion and a web deletion link (if accounts exist)
- [ ] App bundle upload; Play App Signing enrolled; upload key stored outside the repo with a reset plan
- [ ] Release tested on internal or closed track; pre-launch report reviewed with test credentials
- [ ] Crash and ANR rates of the current release below the vitals thresholds

App Store:
- [ ] Built with Xcode 26 or later and the 26 SDK; deployment target iOS 13 or later
- [ ] `PrivacyInfo.xcprivacy` in the app target; every required reason API declared with a correct reason
- [ ] Listed third-party SDKs at versions with manifests (and signatures for binaries); privacy report reviewed
- [ ] App Privacy details match the inventory; tracking declared consistently with ATT use
- [ ] ATT prompt before any tracking; `NSUserTrackingUsageDescription` present if requested
- [ ] Login options meet 4.8; in-app account deletion meets 5.1.1(v); privacy policy linked in app and metadata
- [ ] Review notes, demo account, live backend, no placeholder content, accurate screenshots
- [ ] TestFlight build tested by internal testers; external group approved if used

Both:
- [ ] Marketing version is semver; build numbers strictly higher than anything uploaded
- [ ] Release notes written for each store language
- [ ] Staged or phased rollout with gates, owner and stop conditions
- [ ] Rollback plan: kill switches for risky features, minimum-version gate, hotfix path

## Output format

~~~markdown
## Release readiness: <app> <version> (<build numbers>) -- <date>

Facts checked against store pages on <date>. Items marked "Not verified" need the console owner.

| Item | Platform | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| Target API 36 | Android | Fail | `app/build.gradle.kts:14` targetSdk = 35 |
| Background location declared | Android | N/A | Not in merged manifest (`./gradlew :app:processReleaseMainManifest`) |
| FGS type connectedDevice declared | Android | Not verified | Manifest OK (`AndroidManifest.xml:42`); Play Console declaration not visible to the agent |
| Account deletion (in-app + web) | Both | Pass | `SettingsScreen.kt:88`, `AccountView.swift:51`; web link https://example.com/delete |
| Privacy manifest and required reasons | iOS | Fail | `PrivacyInfo.xcprivacy` missing UserDefaults (`CA92.1`) used in `Settings.swift:12` |
| 4.8 Login Services | iOS | Pass | Sign in with Apple offered next to Google (`LoginView.swift:30`) |
| Build numbers increase | Both | Pass | versionCode 20401 > live 20307; CFBundleVersion 20401 > 20307 |

### Blockers
1. <item> -- why it blocks (store rejects / policy violation), fix, owner

### Rollout plan
- Android: internal, closed, production 5%, 20%, 50%, 100%. Gate: crash and ANR rate vs previous release
  and vitals thresholds. Owner <name>
- iOS: TestFlight internal, external, phased release. Pause condition <metric>. Owner <name>
- Rollback: <flags>, <min-version gate>, hotfix path

### Not verified / check the current policy
- <console-only items and policy points that could not be confirmed>
~~~

Status values: Pass, Fail, N/A, Not verified. "Pass" always has evidence; a blocker is any Fail that
causes rejection, policy enforcement or user harm.

## Related skills

- `mobile-ci-cd` -- signing, upload automation, version numbers from CI
- `mobile-eu-compliance` -- GDPR, consent and deletion behind the store privacy forms
- `mobile-security` -- permissions, storage and network findings that also affect store review
- `mobile-ble` -- BLE permissions, foreground services and background behavior of companion apps
- `mobile-testing` -- test pass before a release and for `targetSdk` changes
- `mobile-performance` -- crash, ANR and startup work behind the vitals gates
- `mobile-merge-request` -- describing release and policy changes in the MR
