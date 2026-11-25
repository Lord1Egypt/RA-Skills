# Google Play release readiness

Load this when checking an Android or Flutter build for Google Play. Facts were checked on 2026-10-15 against
the Play Console Help and developer.android.com pages named in each section. Play policies change often:
if a date below is in the past or close, re-check the page before relying on it.

## Target API level

Source: Play Console Help "Target API level requirements for Google Play apps" and developer.android.com
"Meet Google Play's target API level requirement".

| Form factor | New apps and updates must target | Since |
|---|---|---|
| Phone and tablet | Android 16 (API 36) or higher | 31 August 2026 |
| Wear OS | Android 15 (API 35) or higher | 31 August 2026 |
| Android Automotive OS | Android 15 (API 35) or higher | 31 August 2026 |
| Android TV, Android XR | Android 14 (API 34) or higher | Check the current policy (the Help page lists different dates in two places) |

- Extension: can be requested in Play Console until 1 November 2026.
- Existing apps below API 35 (phones) are not offered to new users on devices running a newer Android
  version than the app targets.
- Exception: permanently private apps for internal distribution in one organization.
- Next deadline: no official announcement for API 37 was found on 2026-10-15. Check the current policy
  before planning the next `targetSdk` raise.

What to check:
- `targetSdk` in every application module and flavor that ships, not only `app/`.
- Behavior changes for the new level (foreground services, background starts, edge-to-edge, permissions,
  intents). Run the full test pass on a device with that Android version.

## Data safety section

Source: Play Console Help "Provide information for Google Play's Data safety section".

- Every published app must complete the form, including apps that collect no user data.
- Data collected or shared by third-party code (SDKs) must be included.
- Building advertising or user profiles cannot be declared as ephemeral processing.
- Encryption in transit: the form asks about it; the Help page points to TLS or HTTPS. Answer from what
  the code and SDKs actually do, and check the form's current wording.
- Data deletion questions are mandatory for all developers.
- Inaccurate declarations lead to policy enforcement such as blocked updates or removal.
- The independent security review badge is optional and does not verify the declarations.

Mapping procedure:
1. List SDKs from the dependency graph (`./gradlew :app:dependencies --configuration releaseRuntimeClasspath`).
2. For each SDK, take the vendor's Data safety guidance and confirm it against how the app configures it.
3. Add the app's own collection: account data, telemetry, crash logs, device identifiers, location.
4. Mark each type: collected or shared, required or optional, purpose. Keep the sheet in the repo next
   to the iOS App Privacy sheet so both stores stay consistent.

## Sensitive permissions and declarations

### Background location

Source: Play Console Help "Requesting access to location in the background".

- Only for core functionality. Never solely for ads or analytics.
- Declaration under App content, Sensitive app permissions, Location permissions. Describe one feature.
- Prominent disclosure in normal app use, before the runtime prompt, containing the word "location",
  describing the data and use, saying it works "when the app is closed" or "not in use", and listing every
  feature that uses it. Template from the page: "[This app] collects location data to enable ["feature"]
  even when the app is closed or not in use."
- Video (30 seconds or less recommended) showing the disclosure, the runtime prompt and the feature.
- If not needed, remove the permission from the manifest in all tracks, including test tracks.

BLE companion apps: on Android 12 and later, `BLUETOOTH_SCAN` with `neverForLocation` avoids location
permissions entirely when the app does not derive location from scan results. Ask the firmware or product
owner before setting it if beacons or location features exist.

### SMS and Call Log

Source: Play Console Help "Use of SMS or Call Log permission groups".

- Only for the app registered as the default SMS, Phone or Assistant handler, or a listed temporary exception
  when no alternative exists.
- Declared through the Permissions Declaration Form in Play Console. Apps without it may be removed.

### QUERY_ALL_PACKAGES

Source: Play Console Help "Use of the broad package (App) visibility (QUERY_ALL_PACKAGES) permission".

- Applies to apps targeting API 30 or later.
- Permitted only when the core purpose needs all installed apps (device search, antivirus, file managers,
  browsers). Not allowed if a less broad method works.
- Declared through the Permissions Declaration Form.

```xml
<!-- Prefer package visibility filtering -->
<queries>
    <package android:name="com.example.gateway.setup" />
    <intent>
        <action android:name="android.intent.action.VIEW" />
        <data android:scheme="https" />
    </intent>
</queries>
```

### Foreground service types

Sources: Play Console Help "Understanding Google Play's foreground service requirements";
developer.android.com "Foreground service types".

