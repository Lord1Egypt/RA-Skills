# CLI Reference & Configuration

## Table of Contents

- [Commands](#commands)
- [Global Flags](#global-flags)
- [Compilation Targets](#compilation-targets)
- [perry.toml Configuration](#perrytoml-configuration)
- [Environment Variables](#environment-variables)

## Commands

### `perry compile <file> [flags]`

Compile TypeScript to native executable.

```bash
perry compile src/main.ts -o MyApp                    # Host platform
perry compile src/main.ts --target ios-simulator -o app
perry compile src/main.ts --target android -o app.apk
perry compile src/main.ts --target harmonyos           # HAP output
perry compile src/main.ts --target web -o dist/        # WASM output
perry compile src/main.ts --print-hir                  # Debug: print HIR
perry compile src/main.ts --minify                     # Strip debug info
perry compile src/main.ts --no-cache                   # Force full rebuild
```

Key flags:
- `-o, --output <path>` — Output path
- `--target <target>` — Cross-compilation target
- `--print-hir` — Print HIR for debugging
- `--minify` — Strip debug symbols
- `--no-cache` — Disable incremental build cache
- `--optimize <level>` — Optimization level (0-3, default: 3)
- `--min-windows-version <7|8|10>` — Windows compatibility (default: 10)
- HarmonyOS signing flags: `--p12-keystore`, `--p12-password`, `--harmonyos-cert`, `--harmonyos-profile`, `--harmonyos-key-alias`

### `perry run <file>`

Compile and run in one step.

```bash
perry run src/main.ts
```

### `perry dev <file>`

Development mode with watch + rebuild on file changes.

```bash
perry dev src/main.ts
```

### `perry check <file>`

Type-check TypeScript source without compiling.

```bash
perry check src/main.ts
```

### `perry init <name>`

Initialize a new Perry project with boilerplate.

```bash
perry init my-app
```

### `perry doctor`

Diagnose toolchain issues. Checks: compiler, runtime libraries, platform SDKs, native toolchains.

```bash
perry doctor
```

### `perry explain <topic>`

Explain compiler concepts, errors, or optimizations.

```bash
perry explain nan-boxing
perry explain gc
```

### `perry publish`

Package and publish for distribution.

```bash
perry publish
```

### `perry setup <platform>`

Configure platform-specific SDK paths and signing keys.

```bash
perry setup harmonyos    # Configure OHOS SDK + signing
perry setup android      # Configure Android SDK/NDK
```

### `perry update`

Check for and install Perry updates.

```bash
perry update
```

### `perry i18n extract`

Extract translatable strings from source.

```bash
perry i18n extract
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--verbose` | Detailed logging |
| `--quiet` | Suppress non-error output |
| `--version` | Print version |
| `--help` | Show help |

## Compilation Targets

| Target Flag | Platform | Output Format |
|------------|----------|---------------|
| (default) | macOS | `.app` bundle |
| `--target ios-simulator` | iOS Simulator | Binary |
| `--target ios` | iOS Device | Binary |
| `--target visionos-simulator` | visionOS | Binary |
| `--target tvos-simulator` | tvOS | Binary |
| `--target watchos-simulator` | watchOS | Binary |
| `--target android` | Android | `.apk` |
| `--target harmonyos` | HarmonyOS | HAP (via DevEco) |
| `--target harmonyos-simulator` | HarmonyOS Sim | HAP |
| `--target windows` | Windows | `.exe` |
| (default on Linux) | Linux (GTK4) | Binary |
| `--target web` | Web/WASM | `.wasm` + JS |

## perry.toml Configuration

### [project]

```toml
[project]
name = "my-app"
version = "1.0.0"
entry = "src/main.ts"          # Entry file (default: src/main.ts)
```

### [app]

```toml
[app]
id = "com.example.myapp"       # Bundle identifier
name = "My App"                # Display name
version = "1.0.0"              # App version
build = 1                      # Build number (auto-incremented)
```

### [build]

```toml
[build]
optimize = 3                   # Optimization level 0-3
minify = false                 # Strip debug symbols
sourcemap = false              # Generate source maps
```

### [macos]

```toml
[macos]
category = "public.app-category.utilities"
minimum_version = "13.0"       # macOS deployment target
signing_identity = "Developer ID Application: ..."
entitlements = "path/to/entitlements.plist"
```

### [ios]

```toml
[ios]
team_id = "XXXXXXXXXX"
bundle_id = "com.example.myapp"
minimum_version = "16.0"
device_family = "universal"     # "iphone", "ipad", "universal"
```

### [visionos]

```toml
[visionos]
team_id = "XXXXXXXXXX"
bundle_id = "com.example.myapp"
```

### [android]

```toml
[android]
package_name = "com.example.myapp"
min_sdk = 24
target_sdk = 34
keystore = "path/to/keystore"
keystore_password = "@keychain/android-keystore"  # Keychain reference
key_alias = "release"
```

### [linux]

```toml
[linux]
category = "Utility"
```

### [i18n]

```toml
[i18n]
locales = ["en", "zh-Hans", "ja", "ko", "ar", "de", "fr"]
default_locale = "en"
dynamic = false                # true = runtime load; false = compile-time embed
currencies = ["USD", "EUR", "CNY"]
```

### [publish]

```toml
[publish]
channel = "stable"
manifest_url = "https://updates.example.com/manifest.json"
signing_key = "@perry/updater/signing-key"  # Keychain reference
```

### [audit]

```toml
[audit]
allowed_modules = ["perry/*", "node:*"]    # Module allowlist
blocked_modules = ["fs", "child_process"]  # Blocked modules
```

### [verify]

```toml
[verify]
strict_types = true            # Enforce strict type checking
```

### Configuration Priority

1. CLI flags (highest)
2. `perry.toml` in project root
3. Environment variables
4. `~/.perry/config.toml` (global config)
5. Defaults (lowest)

### Bundle ID Resolution

1. `perry.toml [app] id`
2. `perry.toml [ios] bundle_id` / `[android] package_name`
3. Directory name fallback

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PERRY_RUNTIME_DIR` | Override runtime library search path |
| `PERRY_LIB_DIR` | Override library directory |
| `PERRY_GEN_GC` | GC mode: `"0"`/`"off"`/`"false"` = full mark-sweep |
| `PERRY_GEN_GC_EVACUATE` | `"1"` = enable copying evacuation pass |
| `PERRY_GC_DIAG` | `"1"` = print per-cycle GC diagnostics |
| `PERRY_WRITE_BARRIERS` | `"1"` = enable codegen-emitted write barriers |
| `PERRY_HARMONYOS_P12` | Path to `.p12` keystore (HarmonyOS signing) |
| `PERRY_HARMONYOS_CERT` | Path to cert file (HarmonyOS signing) |

## Global Config (~/.perry/config.toml)

Populated by `perry setup` wizard. Stores SDK paths, signing keys, and default settings.

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Build
  run: |
    perry compile src/main.ts --target ${{ matrix.target }} -o output
    perry doctor  # Verify toolchain
```
