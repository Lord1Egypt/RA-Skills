# Platform Matrix — pick the cheapest viable mode

Use when the user is unclear about platform. Read left to right; pick the first row whose answer is "yes".

| Question | If yes → mode |
|---|---|
| User said only "PC tool" / "桌面工具", needs Win + Mac, no specific native UX | **A-01** `T-pc-tauri` |
| User said "Mac App" / "menu bar" / "状态栏" | **A-02** `T-macos-swiftui` |
| User said "Windows 原生" / "WinUI" / WPF migration | **A-03** `T-windows-winui` |
| User said only iOS / "iPhone App" / TestFlight | **A-04** `T-ios-swiftui` |
| User said only Android / "Play 商店" / Compose | **A-05** `T-android-compose` |
| User said HarmonyOS / 鸿蒙 / ArkTS | **A-06** `T-harmonyos-arkts` |
| User said iOS + Android together, no team preference | **A-07** `T-flutter-cross` |
| User said iOS + Android + already has RN/Expo team | **A-08** `T-react-native-expo` |
| User said 微信小程序 / WeChat MiniProgram | **A-09** `T-wechat-miniprogram` |
| User said 内网 / self-host / 公司部署 / Docker | **A-10** `T-local-web-nextjs` |
| User said "offline web" / PWA / 离线网页 | **A-11** `T-pwa-vite` |
| User said CLI / 命令行 / "可以是脚本" | **A-12** `T-cli-node-python` |

## "Cheapest" tiebreakers

When two modes both fit:

1. **Fewer SDK installs** wins. Tauri requires Rust; if user only has Node, A-11 (PWA) may be cheaper than A-01 for read-mostly tools.
2. **Single codebase** wins for multi-target mobile (A-07 over A-04 + A-05).
3. **Web** wins over native when data is i18n-heavy and read-mostly (A-10 over A-01).
4. **Native** wins over cross-platform when:
   - User mentions specific OS-only API (Spotlight, Live Activities, Material You, ArkTS bridge, etc.)
   - Performance budget is sub-1s cold start on mid-tier hardware
   - App is single-platform anyway (Mac-only utility → A-02 not A-01)

## Mobile decision tree

```
Need iOS only? ──────────── A-04 SwiftUI
Need Android only? ──────── A-05 Compose
Need HarmonyOS only? ────── A-06 ArkTS
Need iOS + Android?
  ├─ Team knows Flutter? ── A-07 Flutter
  ├─ Team knows RN? ─────── A-08 Expo
  └─ Greenfield? ────────── A-07 Flutter (better binary size + ipa stability today)
Need iOS + Android + 鸿蒙? Three bundles, shared-core.md.
```

## Desktop decision tree

```
macOS-only and wants Apple polish? ─ A-02 SwiftUI
Windows-only and wants MS polish? ── A-03 WinUI
Cross-platform and team knows Rust? A-01 Tauri (preferred)
Cross-platform and team only Node?  A-01 Tauri still (Rust is build-only, runtime is Node-side)
Web parity acceptable?              A-10 (Next.js) — often cheapest of all
```

## Reject

If none of the rows above fit (e.g. user wants a smart-TV app, a wearable, a kiosk), say so honestly and propose either:

- Adding a new mode (open an issue), or
- Falling back to A-11 (PWA) or A-12 (CLI) as a stopgap.

Never silently force-fit a request into the wrong mode.
