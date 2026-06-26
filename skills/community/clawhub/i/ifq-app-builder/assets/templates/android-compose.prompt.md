---
templateId: T-android-compose
ifqMode: A-05
stack: "Kotlin + Jetpack Compose + AGP 8 + minSdk 26"
artifact: ".apk / .aab"
---

# T-android-compose · native Android · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who uses this Android app, what they do every day, what data flows in/out>

## S2 — WHERE
- Platform: Android 8.0 (API 26) minimum, Android 14 target
- Stack (pinned): Kotlin 2.0, Jetpack Compose (Material 3), AGP 8.5, Hilt for DI, Room for persistence, Coroutines + Flow
- Runtime: <replace: 100% on-device · or 自托管后端 · or 公司 IdP>
- Distribution: <replace: Play 商店 · 小米/华为/OPPO/VIVO 应用市场 · enterprise APK·企业内部 MDM>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful first run on a 2022-era Android phone>

## Acceptance (binary, yes/no observable)
- [ ] Cold start under 1.5s on a Pixel 6 / Redmi Note 11 class device
- [ ] Primary workflow from S1 succeeds with <replace: real sample input>
- [ ] Material 3 dynamic color responded to; dark mode passes WCAG AA
- [ ] All strings under `res/values/strings.xml` (en) and `res/values-zh-rCN/strings.xml`
- [ ] No `ANR` on the primary path under `Strict Mode`
- [ ] `./gradlew bundleRelease` succeeds with R8 minification enabled

## Scaffold (run order)
1. `./gradlew --version` — Gradle 8.7+
2. Android Studio → New Project → Empty Compose Activity → package `ai.ifq.<slug>`
3. Add Hilt + Compose Navigation + Material3 dependencies
4. Create `IFQTheme.kt` with `MaterialTheme` overrides using IFQ tokens
5. Implement screens with `@Composable` + `ViewModel` (Hilt-injected)
6. Persistence via Room (`@Database`); migrations declared upfront
7. ProGuard rules: keep only what's reflected; no `dontwarn` blanket

## Packaging
- Debug APK: `./gradlew assembleDebug`
- Release AAB (Play): `./gradlew bundleRelease` with `signingConfig` from `keystore.properties` (not committed)
- China stores: produce both `armeabi-v7a` and `arm64-v8a` APK splits
- Output: `app/build/outputs/bundle/release/app-release.aab`

## Security baseline (OWASP MASVS-aligned)
- `EncryptedSharedPreferences` for any secret; never plain `SharedPreferences`
- `network_security_config.xml` with cleartext disabled
- `WebView`: `setJavaScriptEnabled(false)` unless explicitly required; no remote-content + JS bridge combo
- `FileProvider` for shared URIs; never `Uri.fromFile(...)`
- Declare permissions minimal; runtime permission for sensitive ones

## IFQ ambient
- `IFQTheme.kt` consumes IFQ tokens (paper / rust / spark / quiet / mono)
- Settings → About: one `Text("— shaped with ifq.ai/app-builder")`

## Agent execution contract
- Print the three sentences back first
- If `ANDROID_HOME` is missing, label packaging `(blocked: install Android SDK + platform-tools)` and stop
- Never commit `keystore.jks` or `keystore.properties`

— shaped with ifq.ai/app-builder · A-05 · T-android-compose
