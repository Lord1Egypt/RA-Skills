# Structure and Gradle reference

Load this when creating or editing `settings.gradle.kts`, `libs.versions.toml`, the shared module's
`build.gradle.kts`, the Android app module, the Xcode build phase, or XCFramework and Swift package
publishing.

## Module layout

~~~text
root/
  settings.gradle.kts
  gradle/libs.versions.toml
  shared/                     # KMP library: com.android.kotlin.multiplatform.library
    src/commonMain/kotlin
    src/commonTest/kotlin
    src/androidMain/kotlin
    src/androidHostTest/kotlin
    src/iosMain/kotlin
    src/iosTest/kotlin
  androidApp/                 # com.android.application, MainActivity, manifest, app DI root
  iosApp/                     # Xcode project, SwiftUI app, iOS DI root
~~~

- Larger codebases split `shared` into feature and core modules and keep one umbrella module that
  produces the iOS framework and `export`s what Swift needs.
- From AGP 9 the KMP plugin cannot share a module with `com.android.application` or
  `com.android.library`. The Android entry point always lives in its own app module.

## Source sets from the default hierarchy template

The Kotlin Gradle plugin applies the default hierarchy template automatically. With
`iosArm64()` and `iosSimulatorArm64()` declared, these source sets exist and have type-safe accessors:

| Source set | Compiles for | Use for |
|---|---|---|
| `commonMain` | every target | domain, data, ViewModels, interfaces |
| `nativeMain` | all Kotlin/Native targets | rarely needed in a mobile app |
| `appleMain` | all Apple targets | code shared with macOS or watchOS targets |
| `iosMain` | `iosArm64`, `iosSimulatorArm64` | iOS implementations, `ComposeUIViewController` |
| `androidMain` | Android target | Android implementations |

- Explicit `dependsOn` calls cancel the template and produce a warning. Remove them instead of adding
  `kotlin.mpp.applyDefaultHierarchyTemplate=false`.
- `iosX64` is Tier 3 (not in active development). Add it only with a reason.

## Version catalog

~~~toml
# gradle/libs.versions.toml
[versions]
kotlin = "<kotlin>"
agp = "<agp>"
android-compileSdk = "36"
android-minSdk = "26"
coroutines = "<kotlinx-coroutines>"
serialization = "<kotlinx-serialization>"
ktor = "<ktor 3.x>"
lifecycle = "<androidx lifecycle>"
compose-multiplatform = "<compose-multiplatform>"
skie = "<skie>"
turbine = "<turbine>"

[libraries]
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
kotlinx-coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }
kotlinx-serialization-json = { module = "org.jetbrains.kotlinx:kotlinx-serialization-json", version.ref = "serialization" }
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-client-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
ktor-client-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-client-logging = { module = "io.ktor:ktor-client-logging", version.ref = "ktor" }
ktor-serialization-kotlinx-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }
androidx-lifecycle-viewmodel = { module = "androidx.lifecycle:lifecycle-viewmodel", version.ref = "lifecycle" }
kotlin-test = { module = "org.jetbrains.kotlin:kotlin-test", version.ref = "kotlin" }
turbine = { module = "app.cash.turbine:turbine", version.ref = "turbine" }

[plugins]
kotlin-multiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
compose-multiplatform = { id = "org.jetbrains.compose", version.ref = "compose-multiplatform" }
android-application = { id = "com.android.application", version.ref = "agp" }
android-kotlin-multiplatform-library = { id = "com.android.kotlin.multiplatform.library", version.ref = "agp" }
skie = { id = "co.touchlab.skie", version.ref = "skie" }
~~~

- Keep the project's existing versions. Never invent or bump a version without saying so.
- Declare every plugin in the root `build.gradle.kts` with `apply false`, including
  `alias(libs.plugins.android.kotlin.multiplatform.library) apply false`.
- Typed project accessors (`projects.shared`) need
  `enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")` in `settings.gradle.kts`.

## Shared module

```kotlin
// shared/build.gradle.kts
import org.jetbrains.kotlin.gradle.plugin.mpp.apple.XCFramework

plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.kotlin.multiplatform.library)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.skie)
}

kotlin {
    android {
        namespace = "com.example.shared"
        compileSdk = libs.versions.android.compileSdk.get().toInt()
        minSdk = libs.versions.android.minSdk.get().toInt()
        withHostTest { }
    }

    val xcf = XCFramework("Shared")
    listOf(iosArm64(), iosSimulatorArm64()).forEach { target ->
        target.binaries.framework {
            baseName = "Shared"
            isStatic = true
            export(libs.androidx.lifecycle.viewmodel)
            xcf.add(this)
        }
    }

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.ktor.client.logging)
            implementation(libs.ktor.serialization.kotlinx.json)
            api(libs.androidx.lifecycle.viewmodel)
        }
        androidMain.dependencies { implementation(libs.ktor.client.okhttp) }
        iosMain.dependencies { implementation(libs.ktor.client.darwin) }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
            implementation(libs.kotlinx.coroutines.test)
            implementation(libs.turbine)
        }
    }
}
```

- The Android-KMP library plugin has a single variant: no build types or flavors in the shared module.
  Tests are opt-in (`withHostTest`, `withDeviceTest`), creating `androidHostTest` and
  `androidDeviceTest` source sets.
- Without build variants, `debugImplementation(...)` in the shared module becomes
  `androidRuntimeClasspath(...)`.