- Apps targeting Android 14 and above declare a type for each foreground service in the manifest, with
  the matching `FOREGROUND_SERVICE_*` permission.
- Each type used is declared on the App content page with: a description of the feature, the user impact
  if the task is deferred or interrupted, a video showing how the user triggers it, and the use case.
- `connectedDevice` requires one of: a network or NFC manifest permission, a granted Bluetooth or UWB
  runtime permission (for example `BLUETOOTH_CONNECT`), or USB permission.
- Apps targeting Android 15 or higher cannot start a `dataSync` foreground service from `BOOT_COMPLETED`.
- `specialUse` is for cases no other type covers and is reviewed.

Other declarations to look for in App content: full-screen intent, exact alarms, accessibility services,
photo and video permissions, health permissions. Check the current policy for each one the app uses.

## Account deletion

Source: Play Console Help "Understanding Google Play's app account deletion requirements".

- Apps that allow account creation anywhere in the app must provide an in-app path to delete the account
  and associated data, easy to find (for example account settings).
- They must also provide a web link where users can request deletion without reinstalling the app. The
  link is entered in the Data safety form.
- Deleting the account means deleting associated user data. Data kept for security, fraud prevention or
  legal reasons must be disclosed.
- Wear OS and Android TV apps need no in-app option but still need the web link.

## App bundle and Play App Signing

Sources: Play Console Help "Android App Bundles" and "Use Play App Signing".

- Apps created after August 2021 publish Android App Bundles (`.aab`). Only legacy apps may still use APKs.
- New apps are enrolled in Play App Signing by default.
- Upload key: held by the developer (RSA 2048 or larger), signs the bundle before upload. If lost or
  leaked, request an upload key reset in Play Console (Manage Play app signing, Request upload key reset)
  with the new certificate exported as PEM.
- App signing key: held by Google, signs what users install. It can be upgraded through Play Console.
- API keys, Firebase, Google Sign-In and `assetlinks.json` use the app signing key fingerprints from Play
  Console, not the local upload key. If the console shows several fingerprints, register all of them.

```kotlin
// BAD: release signed with a keystore committed to the repo
signingConfigs { create("release") { storeFile = file("release.jks"); storePassword = "changeit" } }

// GOOD: upload key from the CI environment (see mobile-ci-cd)
signingConfigs {
    create("release") {
        storeFile = file(System.getenv("ANDROID_KEYSTORE_PATH"))
        storePassword = System.getenv("ANDROID_KEYSTORE_PASSWORD")
        keyAlias = System.getenv("ANDROID_KEY_ALIAS")
        keyPassword = System.getenv("ANDROID_KEY_PASSWORD")
    }
}
```

## Release tracks

Source: Play Console Help "Set up an open, closed, or internal test".

| Track | Who | Notes |
|---|---|---|
| Internal testing | Up to 100 testers by email | Available within minutes; use for every release candidate |
| Closed testing | Email lists (up to 2,000 users each) or Google Groups | Test link can take hours the first time |
| Open testing | Anyone who joins; visible on Play | Optional cap of at least 1,000 |
| Production | All users | Test-track users get production if it has a higher versionCode |

- New personal developer accounts (created after 13 November 2023): a closed test with at least 12 testers
  opted in for at least 14 consecutive days before applying for production (Play Console Help "App testing
  requirements for new personal developer accounts").
- Managed publishing lets the team control when an approved release goes live. Check the current Play
  Console Help for how it interacts with review times.

## Pre-launch report

Sources: Play Console Help "Use a pre-launch report to identify issues" and "Pre-launch report overview".

- Runs automatically after a bundle upload, subject to device lab capacity. Results usually within an hour.
- Reports stability (crashes, ANRs, restricted API use), performance, accessibility and screenshots.
- Provide a dedicated test account under Pre-launch report, Settings, Test account credentials. Login
  automation works with standard Android widgets, not WebView or OpenGL sign-in.
- Robo scripts recorded in Android Studio guide the crawler; up to three deep links can be added.
- Crashes on test devices do not count toward the app's vitals. The report cannot find every issue.

## Android vitals

Source: developer.android.com "Android vitals".

| Metric | Overall | Per phone model |
|---|---|---|
| User-perceived crash rate | 1.09% | 8% |
| User-perceived ANR rate | 0.47% | 8% |
| Excessive partial wake locks | 5% | - |

- Above a threshold, Play may reduce the app's visibility and show a warning on the store listing.
- Check the evaluation window and the per-watch-model thresholds in Play Console before using them as gates.
