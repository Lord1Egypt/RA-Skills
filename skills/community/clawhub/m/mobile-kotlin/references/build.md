# Build and tooling reference

Load this when editing `build.gradle.kts`, `settings.gradle.kts`, `libs.versions.toml`, R8 rules, or lint
configuration.

## Version catalog

~~~toml
# gradle/libs.versions.toml
[versions]
kotlin = "<kotlin>"
ksp = "<ksp>"
agp = "<agp>"
hilt = "<hilt>"
room = "<room>"
compose-bom = "<bom>"

[libraries]
compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
compose-material3 = { group = "androidx.compose.material3", name = "material3" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
room = { id = "androidx.room", version.ref = "room" }
~~~

- Use the project's existing versions. Do not invent or bump versions without saying so.
- Compose libraries take their version from the BOM: `implementation(platform(libs.compose.bom))`.
- The Compose compiler plugin and the serialization plugin are versioned with Kotlin. Since Kotlin 2.0 there is
  no separate `kotlinCompilerExtensionVersion` to manage.
- Check KSP compatibility with the Kotlin version whenever either one is upgraded.

## Module build file

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
    alias(libs.plugins.room)
}

android {
    namespace = "com.example.app"
    compileSdk = 36
    defaultConfig {
        minSdk = 26
        targetSdk = 36
    }
    buildFeatures { compose = true }
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}

kotlin {
    jvmToolchain(17)
}

room {
    schemaDirectory("$projectDir/schemas")
}

dependencies {
    implementation(platform(libs.compose.bom))
    implementation(libs.compose.material3)
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.room.runtime)
    implementation(libs.room.ktx)
    ksp(libs.room.compiler)
}
```

- SDK numbers above are an example. Never change the project's `compileSdk`, `targetSdk` or `minSdk`
  without asking; a `targetSdk` bump opts into behavior changes (see [Platform changes](platform.md)).
- Compiler options go in `kotlin { compilerOptions { } }`. `kotlinOptions {}` is deprecated.
- Recent AGP versions include built-in Kotlin support, so a separate `org.jetbrains.kotlin.android` plugin may
  not be needed. Follow what the project's AGP version requires rather than adding plugins by habit.
- Shared configuration across many modules belongs in convention plugins (`build-logic`), not copied blocks.

## kapt to KSP

- Replace `kapt(...)` with `ksp(...)` for Room, Hilt (Dagger), Moshi codegen and other processors that ship a
  KSP implementation. Remove the kapt plugin once nothing uses it.
- KSP is faster and works with K2. kapt runs in a compatibility mode and slows every build.
- Keep any processor that has no KSP version on kapt, and say so.

## Compose compiler options

```kotlin
composeCompiler {
    reportsDestination = layout.buildDirectory.dir("compose_compiler")
    metricsDestination = layout.buildDirectory.dir("compose_compiler")
}
```

- Enable reports in a local or CI diagnostic build, not permanently in every build.
- Strong skipping is on by default; do not add flags to enable it.
- A stability configuration file (also set in `composeCompiler {}`) marks external types as stable. Use it
  only for types that really are immutable.

## R8

- `isMinifyEnabled = true` and `isShrinkResources = true` for release. Test the release build, not only debug.
- Keep rules are needed for code reached only by reflection, JNI, or class names held in strings.
  Classes referenced from the manifest and XML layouts are kept by AGP-generated rules.

```proguard
# Reflection-based JSON models (Gson and similar): keep field names
-keepclassmembers class com.example.app.data.remote.dto.** { <fields>; }

# Classes loaded by name
-keep class com.example.app.plugin.** implements com.example.app.plugin.Plugin { <init>(); }
```

- kotlinx.serialization uses generated serializers, not reflection, and its artifacts ship R8 rules for
  standard usage. Verify the release build when serializers are looked up dynamically.
- Retrofit, OkHttp, Room and Hilt ship consumer rules. Do not copy old blanket rules for them.
- `-keep class com.example.** { *; }` disables shrinking for the whole app. Never add it to fix one crash.
- `@Keep` (androidx.annotation) on a single class is acceptable for a narrow reflection case.
- Upload the mapping file (`build/outputs/mapping/release/mapping.txt`) with each release for readable
  stack traces.

## Static analysis

- detekt for code smells and complexity; ktlint (directly or through Spotless) for formatting.
- Add the Compose lint rule set for detekt or ktlint to catch missing `modifier` parameters, unstable
  parameters, and effects without keys.
- Commit a baseline when adopting on legacy code; never grow the baseline for new code.
- Run both in CI on every merge request, alongside `lint` and unit tests.
- Android Lint warnings about new API usage, missing permissions and `RECEIVER_EXPORTED` flags are real
  defects, not noise.

## Secrets and build config

- No API keys, tokens or signing passwords in `build.gradle.kts`, `BuildConfig`, `gradle.properties` in VCS,
  or `strings.xml`. Anything in the APK can be extracted.
- Signing configs read from CI secrets or a local untracked file. See `mobile-ci-cd` and
  `mobile-security`.
- `buildConfig = true` only in modules that actually read `BuildConfig`.

## Native libraries

- Apps with `.so` files (own or from dependencies) must support 16 KB memory page sizes for current Google
  Play submissions targeting Android 15+. Check with the APK Analyzer and rebuild native code with a current
  NDK.
