# Modes — full protocol

This file enumerates every mode the skill can route to. Routes are matched in order; the **first** entry whose triggers match the user's intent at ≥70% confidence wins. If none match, fall back per the table at the bottom.

| Mode | Trigger keywords | Template | Stack | Output artifact | Fallback when blocked |
|---|---|---|---|---|---|
| **A-01** | PC 桌面、跨平台桌面、Win + Mac、desktop tool、Tauri、Electron 替代 | `T-pc-tauri` | Tauri 2 + React + Vite | `.dmg`/`.exe`/`.AppImage` | A-02 if macOS-only and want native polish |
| **A-02** | macOS 原生、Mac App、menu bar、状态栏、AppKit、SwiftUI | `T-macos-swiftui` | SwiftUI + Swift 5.9 | `.app`/`.dmg`/MAS | A-01 if user also wants Windows |
| **A-03** | Windows 原生、WinUI、WPF、.NET、MSIX | `T-windows-winui` | WinUI 3 + .NET 8 | MSIX / `.exe` | A-01 if cross-platform desktop |
| **A-04** | iOS、iPhone、App Store、TestFlight、SwiftUI iOS | `T-ios-swiftui` | SwiftUI + iOS 17 | `.ipa` | A-07 Flutter if user also wants Android |
| **A-05** | Android、安卓、Play 商店、Jetpack Compose、Kotlin | `T-android-compose` | Kotlin + Compose | `.apk`/`.aab` | A-07 / A-08 if cross-platform mobile |
| **A-06** | 鸿蒙、HarmonyOS、ArkTS、ArkUI、华为应用市场 | `T-harmonyos-arkts` | ArkTS + ArkUI Stage | `.hap`/`.app` | — (no real cross-platform fallback) |
| **A-07** | Flutter、一份代码多端、跨端移动、Dart | `T-flutter-cross` | Flutter 3 + Riverpod | iOS + Android | A-08 if user already on RN team |
| **A-08** | React Native、Expo、RN、EAS Build | `T-react-native-expo` | Expo 51 + RN + TS | iOS + Android + Web | A-07 if user wants smaller binary / better animations |
| **A-09** | 微信小程序、WeChat MiniProgram、wx、小程序 | `T-wechat-miniprogram` | 原生 + TS + Skyline | `.wxapkg` | — |
| **A-10** | 本地部署、self-host、内网 web、Docker、私有部署 | `T-local-web-nextjs` | Next.js 15 + Docker | docker image | A-11 if no DB / no auth |
| **A-11** | PWA、离线 Web、可安装网页、Workbox | `T-pwa-vite` | Vite + Workbox | static + SW | A-10 if user needs auth + server data |
| **A-12** | CLI、命令行、脚本、终端工具、npx、pipx | `T-cli-node-python` | Node 20 or Python 3.11 | npm/pipx package | — |

## When multiple modes match

Pick the **cheapest** match for the user. "Cheapest" means:

1. Fewest required SDKs the user has to install.
2. Single codebase if user said "iOS + Android" (A-07 > A-04 + A-05).
3. Web > native when the use case is read-mostly and i18n-heavy.
4. CLI > GUI when input is files-in-files-out and user already lives in the terminal.

## When zero modes match at ≥70% confidence

| User signal | Default |
|---|---|
| "桌面"/"desktop" without specifics | A-01 Tauri |
| "手机"/"mobile" without specifics | A-07 Flutter |
| "网页"/"web" without specifics | A-10 Next.js (or A-11 if explicitly offline-first) |
| "工具"/"tool" without GUI cues | A-12 CLI |
| "做一个 app" 完全没限定 | Ask **one** question: "PC、手机，还是网页 / 小程序？" — never more than one |

## Multi-platform requests

If S2 names more than one platform, emit **one bundle per platform** plus a shared `shared-core.md` describing data model + business rules. Each bundle's S2 references the shared file by relative path.

## Mode metadata is canonical in `assets/templates/INDEX.json`

That file is policy-validated by `scripts/validate-templates.mjs`. This file is for humans; `INDEX.json` is for agents.
