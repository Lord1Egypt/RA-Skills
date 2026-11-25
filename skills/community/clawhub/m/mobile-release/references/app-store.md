# App Store release readiness

Load this when checking an iOS or Flutter build for the App Store. Facts were checked on 2026-10-15 against
developer.apple.com pages named in each section. Guideline numbers and wording change; quote the current
App Store Review Guidelines in any reply to App Review.

## Build requirements

Source: Apple "Upcoming Requirements" (developer.apple.com/news/upcoming-requirements).

| Since | Requirement |
|---|---|
| 28 April 2026 | Uploads built with Xcode 26 or later using the iOS 26, iPadOS 26, tvOS 26, visionOS 26 or watchOS 26 SDK |
| 9 September 2026 | iOS and iPadOS apps uploaded must target iOS 13 or later |
| 31 January 2026 | Answers to the updated age rating questions required to keep submitting updates |
| 1 May 2024 | Approved reasons required for required reason APIs, including in third-party SDKs |
| 16 October 2024 | EU: trader status required to submit updates for apps on the EU App Store (DSA) |

No newer future-dated requirement was listed on 2026-10-15. Check the page before each major release and
before pinning the CI Xcode version.

## Privacy manifest

Sources: Apple "Privacy manifest files", "Adding a privacy manifest to your app or third-party SDK",
"Describing use of required reason API".

- File name `PrivacyInfo.xcprivacy`, added to the target's resources (File, New File, App Privacy File).
- App bundles place it at the bundle root on iOS. Swift packages declare it as a resource explicitly.
- Top-level keys:

| Key | Meaning |
|---|---|
| `NSPrivacyTracking` | Whether the app or SDK uses data for tracking as defined for App Tracking Transparency |
| `NSPrivacyTrackingDomains` | Domains used for tracking; requests to them fail until the user grants tracking permission. Requires `NSPrivacyTracking` true |
| `NSPrivacyCollectedDataTypes` | Data types collected, linked or not, used for tracking or not, purposes |
| `NSPrivacyAccessedAPITypes` | Required reason API categories used, each with approved reasons |

- App Store Connect rejects submissions with invalid manifests (unexpected keys or values) and emails the
  path of the invalid file. If it comes from an SDK, update the SDK.
- Generate the privacy report: archive, open Organizer, select the archive, Generate Privacy Report. Review
  it against the App Privacy answers before submission.

## Required reason API reasons

Source: Apple "NSPrivacyAccessedAPIType". Declare only reasons that match the code. Values as of 2026-10-15:

| Category | Reason | Use |
|---|---|---|
| `NSPrivacyAccessedAPICategoryUserDefaults` | `CA92.1` | Read and write data only accessible to the app itself |
| | `1C8F.1` | Data shared within the same App Group |
| | `C56D.1` | Third-party SDK wrapper, only when the app calls it |
| | `AC6B.1` | Managed app configuration and feedback keys (MDM) |
| `NSPrivacyAccessedAPICategoryFileTimestamp` | `C617.1` | Metadata of files in the app, App Group or CloudKit container |
| | `DDA9.1` | Display timestamps to the user; not sent off-device |
| | `3B52.1` | Files the user granted access to (document picker) |
| | `0A2A.1` | Third-party SDK wrapper |
| `NSPrivacyAccessedAPICategorySystemBootTime` | `35F9.1` | Elapsed time between in-app events, timers |
| | `8FFB.1` | Absolute timestamps for in-app events |
| | `3D61.1` | Optional user-submitted bug report |
| `NSPrivacyAccessedAPICategoryDiskSpace` | `85F4.1` | Display disk space to the user |
| | `E174.1` | Check space before writing, or clean up when low |
| | `7D9E.1` | Optional user-submitted bug report |
| | `B728.1` | Health research apps |
| `NSPrivacyAccessedAPICategoryActiveKeyboards` | `3EC4.1` | Custom keyboard apps |
| | `54BD.1` | Customize UI based on active keyboards |

Where these come from in practice:
- `UserDefaults` / `@AppStorage`: the app, and plugins such as Flutter `shared_preferences`.
- File timestamps: `FileManager.attributesOfItem`, `stat`, `URLResourceValues` with dates.
- Boot time: `mach_absolute_time()`, `ProcessInfo.systemUptime` (often inside analytics and crash SDKs).
- Disk space: `volumeAvailableCapacityKey`, `statfs`.

Search the code before writing the manifest:

```sh
grep -rnE "UserDefaults|@AppStorage|systemUptime|mach_absolute_time|attributesOfItem|creationDate|contentModificationDate|volumeAvailableCapacity|statfs|activeInputModes" --include=*.swift --include=*.m .
```

An upload missing a reason gets an email naming the API (ITMS-91053 "Missing API declaration").

## Third-party SDK manifests and signatures

Source: Apple "Third-party SDK requirements".

- Apple lists commonly used SDKs (examples: Alamofire, Firebase modules, FBSDKCoreKit, GoogleSignIn,
  Flutter, `path_provider`, `url_launcher`, `share_plus`, OneSignal, RealmSwift, Lottie). Check the current
  list for every dependency.
- New apps that include a listed SDK, or updates that add one, must include its privacy manifest. Binary
  dependencies on the list must also be signed. Any version, and SDKs that repackage listed ones, count.
- Since 12 February 2025, submissions must contain a valid privacy manifest for these SDKs.
- Xcode validates that a new version of a signed SDK comes from the same developer.
- The app developer remains responsible for all code an SDK brings in.

## App Privacy details

Source: Apple "App privacy details on the App Store".

