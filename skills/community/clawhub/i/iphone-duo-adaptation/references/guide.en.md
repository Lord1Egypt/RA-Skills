# iPhone Duo engineering and QA handbook

[简体中文](guide.zh-Hans.md) · [日本語](guide.ja.md) · [Engineering examples](engineering.md) · [Apple references](sources.md)

## 1. Establish the project baseline

Start at the affected target and user-facing entry point. Record the project and scheme, SwiftUI and UIKit boundaries, minimum iOS version, selected Xcode and SDK, shipped languages and regions, and any iPad or Mac Catalyst support. Choose an end-to-end flow such as opening a detail, editing, saving, and returning to the list. Capture the current build and user state before upgrading the build SDK so regressions can be traced to the relevant change.

| Build SDK | Presentation on iPhone Duo |
| --- | --- |
| iOS 26 or earlier | Compatibility presentation on the outer display. The inner display shows a smaller centered window with surrounding space. |
| iOS 27.0 | The app resizes dynamically and fills most of the inner display. Space remains reserved along the status-bar edge. |
| iOS 27.1 or later | The app can extend to the display edges on both displays. Standard navigation, toolbars, and tab bars are vertical where the system selects that presentation. |

Use Xcode 27.1 or a later version with the appropriate SDK for full adaptation. Configure the build SDK and deployment target independently. Use runtime availability checks such as `#available(iOS 27.1, *)` for new APIs, and provide usable fallbacks on older iOS versions. Check platform-specific availability and toolchain issues for shared targets. [Apple preparation guide](https://developer.apple.com/iphone-duo/prepare/) · [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)

## 2. Audit existing screens

| Inspect | Fix and acceptance check |
| --- | --- |
| `UIScreen.main`, fixed device dimensions, or geometry cached at launch | Size from the current container. Use adaptive SwiftUI containers first, then `GeometryReader` or `onGeometryChange` for measured layout. In UIKit, use Auto Layout, `view.bounds`, or the actual window, and recalculate during layout. Opening and closing the device during a session should update the UI. |
| Model, `userInterfaceIdiom`, or interface orientation used to pick a layout | Use size classes for navigation structure and actual container size to determine fit. The full inner display can have regular width and can rotate regardless of declared supported orientations. Read actual traits and exercise Split View. Keep framework-specific orientation handling where needed for features such as capture. |
| Custom bottom bars, fixed right-side controls, or broad safe-area overrides | Prefer framework navigation. Apply actual safe areas and directional margins to custom foreground content. Extend backgrounds where the design calls for it. Validate each edge and both Split View placements. |
| Layout switches discard work | Inspect conditional branches, `.id(...)`, `UIHostingController` lifetime, requests started on appearance, and recreated child controllers. Keep selection, drafts, and in-flight tasks under stable model ownership and item IDs. |
| Modals, keyboards, web content, or custom rendering | Inspect sheets, popover anchors, and floating controls. Use a scroll view and the keyboard layout guide for UIKit forms. In mixed apps, check the web viewport, CSS breakpoints, and how native and web insets combine. |

Trace search hits to their callers and visible behavior. Prioritize defects in shared containers and blocked primary flows. Keep fixed dimensions or orientation logic that express an existing functional requirement. [Repository searches](engineering.md) · [Apple Tech Talk](https://developer.apple.com/videos/play/tech-talks/111461/)

## 3. Implement the adaptation

### Navigation and vertical bars

- Use SwiftUI `NavigationStack` for a single-column flow, `NavigationSplitView` for list and detail, and `TabView` for tab entry points. Add actions with `.toolbar` on the active navigation hierarchy. Check list and detail side by side at wide widths and confirm the user can return to the list at narrow widths.
- In UIKit, use `UINavigationController`, `UISplitViewController`, and `UITabBarController`. Configure the owning controller's `navigationItem` or `toolbarItems`. In a mixed app, let the container that owns the flow supply its bars.
- Use semantic placement for important actions. Provide an icon and localized title, then verify vertical, horizontal, and overflow presentation. Title-only and custom-view items can be omitted from vertical presentation. Use SDK APIs such as `axisBehavior`, `visibilityPriority`, and overflow configuration when needed. Keep Back, Close, Save, and Edit reachable.
- For custom views that need to react to vertical bars, read SwiftUI's `toolbarVerticalEdge` or UIKit's `verticalBarEdge`. Sheets can use different bar orientations depending on the display and placement. View the default behavior before tuning placement.

[Apple implementation overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)

### Fold, camera, and custom layouts

| Situation | Approach |
| --- | --- |
| List/detail, standard sheet/alert/popover, or continuous reading | Use native components and verify the result. Continuous scrolling content can extend across the fold, with primary controls visible and easy to reach. |
| Two views that rearrange with pose | Consider SwiftUI `ArrangementView` or UIKit `UIArrangementViewController` on iOS 27.1. Use split when both views should stay visible and overlay for a foreground/background relationship. Keep secondary content reachable if axis restrictions can hide it. Verify accessibility when nesting the container. |
| Custom editor, grid, floating playback controls, or edge interaction | Query `.division` and `.occlusion` in the component's geometry. The hinge is a division and camera coverage is an occlusion. Use active regions for current exclusion. Compare actual hit frames in the same coordinate space and derive the geometry on each layout pass. |
| Camera, video calls, or live capture | Verify whether the Virtual Front Camera meets capture requirements. For physical camera selection, use Apple's direction coordinator with the existing capture service. Test permissions, interruption recovery, crop, rotation, mirroring, and recording continuity. Simultaneous use of both displays is a distinct camera workflow with its own scene and availability checks. |

The inner camera region changes with camera activity. Regions can change while bounds or size classes remain the same. In a custom UIKit view, query in `updateConstraints()` so UIKit invokes it again when a tracked region changes. SwiftUI mirrors region frames in RTL by default. Use `layoutDirectionBehavior` to align coordinate handling when positioning in physical coordinates. Decorative backgrounds can extend past safe areas while interactive elements remain usable. [Adaptive layouts Tech Talk](https://developer.apple.com/videos/play/tech-talks/111463/) · [Camera Tech Talk](https://developer.apple.com/videos/play/tech-talks/111465/)

### Preserve work across display changes

1. Keep the selected item, navigation path, draft, playback position, and upload task in the appropriate view model, scene, or persistent store based on its required lifetime.
2. Share the same state and tasks across compact and wide SwiftUI layouts. In UIKit, reuse the relevant child controllers, models, and ongoing work while updating constraints as needed.
3. Repeat transitions during input, with the keyboard open, with VoiceOver active, and during an upload. Check the draft, route, focus, and task outcome. Verify a sensible fallback if an item is deleted or a request is cancelled during the transition.

## 4. Localize and verify accessibility

- Keep the project's localization system. For a project using String Catalogs, put text in the appropriate `.xcstrings` file and check the key, module, and resource bundle. Use whole sentences with interpolation, translator context, and language-specific plural variants. Format dates, units, currency, and numbers with the relevant locale.
- Let text wrap, views grow, and actions reflow. Pay special attention to the outer display and Split View. Provide localized names for icons and cover empty states, errors, permissions, and overflow actions.
- Use `leading` and `trailing`, and verify RTL reading order. Determine which icons encode reading direction. Inspect mixed-direction account names, numbers, and punctuation, and confirm the physical camera or fold aligns with custom avoidance regions.
- Exercise the largest accessibility text size and check VoiceOver order, labels, focus continuity, and control reachability. Use Accessibility Inspector or `performAccessibilityAudit` in UI tests alongside a manual pass.
- Select Double-Length and RTL pseudolanguages in the Xcode scheme to find layout defects. Then run actual supported languages with relevant App Region settings. The included examples cover English, Simplified Chinese, Japanese, German, and Arabic. Use the app's shipping language list for acceptance.

[Sample string catalog](../assets/Localizable.xcstrings) · [Apple localization guidance](https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization) · [Apple accessibility audits](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app)

## 5. Acceptance matrix

Select an iPhone Duo simulator in Xcode and open Device Hub. Use its controls to close, open, rotate, and partially fold the device. Start each case at the normal entry point. Record the build, runtime, pose, window placement, language and region, text size, and evidence. Run the combinations below first and extend them for the app's features.

| ID | Setup and action | Pass criteria |
| --- | --- | --- |
| D01 | Open the core screen on the outer display in portrait and supported landscape orientations | Primary controls are usable. Tabs and overflow are reachable. Content avoids clipping. |
| D02 | Fully open the inner display, rotate, and navigate from list to detail and back | Columns remain usable and navigation is reachable. Rotation preserves the route and avoids blank UI or duplicate requests. |
| D03 | Open, partially fold, and close while editing an unsaved draft with the keyboard visible | The same item and draft remain available. Keyboard and focus behave as designed, and saving runs once. |
| D04 | Partially fold into book and tabletop poses with a sheet, popover, alert, or custom control present | Controls remain visible and avoid active regions. Presented UI can be operated and dismissed. |
| D05 | Where Split View is supported, navigate and scroll on each side of the inner display | The bars and asymmetric safe areas work on both sides, and hit testing and scrolling work. |
| D06 | Test double-length, RTL, and maximum accessibility text on the outer display and at least one partial fold | Text, controls, overflow actions, and VoiceOver remain usable. Confirm with actual high-priority locales. |
| D07 | For camera or recording features, switch displays on physical hardware and activate/deactivate the inner camera | Capture device, preview, mirroring, occlusion, and interruption recovery behave as intended. Saving and cancellation leave consistent state. |
| D08 | Run on an ordinary iPhone with minimum supported iOS and current iOS, plus iPad or Mac Catalyst when supported | Primary flows and availability fallbacks pass on the supported platforms. |

Automate geometry calculations, navigation and input assertions, and snapshot checks where supported by the project. Exercise pose changes in Device Hub or on hardware. Review simulator limitations and record physical-device results for hardware-dependent behavior, extensions, or capture. [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)

## 6. Handoff and release

- For an audit, report severity, reproduction conditions, user impact, file and line, recommended fix, acceptance case, and evidence. Identify whether the finding was observed at runtime or inferred from code.
- For implementation, record the affected screens, build SDK, minimum iOS version, and availability paths. List build and UI test results separately with passed, failed, unrun, or not applicable. Prioritize data loss, crashes, and unreachable primary actions.
- For a release, prepare outer and inner display screenshots and localized storefront assets as applicable. Apple's current screenshot reference lists an April 2027 requirement for apps using the iOS 27.1 SDK or later. Check the live requirements for the actual submission. Upload only when authorized. [App Store Connect screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)

Evidence record

```text
Case D03 | Build and SDK | Device and iOS | Outer → inner → outer
Language and region | Text size | Entry point and steps | Expected result
Observed outcome | Passed / failed / unrun / N/A | Screenshot, recording, or log
```
