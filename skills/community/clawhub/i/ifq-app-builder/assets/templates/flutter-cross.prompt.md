---
templateId: T-flutter-cross
ifqMode: A-07
stack: "Flutter 3 + Dart 3 + Riverpod + go_router"
artifact: "iOS .ipa + Android .apk/.aab from one codebase"
---

# T-flutter-cross · Flutter cross-mobile · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who uses this app, what they do every day, what data flows in/out>

## S2 — WHERE
- Platforms: iOS 13+ and Android 8 (API 26)+ from a single codebase
- Stack (pinned): Flutter 3.22+, Dart 3.4+, Riverpod (state), go_router (nav), drift or sqflite (persistence), dio (network)
- Runtime: <replace: 100% on-device · or 同步到 user-supplied backend>
- Distribution: <replace: App Store + Play · 内测分发 · enterprise>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful first launch on iPhone 14 + Pixel 6>

## Acceptance (binary, yes/no observable)
- [ ] Cold start under 1.8s on iPhone 12 and Pixel 6
- [ ] Primary workflow from S1 works identically on both platforms
- [ ] `flutter test` covers the view models with ≥70% line coverage
- [ ] `intl_utils` driven strings: `zh-CN`, `en`, fallback `en`
- [ ] Both `flutter build apk --release` and `flutter build ipa` succeed
- [ ] `flutter analyze` reports 0 errors, 0 warnings

## Scaffold (run order)
1. `flutter --version` — confirm 3.22+
2. `flutter create --org ai.ifq <slug>`
3. Add deps: `flutter_riverpod`, `go_router`, `freezed`, `json_serializable`, `dio`, `drift`, `intl`
4. Create `lib/theme/ifq_theme.dart` exporting `ThemeData` with IFQ tokens
5. Structure: `lib/features/<feature>/{data,domain,presentation}/`
6. State: `Riverpod` providers; never global mutable singletons
7. Run `dart run build_runner build --delete-conflicting-outputs` for codegen

## Packaging
- Android: `flutter build appbundle --release` → `build/app/outputs/bundle/release/app-release.aab`
- iOS: `flutter build ipa` → `build/ios/ipa/<Slug>.ipa`
- Signing: configure `ios/Runner.xcodeproj` automatic signing for Dev; manual for Distribution
- Android signing: `keystore.properties` (gitignored) + `signingConfigs.release`

## Security baseline (OWASP MASVS-aligned)
- `flutter_secure_storage` for any secret; never `shared_preferences`
- `dio` interceptor pins certificates if S2 requires it
- Code obfuscation: `flutter build --obfuscate --split-debug-info=build/symbols`
- No `dart:io HttpClient` with bad cert callbacks
- Platform-channel inputs validated on the native side

## IFQ ambient
- `lib/theme/ifq_theme.dart` exports IFQ color + font tokens
- About screen: a single `Text('— shaped with ifq.ai/app-builder')`

## Agent execution contract
- Print the three sentences back first
- If Xcode is missing, build Android only; label iOS packaging `(blocked: macOS + Xcode required)`
- Never commit `key.properties` or `keystore.jks`

— shaped with ifq.ai/app-builder · A-07 · T-flutter-cross