- Required to submit new apps and updates. Includes data collected by third-party SDKs.
- A data type may be omitted only if it meets all the optional disclosure criteria (not used for tracking,
  not for advertising or other purposes, infrequent, optional, user-provided each time with clear disclosure).
- Data is presumed linked to the user unless de-identified before collection.
- Answers can be updated at any time without a new build, and must stay accurate.

## App Tracking Transparency

Sources: Apple "User privacy and data use"; AppTrackingTransparency framework documentation.

- Tracking: linking user or device data from the app with other companies' data for targeted ads or ad
  measurement, or sharing it with data brokers.
- Ask through ATT before tracking or reading the advertising identifier. Without permission the identifier
  is all zeros; tracking with another identifier (for example a hashed email) is not allowed.
- Not tracking: on-device-only linking, sharing solely for fraud prevention or security, consumer reporting
  for credit decisions.
- `NSUserTrackingUsageDescription` in `Info.plist` explains the use. No incentives and no gating (5.1.2(i)).
- Fingerprinting is not allowed regardless of ATT.

## Common App Review rejections

Source: App Store Review Guidelines (developer.apple.com/app-store/review/guidelines).

| Guideline | What it says (short) | Check |
|---|---|---|
| 2.1(a) App Completeness | Final versions, no placeholder text or temporary content, tested on device, demo account and live backend if login exists; crashing binaries are rejected | Demo account in review notes, backend up, no "TODO" or lorem ipsum strings |
| 2.3 Accurate Metadata | Metadata, including privacy information, matches the app's core experience | Description, screenshots, App Privacy answers current |
| 2.3.3 | Screenshots show the app in use, not only title art, login or splash screen | Screenshot set per device size |
| 2.5.4 | Background services only for intended purposes (VoIP, audio, location, task completion, notifications) | `UIBackgroundModes` justified, BLE background modes used for real features |
| 4.2 Minimum Functionality | More than a repackaged website | WebView-only apps |
| 4.8 Login Services | Third-party or social login for the primary account needs an equivalent option limiting data to name and email, private email, no ad tracking without consent | Sign in with Apple or another compliant option, or a listed exception |
| 5.1.1(i) Privacy Policies | Privacy policy link in App Store Connect metadata and easily accessible in the app | Link in settings or about screen |
| 5.1.1(ii) Permission | Purpose strings clearly and completely describe the use | Every `NS*UsageDescription` specific to the feature |
| 5.1.1(iv) Access | No manipulating or forcing consent; offer alternatives when a permission is declined | App works with location denied (manual entry) |
| 5.1.1(v) Account Sign-In | Apps that support account creation offer account deletion in the app; no login if no significant account features | Deletion path in account settings |
| 5.1.2(i) Data Use and Sharing | ATT permission required to track; no requiring tracking, notifications or location to use the app | ATT flow and feature gating |

4.8 exceptions (no extra login option needed): only the company's own accounts; alternative app marketplace
login; education or enterprise accounts; government or industry citizen ID; a client for a specific
third-party service where users sign in to that service to access their content.

## Account deletion (5.1.1(v))

Source: Apple "Offering account deletion in your app".

- Easy to find, typically in account settings. Delete the entire account record and associated personal data.
- Temporary deactivation alone is insufficient. Extra confirmation steps are allowed; obstruction is not.
- If deletion must finish on a website, link directly to that page.
- Customer service flows (phone, email) only for highly regulated industries (5.1.1(ix)).
- Manual deletion that takes time is acceptable if the user is told how long and gets a confirmation.
- Sign in with Apple: revoke user tokens with the REST API and handle server-to-server notifications.
- Applies to everyone regardless of location, and to automatically created guest accounts.

## Review notes for hardware companion apps

```text
Demo account: reviewer@example.com / (password in the App Review Information field, not here)
Hardware: the app controls the <model> gateway over Bluetooth LE. Without the device, the reviewer can
sign in, browse the demo site and its recorded history. Pairing, live data and firmware update are shown
in the attached video: <link>.
Background mode bluetooth-central: keeps the connection to the paired gateway to receive alarms.
```

## TestFlight

Source: App Store Connect Help "TestFlight overview".

- Internal testers: up to 100 App Store Connect users with access to the app.
- External testers: up to 10,000, by email or public link. The first build added to an external group goes
  to App Review; later builds may not need a full review.
- Builds are available for 90 days.
- Use TestFlight internal for every release candidate; external groups for field testing with devices.

## Phased release and expedited review

Sources: App Store Connect Help "Release a version update in phases"; Apple "App Review".

- Phased release: 7 days at 1%, 2%, 5%, 10%, 20%, 50%, 100% of users with automatic updates. Anyone can
  still update manually from the App Store. Pause for up to 30 days in total, any number of times.
  "Release to All Users" ends it early.
- Removing the app from sale stops the phased release for that version.
- There is no rollback of a released version. Fix forward with a new build.
- Expedited review: request for a critical bug fix (include steps to reproduce on the current version) or a
  time-sensitive event. It is a request, not a guarantee. Apple states it reviews at least 50% of
  submissions in under 24 hours and 90% in under 48 hours.

## Crash monitoring

- Xcode Organizer shows crashes, hangs, energy and launch metrics from users who share analytics.
- MetricKit delivers daily metric reports and diagnostic reports in the app (`MXMetricManager`
  subscriber; iOS 27 adds `MetricManager` with async sequences). Forward them to your backend or crash
  reporter, without personal data.
- App Store Connect has no published crash threshold equivalent to Android vitals; set the team's own gate.