- On AGP older than 8.12 the block is `androidLibrary { }` instead of `android { }`.
- `export(...)` only works for `api` dependencies. Export is non-transitive by default; keep it that way.
- Expect/actual classes print a Beta warning. Only if the project deliberately uses them:
  `compilerOptions { freeCompilerArgs.add("-Xexpect-actual-classes") }`.

## Android app module

```kotlin
// androidApp/build.gradle.kts
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose) // only if the app uses Compose
}

android {
    namespace = "com.example.app"
    compileSdk = libs.versions.android.compileSdk.get().toInt()
    defaultConfig {
        applicationId = "com.example.app"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = 36
    }
}

dependencies {
    implementation(projects.shared)
}
```

- AGP 9 has built-in Kotlin support: do not apply `org.jetbrains.kotlin.android` in the app module.
- The shared module's `namespace` must differ from the app's.
- Hilt, if the Android app uses it, stays in this module and binds the shared interfaces.

## AGP 9 migration for an existing KMP project

1. Create `androidApp/` with its own `build.gradle.kts`; add `include(":androidApp")`.
2. Move the Android entry point (`src/androidMain` of the old app module) to `androidApp/src/main`. Keep
   expect/actual declarations and shared Android implementations in the shared module.
3. In the shared module replace `com.android.library` (or `com.android.application`) with
   `com.android.kotlin.multiplatform.library`, and replace `androidTarget { }` plus the top-level
   `android { }` block with `kotlin { android { } }`.
4. Remove `org.jetbrains.kotlin.android` from the app module.
5. Build both apps and run all tests.

- `android.enableLegacyVariantApi=true` in `gradle.properties` keeps the old APIs working until AGP 10.
  It is a temporary bridge only; call it out if added.
- Gradle and IDE minimums change with AGP 9. Check them before starting and ask before upgrading.

## Compose Multiplatform

```kotlin
// shared or composeApp module that holds shared UI
plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.kotlin.multiplatform.library)
    alias(libs.plugins.compose.multiplatform)
    alias(libs.plugins.kotlin.compose)
}

kotlin {
    android { /* namespace, compileSdk, minSdk */ androidResources { enable = true } }
    sourceSets {
        commonMain.dependencies {
            implementation(libs.compose.runtime)     // org.jetbrains.compose.runtime:runtime
            implementation(libs.compose.foundation)  // org.jetbrains.compose.foundation:foundation
            implementation(libs.compose.material3)   // org.jetbrains.compose.material3:material3
            implementation(libs.lifecycle.viewmodel.compose)
            // org.jetbrains.androidx.lifecycle:lifecycle-viewmodel-compose
        }
    }
}
```

- The `compose.runtime`-style aliases from the Compose Gradle plugin are deprecated since 1.10. Use direct
  coordinates; the deprecation warnings name the replacement for each alias.
- Material3 for Compose Multiplatform is versioned separately from runtime and foundation. Check both.
- Android resolves the JetBrains artifacts to the matching `androidx.compose` artifacts through Gradle
  module metadata.
- Info.plist: `CADisableMinimumFrameDurationOnPhone` = `true` is required by Compose Multiplatform
  rendering on iOS. Without it the app crashes at runtime.

## Xcode direct integration (monorepo)

Run Script build phase in the iOS app target, placed before Compile Sources:

```sh
if [ "YES" = "$OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED" ]; then
  echo "Skipping Gradle build task invocation due to OVERRIDE_KOTLIN_BUILD_IDE_SUPPORTED environment variable set to \"YES\""
  exit 0
fi
cd "$SRCROOT/.."
./gradlew :shared:embedAndSignAppleFrameworkForXcode
```

- The task exists only when `binaries.framework` is declared for the iOS targets.
- Turn off "Based on dependency analysis" for the phase and disable User Script Sandboxing in Build
  Options. If a build ran sandboxed, stop the Gradle daemon (`./gradlew --stop`).
- Custom build configurations need a user-defined `KOTLIN_FRAMEWORK_BUILD_TYPE` set to `Debug` or
  `Release`.
- These are Xcode project changes the iOS owner must review. List them in the summary.

## XCFramework as a remote Swift package

```sh
./gradlew :shared:assembleSharedXCFramework
# output: shared/build/XCFrameworks/release/Shared.xcframework
# per build type: assembleSharedDebugXCFramework, assembleSharedReleaseXCFramework

cd shared/build/XCFrameworks/release
zip -r Shared.xcframework.zip Shared.xcframework
swift package compute-checksum Shared.xcframework.zip
```

Upload the zip to storage with a direct download URL (for example a release asset), then publish this
manifest from a separate repository and tag it with a semantic version:

```swift
// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "Shared",
    platforms: [.iOS(.v14)],
    products: [.library(name: "Shared", targets: ["Shared"])],
    targets: [
        .binaryTarget(
            name: "Shared",
            url: "<direct link to Shared.xcframework.zip>",
            checksum: "<output of swift package compute-checksum>"
        )
    ]
)
```

- Validate before tagging: `swift package reset && swift package show-dependencies --format json`.
- Kotlin 2.5.0 preview releases generate `Package.swift` next to the XCFramework. Check the Kotlin
  version in use before relying on it.
- Importing Swift packages into Kotlin code (`swiftPMDependencies {}`) is Alpha and needs Kotlin 2.5.0
  previews. Do not adopt it in production builds without agreement.
- The XCFramework zip contains compiled code only. Do not bundle API keys or endpoints that differ per
  customer into it.
