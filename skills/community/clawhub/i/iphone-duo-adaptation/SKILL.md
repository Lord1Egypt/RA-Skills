---
name: iphone-duo-adaptation
description: Audit, implement, or verify iPhone Duo adaptation in iOS apps using SwiftUI, UIKit, or mixed UI. Use for inner/outer display continuity, folding and resizing, side bars, reserved regions, Device Hub, and localization or accessibility regressions specific to these layouts. 支持 iPhone Duo 内外屏、折叠及多语言适配。iPhone Duo の内外ディスプレイと折りたたみ対応を支援。
---

# iPhone Duo adaptation

Use the user's requested language for findings, plans, and test reports. Otherwise use the language of their request. Read one handbook by default, using English as a reference for requests in other languages. Keep Apple API names and repository identifiers unchanged.

| Language | Handbook |
| --- | --- |
| 简体中文 | [开发与验收手册](references/guide.zh-Hans.md) |
| English | [Engineering and QA handbook](references/guide.en.md) |
| 日本語 | [開発・検証ガイド](references/guide.ja.md) |

## Workflow

1. **Establish scope.** Identify affected targets, entry points, UI frameworks, deployment target, selected build SDK, and existing localization system. Choose audit, implementation, or verification from the user's request. When no app is supplied, provide a project-ready plan and mark runtime evidence as pending.
2. **Reproduce and trace.** Walk a representative flow from outer display to inner display and back. Exercise folding or resizing while a detail, sheet, or keyboard is open. Record runtime, orientation, window placement, language, and text size. Use [code-review searches](references/engineering.md) to find candidate sites and trace each match to a user-visible failure. Repo inspection can proceed when Device Hub is unavailable.
3. **Fix the owning layer.** Size UI from actual container geometry and traits. Prefer adaptive system navigation and bars. Keep selection, drafts, and long-lived work in a stable owner above layout branches. Use safe areas for foreground content and query active reserved regions for custom elements that may cross the fold or camera. Use availability checks and keep the existing deployment target unless the user requests a change.
4. **Verify the normal entry point.** Build the affected scheme with the appropriate SDK. Use the handbook matrix to cover pose transitions, both Split View placements when applicable, compact and regular widths, an ordinary iPhone on the supported baseline, and high-risk locale and accessibility combinations. Confirm release requirements only for release work. Use [the shared examples and test commands](references/engineering.md) as starting points.
5. **Report evidence.** For each issue give severity, flow, observed or inferred effect, file and line if available, fix, and verification. List build and runtime results separately. Mark cases as passed, failed, unrun, or not applicable with a reason. Claim real-device behavior only with real-device evidence.

On iPhone Duo, building with iOS 27.1 SDK or later enables the full-display presentation and adaptive system bars. This build SDK choice is separate from the app's minimum supported iOS version. Some iOS 27.1-specific APIs require runtime guards with older deployment targets. Verify toolchain and App Store requirements against [Apple sources](references/sources.md).
