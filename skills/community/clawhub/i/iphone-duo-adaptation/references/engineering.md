# Shared engineering examples · 工程示例 · 実装サンプル

[简体中文](guide.zh-Hans.md) · [English](guide.en.md) · [日本語](guide.ja.md)

## Repository review · 工程扫描 · リポジトリ調査

Run these read-only searches at the app repository root. Confirm target membership and inspect callers. Hits can be legitimate, such as orientation in a capture pipeline or fixed sizes for decorative icons. Review ignored or generated files only when they contribute to the affected target. Mixed apps should also scan their own HTML, CSS, JS, or cross-platform UI sources for viewport-size assumptions.

```sh
rg --files -g 'project.pbxproj' -g '*.xcconfig' -g '*.xcscheme' -g '*.xcworkspace/contents.xcworkspacedata' -g 'Info.plist' -g '*.xcstrings' -g '*.strings' -g '*.stringsdict' -g '*.storyboard' -g '*.xib'

rg -n -g '*.{swift,m,mm,h,plist,pbxproj,xcconfig}' 'UIScreen\.main|\[UIScreen mainScreen\]|mainScreen\]|userInterfaceIdiom|UIDevice\.current\.orientation|statusBarOrientation|interfaceOrientation|supportedInterfaceOrientations|UISupportedInterfaceOrientations|IPHONEOS_DEPLOYMENT_TARGET' .

rg -n -g '*.{swift,m,mm,storyboard,xib}' 'ignoresSafeArea|safeAreaInsets|additionalSafeAreaInsets|layoutMargins|contentInset|frame\((width|height):|\.leftAnchor|\.rightAnchor|leftAnchor\]|rightAnchor\]|ToolbarItem|UINavigationBar|UITabBar|preferredContentSize|UIHostingController|\.id\(' .
```

Apple's App Resizability skill is available from Xcode. Apple also documents `xcrun agent skills export` for other coding agents. Treat its findings as candidates and review live flows. [Apple's preparation guide](https://developer.apple.com/iphone-duo/prepare/)

The following build commands are examples. Replace the workspace and scheme with repository values. Use `-project YourApp.xcodeproj` for a project. A generic build validates compilation and linking. A concrete run destination is required for runtime tests. Use the actual simulator destination ID listed by Xcode.

```sh
xcodebuild -version
xcrun --sdk iphonesimulator --show-sdk-version
xcodebuild -list -workspace YourApp.xcworkspace
xcodebuild -workspace YourApp.xcworkspace -scheme YourApp -showdestinations
xcodebuild -workspace YourApp.xcworkspace -scheme YourApp -destination 'generic/platform=iOS Simulator' build
xcodebuild -workspace YourApp.xcworkspace -scheme YourApp -destination 'platform=iOS Simulator,id=ACTUAL_DESTINATION_ID' test
```

## Code examples · 代码示例 · コード例

| File | How to use |
| --- | --- |
| [DuoLibraryView.swift](../assets/DuoLibraryView.swift) | iOS 17+ SwiftUI list/detail sample with split-view selection and a draft owned above the columns. In a demo target, use `DuoLibraryView()` as the root. Select an item, type into Notes, and fold/unfold with the keyboard visible. The draft is per item and in memory. Use the project's model if drafts must survive relaunch. |
| [DuoEditorViewController.swift](../assets/DuoEditorViewController.swift) | iOS 17+ UIKit example for standard navigation items, directional margins, Dynamic Type, scrolling, and the keyboard layout guide. Push it onto the project's navigation controller. The sample's Save button dismisses the keyboard. Connect it to the app's existing save flow when adapting the pattern. |
| [DuoReservedRegions.swift](../assets/DuoReservedRegions.swift) | Helper snippets for custom components queried in their own geometry. SwiftUI passes active division and occlusion frames to the caller's layout. UIKit returns active frames in the queried view's coordinate space. Use the selected iOS 27.1+ SDK to compile these symbols. Older iOS versions receive empty arrays. |
| [Localizable.xcstrings](../assets/Localizable.xcstrings) | Sample string catalog with English, Simplified Chinese, Japanese, German, and Arabic. The interpolated photo count illustrates language-specific plural categories. Merge selected keys into the target's catalog. If the project uses another source language or table, preserve its conventions and adjust the lookup calls. |

SwiftUI sample and catalog use English as the source language. The UIKit sample uses the same catalog. String keys for a count are extracted from interpolation at build time. Verify that Xcode produces the existing key for the actual interpolated type and check the plural forms in the catalog editor.

```swift
let photoCount = 3
Text("\(photoCount) photos")
```

Use `Label("Save", systemImage: "checkmark")` for a SwiftUI toolbar action that needs both a localized title and a symbol. Route frequent actions through the appropriate semantic toolbar placement. A text-only or custom-view item can lose vertical visibility. Provide a usable overflow route for secondary actions.

For UIKit view sizes, run idempotent geometry-dependent updates after layout, and work with the transition coordinator for custom animations if needed. For SwiftUI, prefer adaptive stacks and `ViewThatFits` when only a small group needs reflow. Use the appropriate typed measurement with `onGeometryChange` when actual container width is necessary. Keep view identity, user input, and loading tasks stable across structural layout changes. For a lower deployment target, verify every adopted API's availability in the installed SDK.

For reserved regions, query wherever the custom component performs layout. Compare rectangles in the same coordinate space. SwiftUI mirrors region frames in RTL by default. Pass `layoutDirectionBehavior: .fixed` when your placement uses coordinates that remain physically fixed. In UIKit, query from the custom view’s `updateConstraints()` to let UIKit track region changes even when bounds and size class stay the same. Keep interactive frames outside active exclusions. Prefer a system split or arrangement container if it can own that positioning. A custom grid can use inactive divisions for consistent column count while applying actual exclusion only to active geometry. Apply UIKit's published Mac Catalyst conditional-compilation workaround where applicable. [Apple layout notes](sources.md)
