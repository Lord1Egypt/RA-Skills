# Packaging — per-platform reference

This is a single-page cheatsheet. Each mode's template already embeds the canonical commands; this file is for cross-referencing when the user asks "how do I ship".

## A-01 PC Tauri

| Target | Command | Output |
|---|---|---|
| macOS universal | `npm run tauri build -- --target universal-apple-darwin` | `src-tauri/target/release/bundle/dmg/<App>.dmg` |
| Windows x64 | `npm run tauri build -- --target x86_64-pc-windows-msvc` | `src-tauri/target/release/bundle/nsis/<App>-setup.exe` |
| Linux AppImage | `npm run tauri build -- --target x86_64-unknown-linux-gnu` | `src-tauri/target/release/bundle/appimage/<App>.AppImage` |

Signing: macOS via `xcrun notarytool` after build; Windows via `signtool.exe` with an EV cert if available.

## A-02 macOS SwiftUI

| Target | Command | Output |
|---|---|---|
| Developer ID `.dmg` | `xcodebuild -scheme <Scheme> archive` → Organizer → Distribute → Developer ID | `<App>.dmg` |
| Mac App Store | Archive → Distribute → Mac App Store | `.pkg` uploaded via Transporter |

Notarize: `xcrun notarytool submit <archive>.zip --apple-id <id> --team-id <team> --wait`.

## A-03 Windows WinUI

| Target | Command | Output |
|---|---|---|
| MSIX | `msbuild /restore /p:Configuration=Release /p:Platform=x64 /p:GenerateAppxPackageOnBuild=true` | `AppPackages/<App>_x64.msix` |
| `.exe` installer | optional Inno Setup script after Release build | `<App>-Setup.exe` |

Code-sign with EV cert: `signtool sign /a /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 <app.msix>`.

## A-04 iOS SwiftUI

| Target | Command | Output |
|---|---|---|
| TestFlight / App Store | Xcode → Archive → Distribute App → App Store Connect | `.ipa` uploaded |
| Ad-hoc | same, choose Ad-hoc | `.ipa` for direct install |

Privacy Manifest (`PrivacyInfo.xcprivacy`) is mandatory for App Store.

## A-05 Android Compose

| Target | Command | Output |
|---|---|---|
| Play Store (AAB) | `./gradlew bundleRelease` | `app/build/outputs/bundle/release/app-release.aab` |
| Sideload APK | `./gradlew assembleRelease` | `app/build/outputs/apk/release/app-release.apk` |
| China stores | per-store APK with split ABI | armeabi-v7a + arm64-v8a |

Signing config from `keystore.properties` (gitignored).

## A-06 HarmonyOS ArkTS

| Target | Command | Output |
|---|---|---|
| Debug HAP | `hvigorw assembleHap --mode module` | `entry/build/default/outputs/default/entry-default-signed.hap` |
| Release HAP | `hvigorw assembleHap --mode module -p product=default` with signing | signed `.hap` |
| App Gallery `.app` | App Gallery Connect packaging | submitted bundle |

## A-07 Flutter

| Target | Command | Output |
|---|---|---|
| iOS | `flutter build ipa` | `build/ios/ipa/<App>.ipa` |
| Android AAB | `flutter build appbundle --release` | `build/app/outputs/bundle/release/app-release.aab` |
| Android APK | `flutter build apk --release` | `build/app/outputs/flutter-apk/app-release.apk` |

Obfuscate: append `--obfuscate --split-debug-info=build/symbols`.

## A-08 React Native / Expo

| Target | Command | Output |
|---|---|---|
| iOS | `eas build --platform ios --profile production` | `.ipa` |
| Android | `eas build --platform android --profile production` | `.aab` |
| Web | `npx expo export --platform web` | `dist/` static |

`eas submit -p ios|android` to push to stores.

## A-09 WeChat MiniProgram

| Target | Command | Output |
|---|---|---|
| 体验版 | `miniprogram-ci preview --pp ./project --pkp <pkey> --appid <appid>` | QR code |
| 提审版本 | `miniprogram-ci upload --robot 1 --ver <semver>` | uploaded to mp.weixin.qq.com |

Manual submission for review happens in mp.weixin.qq.com.

## A-10 Local Web Next.js

| Target | Command | Output |
|---|---|---|
| Image | `docker build -t <org>/<slug>:<ver> .` | OCI image |
| Compose | `docker compose up -d` | running services |
| Backup | `docker compose exec db pg_dump -U <user> <db> > backup.sql` | SQL dump |

## A-11 PWA Vite

| Target | Command | Output |
|---|---|---|
| Static bundle | `npm run build` | `dist/` ready to upload |
| Deploy | host-specific (Pages, Netlify, Cloudflare, S3+CF) | live URL |

## A-12 CLI

| Target | Command | Output |
|---|---|---|
| npm publish | `npm publish` | tarball on registry |
| pipx wheel | `python -m build` + `pipx install dist/*.whl` | installed |
| Single binary | `npx pkg .` or `pyinstaller --onefile src/cli.py` | `<slug>-darwin-x64` etc. |
