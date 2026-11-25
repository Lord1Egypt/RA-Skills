# Packages and tooling reference

Load this when creating or changing Swift packages, access levels, lint and format configuration,
`Info.plist`, entitlements or the privacy manifest.

## Layout

```
App/                      Xcode app target: composition root, App struct, assets, entitlements
Packages/
  Core/                   Package.swift with targets: CoreModels, CoreNetworking, CoreBLE, CoreTesting
  DeviceFeature/          Package.swift: DeviceFeature, DeviceFeatureTests
  FirmwareFeature/        Package.swift: FirmwareFeature, FirmwareFeatureTests
```

- The app target is thin: it wires dependencies and hosts the root view.
- Features depend on core modules, never on other features. Cross-feature navigation goes through
  routes or closures provided by the app.
- Shared fakes live in a testing target (for example `CoreTesting`) that only test targets depend on.

## Package.swift

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "DeviceFeature",
    platforms: [.iOS(.v17)],
    products: [
        .library(name: "DeviceFeature", targets: ["DeviceFeature"]),
    ],
    dependencies: [
        .package(path: "../Core"),
    ],
    targets: [
        .target(
            name: "DeviceFeature",
            dependencies: [
                .product(name: "CoreModels", package: "Core"),
                .product(name: "CoreBLE", package: "Core"),
            ],
            resources: [.process("Resources")]
        ),
        .testTarget(
            name: "DeviceFeatureTests",
            dependencies: [
                "DeviceFeature",
                .product(name: "CoreTesting", package: "Core"),
            ]
        ),
    ],
    swiftLanguageModes: [.v6]
)
```

- Declare every module the target imports. Do not rely on something being linked transitively.
- Resources are loaded with `Bundle.module`, never `Bundle.main`, inside a package.
- Remote dependencies use a version requirement (`from: "2.1.0"`), not a branch. Commit
  `Package.resolved` for the app.
- Opt into upcoming features per target with `swiftSettings: [.enableUpcomingFeature("ExistentialAny")]`.
- With tools version 6.2 or later, `swiftSettings: [.defaultIsolation(MainActor.self)]` makes a UI
  module main-actor by default. Do not use it for networking, parsing or BLE transport modules.

## Access control

| Level | Visible to | Use for |
|---|---|---|
| `private` | Enclosing declaration and its extensions in the same file | Implementation details |
| `fileprivate` | Same file | Rare; helpers shared by several types in one file |
| `internal` (default) | Same module | Almost everything |
| `package` | All targets in the same Swift package | Helpers shared between targets of one package |
| `public` | Any importing module | The module's API |
| `open` | Any importing module, subclassable | Only for classes designed for subclassing |

- Start `internal`, widen only when a caller in another module needs it.
- A `public` type needs a `public init` if other modules construct it; the memberwise init is internal.
- Public types that cross isolation declare `Sendable` explicitly; it is not inferred for public types.
- `@testable import` in tests only. Production code never relies on it.

## SwiftLint

```yaml
# .swiftlint.yml
included:
  - App
  - Packages
excluded:
  - "**/.build"
opt_in_rules:
  - force_unwrapping
  - implicitly_unwrapped_optional
  - unowned_variable_capture
  - empty_count
  - first_where
  - fatal_error_message
line_length:
  warning: 140
  error: 200
```

- `force_cast` and `force_try` are on by default; keep them on.
- Run `swiftlint --strict` in CI so warnings fail the build.
- Disable a rule inline with `// swiftlint:disable:next <rule>` and a reason, never file-wide.

## Formatting

- Pick one formatter for the repository: SwiftFormat (`.swiftformat` config) or the `swift-format` tool
  shipped with the Swift toolchain. Running both causes churn.
- SwiftFormat example:

```
# .swiftformat
--swiftversion 6.0
--indent 4
--maxwidth 140
--exclude **/.build
```

- CI runs the formatter in lint mode (`swiftformat --lint .`) and fails on differences.
- Formatting-only changes go in their own commit.

## Info.plist and entitlements

Every addition here must be listed in the change summary because it affects signing, App Review or
user prompts.

- Usage descriptions explain the user benefit in plain language:
  `NSBluetoothAlwaysUsageDescription`, `NSCameraUsageDescription`,
  `NSLocationWhenInUseUsageDescription`, `NSLocalNetworkUsageDescription`.
  Accessing Bluetooth, camera or microphone without the key terminates the app.
- `UIBackgroundModes` (`bluetooth-central`, `location`, `remote-notification`, `processing`) must match
  real behaviour; App Review rejects unused modes.
- Entitlements such as Push Notifications, App Groups, Keychain Sharing and Associated Domains require
  the capability on the App ID and a regenerated provisioning profile. Flag this for whoever owns signing.
- App Transport Security exceptions (`NSAppTransportSecurity`) need a written justification. Never add
  `NSAllowsArbitraryLoads` for production traffic.

## Privacy manifest (PrivacyInfo.xcprivacy)

The app and every SDK that uses required-reason APIs or collects data ships a `PrivacyInfo.xcprivacy`.

```xml
<key>NSPrivacyTracking</key>
<false/>
<key>NSPrivacyTrackingDomains</key>
<array/>
<key>NSPrivacyCollectedDataTypes</key>
<array/>
<key>NSPrivacyAccessedAPITypes</key>
<array>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array>
            <string>CA92.1</string>
        </array>
    </dict>
</array>
```

- Required-reason API categories include `UserDefaults`, file timestamps, system boot time, disk space
  and active keyboards. Adding code that calls one of these means adding or updating an entry with an
  approved reason code from Apple's documentation. Do not guess a reason code.
- Collected data types (device IDs, location, diagnostics, telemetry) must match what the app and its
  SDKs actually send, including whether it is linked to the user and used for tracking.
- A Swift package that needs its own manifest includes it as a resource:
  `resources: [.copy("PrivacyInfo.xcprivacy")]`.
- Generate the privacy report from an archive in the Xcode Organizer before release and review it.
