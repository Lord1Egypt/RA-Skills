---
templateId: T-macos-swiftui
ifqMode: A-02
stack: "SwiftUI + AppKit bridge + Swift 5.9 + Xcode 15"
artifact: ".app / .dmg (optionally MAS)"
---

# T-macos-swiftui · native macOS · ifq-app-builder

Fork this file into the user workspace as `<slug>.prompt.md`, fill every `<replace: ...>` block, run `npm run verify:lite -- <slug>.prompt.md`, hand to the calling coding agent.

## S1 — WHO + WHAT
<replace: who uses this Mac app, what they do every day, what data goes in and out>

## S2 — WHERE
- Platform: macOS 13 Ventura+ (universal binary, Apple Silicon + Intel)
- Stack (pinned): Swift 5.9, SwiftUI, AppKit bridge for `NSStatusItem` / `NSWindow` chrome, Xcode 15
- Runtime: 100% local; sandbox: `App Sandbox` ON; entitlements minimal
- Distribution: <replace: notarized .dmg via direct download · or Mac App Store>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful launch on a fresh Mac>

## Acceptance (binary, yes/no observable)
- [ ] First launch under 1s after dock click
- [ ] Primary workflow from S1 works end-to-end with <replace: real sample input>
- [ ] Menu bar / status bar UX (if relevant) does not regress focus from other apps
- [ ] Light + dark mode both render with no contrast failures
- [ ] All strings localized via `Localizable.strings` (`zh-Hans` + `en`)
- [ ] App passes `xcrun notarytool` (when notarization is in scope)

## Scaffold (run order)
1. `xcodebuild -version` — confirm Xcode 15+
2. In Xcode: New Project → App → SwiftUI → name `<Slug>` → bundle id `ai.ifq.<slug>`
3. Add `IFQTheme.swift` exporting `Color.ifqPaper`, `Color.ifqRust`, `Color.ifqSpark`, `Color.ifqQuiet`, `Font.ifqMono`
4. Implement the workflow per S1 — use `@Observable` (Swift 5.9) for view model
5. For status-bar apps: `NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)` in `AppDelegate`
6. Add `App Sandbox` entitlement; add only the file-access / network scope S2 actually requires

## Packaging
- Archive: Xcode → Product → Archive
- `.dmg`: `xcrun notarytool submit <app.zip> --apple-id <id> --team-id <team> --wait`
- MAS: separate provisioning profile + `App Store Connect` upload via Transporter
- Output artifact name: `<Slug>-<version>-universal.dmg`

## Security baseline (OWASP-aligned)
- `App Sandbox`: ON
- Hardened Runtime: ON
- Keychain via `Security.framework` for credentials; never `UserDefaults`
- Per-URL bookmarks for user-granted folder access
- No `NSAllowsArbitraryLoads`; ATS strict

## IFQ ambient
- `IFQTheme.swift` colors + fonts (see `assets/ifq-brand/BRAND-DNA.md` → SwiftUI mapping)
- About panel: a single `Text("— shaped with ifq.ai/app-builder")` line
- App icon: only the IFQ mark if product is IFQ-owned

## Agent execution contract
- Print the three sentences back before opening Xcode
- If `xcodebuild` is missing, label `S3.packaging` as `(blocked: Xcode required)` and stop, do not auto-install Xcode
- Code-signing identity: detect via `security find-identity -v -p codesigning`; if missing, build unsigned for dev only

— shaped with ifq.ai/app-builder · A-02 · T-macos-swiftui
