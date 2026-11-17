# Platforms

## Overview

Perry compiles to native executables on 10 platforms. Each platform uses its native UI toolkit — no abstraction layer overhead.

| Platform | Target Flag | UI Framework | Status |
|----------|------------|--------------|--------|
| macOS | (default) | AppKit | Tier 1 |
| iOS | `--target ios-simulator` / `--target ios` | UIKit | Tier 1 |
| visionOS | `--target visionos-simulator` | UIKit (visionOS) | Tier 2 |
| tvOS | `--target tvos-simulator` | UIKit (tvOS) | Tier 2 |
| watchOS | `--target watchos-simulator` | SwiftUI | Tier 2 |
| Android | `--target android` | JNI + Views | Tier 1 |
| HarmonyOS | `--target harmonyos` | ArkUI + NAPI | Tier 2 |
| Windows | `--target windows` | Win32 | Tier 1 |
| Linux | (default on Linux) | GTK4 | Tier 1 |
| Web/WASM | `--target web` | DOM | Tier 2 |

## macOS

AppKit-based. Full menu bar, multi-window, sheets, vibrancy, App Store distribution.

```bash
perry compile src/main.ts -o MyApp.app
```

App bundle structure auto-generated. Code signing via `perry.toml [macos]` section.

## iOS

UIKit-based. Simulator and device targets.

```bash
perry compile src/main.ts --target ios-simulator -o MyApp
# Device:
perry compile src/main.ts --target ios -o MyApp
```

Requires Xcode + Apple Developer certificate for device builds.

## Android

JNI bridge to Android Views. Builds APK directly.

```bash
perry compile src/main.ts --target android -o MyApp.apk
```

Requires Android SDK + NDK. Template project in `crates/perry-ui-android/template/`. Java/Kotlin interop via JNI.

Key files:
- `app/src/main/java/com/perry/app/PerryBridge.java` — pump timer, lifecycle
- `app/src/main/java/com/perry/app/MainActivity.java` — activity host
- `app/build.gradle.kts` — Android build config

## HarmonyOS

ArkUI harvest model — TypeScript widget tree destructively rewritten to ArkUI source code.

```bash
perry compile src/main.ts --target harmonyos
```

Architecture: HIR → harvest → `Index.ets` + `libentry.so`. Uses NAPI drain queues for callbacks, toasts, state updates. DevEco Studio for HAP packaging.

Setup: `perry setup harmonyos` (configures SDK path, signing keys).

## Windows

Win32 API (HWND, WNDPROC). Native look and feel.

```bash
perry compile src/main.ts -o MyApp.exe
```

Win7+ compatibility via `--min-windows-version=7|8|10` (default: 10).

## Linux (GTK4)

GTK4 widgets via Rust bindings. Requires `libgtk-4-dev`.

```bash
perry compile src/main.ts -o myapp
```

Package dependencies: `libgtk-4-dev`, `libgstreamer1.0-dev` (for media), `libpango1.0-dev`.

## Web/WASM

Compiles to WASM + JS runtime. DOM-based UI.

```bash
perry compile src/main.ts --target web -o dist/
```

Output: `.wasm` binary + `wasm_runtime.js` wrapper. Browser-native widgets via DOM manipulation.

## Build Commands Summary

```bash
# Host platform (auto-detected)
perry compile src/main.ts -o output

# Cross-compile
perry compile src/main.ts --target ios-simulator -o app
perry compile src/main.ts --target android -o app.apk
perry compile src/main.ts --target harmonyos
perry compile src/main.ts --target web -o dist/

# Run directly
perry run src/main.ts

# Development mode (watch + rebuild)
perry dev src/main.ts
```
