---
templateId: T-react-native-expo
ifqMode: A-08
stack: "Expo SDK 51 + React Native + TypeScript + Expo Router"
artifact: "iOS .ipa + Android .apk via EAS Build (+ optional Web)"
---

# T-react-native-expo · Expo cross-mobile · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who uses this app, what they do, what data flows in/out>

## S2 — WHERE
- Platforms: iOS 13+, Android 8 (API 26)+, optional Web (Expo Web)
- Stack (pinned): Expo SDK 51, React Native 0.74, TypeScript 5, Expo Router (file-based), Zustand or React Query for state
- Runtime: <replace: 100% on-device · or 自托管后端 · or 公司 SSO>
- Distribution: <replace: EAS Submit → App Store + Play · 内测 EAS Update · enterprise>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful first launch>

## Acceptance (binary, yes/no observable)
- [ ] `npx expo start` boots the app in Simulator and Emulator without warnings
- [ ] Primary workflow from S1 works identically on iOS + Android
- [ ] All strings localized via `i18n-js` + JSON files (`zh-CN`, `en`)
- [ ] `eas build --platform all --profile preview` succeeds
- [ ] `expo doctor` reports 0 issues
- [ ] No `console.warn` during the happy path

## Scaffold (run order)
1. `npx create-expo-app@latest <slug> -t default`
2. `cd <slug> && npx expo install expo-router expo-localization`
3. `app/_layout.tsx` declares stacks; routes are file-based under `app/`
4. Create `theme/ifq.ts` exporting IFQ color + font tokens; consume via `ThemeContext`
5. State: Zustand store under `store/`; data fetching via React Query
6. Add `eas.json` with `development`, `preview`, `production` profiles
7. `npx expo install expo-secure-store` for any credential

## Packaging
- `eas build --platform ios --profile production` → `.ipa`
- `eas build --platform android --profile production` → `.aab`
- Web: `npx expo export --platform web` → static `dist/`
- `eas submit -p ios` / `eas submit -p android` for store upload

## Security baseline (OWASP MASVS-aligned)
- `expo-secure-store` (Keychain / Keystore) for secrets; never `AsyncStorage`
- `expo-auth-session` for OAuth (PKCE)
- No `WebView` with `originWhitelist={['*']}` + JS bridge
- HTTPS only; `Image` `cache: 'force-cache'` only for trusted hosts
- App Transport Security strict on iOS; `usesCleartextTraffic=false` on Android

## IFQ ambient
- `theme/ifq.ts` exports the IFQ color + font tokens
- Settings → About: one `<Text>— shaped with ifq.ai/app-builder</Text>`

## Agent execution contract
- Print the three sentences back first
- If user has no Expo / EAS account: build with `--local` flag; label store-submission `(blocked: need Expo account)`
- Never commit `eas.json` credentials block

— shaped with ifq.ai/app-builder · A-08 · T-react-native-expo
