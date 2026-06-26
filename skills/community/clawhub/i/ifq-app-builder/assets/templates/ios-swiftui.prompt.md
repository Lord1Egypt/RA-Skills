---
templateId: T-ios-swiftui
ifqMode: A-04
stack: "SwiftUI + iOS 17 + Swift Package Manager"
artifact: ".ipa (Dev / Ad-hoc / App Store)"
---

# T-ios-swiftui · native iOS · ifq-app-builder

Fork as `<slug>.prompt.md`, fill, verify, hand to the coding agent.

## S1 — WHO + WHAT
<replace: who uses this iPhone app, what they do every day, what data flows in/out>

## S2 — WHERE
- Platform: iOS 17+ (iPhone primary, iPad if S1 implies it)
- Stack (pinned): Swift 5.9, SwiftUI, Observable macro, SwiftData (if persistence needed), Xcode 15
- Runtime: <replace: 100% on-device · or 同步到 iCloud · or 自托管后端>
- Distribution: <replace: TestFlight · App Store · Ad-hoc · Enterprise>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a happy-path first launch on an iPhone 14>

## Acceptance (binary, yes/no observable)
- [ ] Cold start under 1.2s on iPhone 12
- [ ] Primary workflow from S1 succeeds with <replace: real sample input>
- [ ] Light + dark mode both pass WCAG AA contrast on every screen
- [ ] All strings localized (`zh-Hans` + `en`) via `String Catalog` (xcstrings)
- [ ] All persistence respects `Data Protection: NSFileProtectionComplete`
- [ ] App passes basic Apple review heuristics (no private API, no placeholder copy)

## Scaffold (run order)
1. `xcodebuild -version` — Xcode 15+
2. New Project → iOS App → SwiftUI → name `<Slug>` → bundle id `ai.ifq.<slug>`
3. Add `IFQTheme.swift` (Color + Font tokens)
4. Implement view models with `@Observable`; views with `@Bindable`
5. Persistence: `SwiftData` `@Model` types (preferred) or `CoreData` legacy
6. Add `String Catalog` (`.xcstrings`) with `zh-Hans`, `en`
7. Add Privacy Manifest (`PrivacyInfo.xcprivacy`) declaring every accessed API

## Packaging
- Archive: Xcode → Product → Archive
- TestFlight: upload via Xcode or Transporter
- App Store: submit via App Store Connect; ensure Privacy Manifest & required reasons present

## Security baseline (OWASP MASVS-aligned)
- Keychain for credentials and tokens, never `UserDefaults`
- HTTPS-only via ATS (no exceptions)
- Sensitive files marked `NSFileProtectionComplete`
- No JavaScriptCore `eval` of remote strings
- Universal Links validated against `apple-app-site-association`

## IFQ ambient
- `IFQTheme.swift` (Color.ifqPaper, .ifqRust, .ifqSpark, .ifqQuiet, Font.ifqMono)
- Settings → About: a single SwiftUI `Text("— shaped with ifq.ai/app-builder")` line
- App icon may carry IFQ mark only if app is IFQ-owned

## Agent execution contract
- Print the three sentences back before opening Xcode
- If no Apple Developer team is configured: build for the simulator only, label packaging `(blocked: need Apple Developer account)`
- Use Xcode automatic signing for Dev; manual signing for Distribution

— shaped with ifq.ai/app-builder · A-04 · T-ios-swiftui
