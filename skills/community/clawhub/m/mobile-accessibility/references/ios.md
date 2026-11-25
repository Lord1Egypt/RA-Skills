# iOS accessibility: SwiftUI, UIKit, VoiceOver and tests

Load this when reviewing or fixing accessibility in an iOS app. APIs and availability checked against
developer.apple.com documentation (SwiftUI, Accessibility, UIKit, XCUIAutomation) and the Human Interface
Guidelines accessibility page.

## SwiftUI cookbook

| Need | SwiftUI API | Availability | WCAG 2.2 |
|---|---|---|---|
| Name | `.accessibilityLabel(_:)`, or a `Label` / `Button` title | iOS 14 | 1.1.1, 4.1.2 |
| Usage hint | `.accessibilityHint(_:)` (short, optional, not a second label) | iOS 14 | 3.3.2 |
| Value of a custom control | `.accessibilityValue(_:)` | iOS 14 | 4.1.2 |
| Role and state | Native `Toggle`, `Button`, `Picker`, `Slider`; else `.accessibilityAddTraits(.isButton)`, `.isSelected`, `.isHeader` | iOS 14 | 4.1.2 |
| Heading | `.accessibilityAddTraits(.isHeader)` or `.accessibilityHeading(.h2)` | iOS 14 / 15 | 1.3.1 |
| Group | `.accessibilityElement(children: .combine)`, `.ignore` with own label, `.contain` | iOS 13 | 1.3.1 |
| Hide decoration | `Image(decorative:)`, `.accessibilityHidden(true)` | iOS 14 | 1.1.1 |
| Custom control semantics | `.accessibilityRepresentation { Slider(...) }` | iOS 15 | 4.1.2 |
| Gesture alternative | `.accessibilityAction(named:_:)`, `.accessibilityAdjustableAction` | iOS 14 | 2.5.1, 2.5.7 |
| Reading order | `.accessibilitySortPriority(_:)` | iOS 14 | 1.3.2 |
| Move focus | `@AccessibilityFocusState` with `.accessibilityFocused(_:)` | iOS 15 | 2.4.3 |
| Voice Control names | `.accessibilityInputLabels(_:)` | iOS 14 | 2.5.3 |
| Announcement | `AccessibilityNotification.Announcement("...").post()` | iOS 17 | 4.1.3 |
| Screen or layout change | `AccessibilityNotification.ScreenChanged`, `.LayoutChanged` | iOS 17 | 2.4.3 |
| Scaled size | `@ScaledMetric(relativeTo: .body)` | iOS 14 | 1.4.4 |
| Text size category | `@Environment(\.dynamicTypeSize)`, `.isAccessibilitySize` | iOS 15 | 1.4.4, 1.4.10 |
| Reduce Motion | `@Environment(\.accessibilityReduceMotion)` | iOS 13 | 2.2.2, 2.3.1 |
| Increase Contrast | `@Environment(\.colorSchemeContrast)` | iOS 13 | 1.4.3, 1.4.11 |
| Bold Text | `@Environment(\.legibilityWeight)` | iOS 13 | 11.7 user preferences |
| Differentiate Without Color | `@Environment(\.accessibilityDifferentiateWithoutColor)` | iOS 13 | 1.4.1 |
| Reduce Transparency | `@Environment(\.accessibilityReduceTransparency)` | iOS 13 | 1.4.3 |

### Card with a custom label and actions

```swift
// BAD: five VoiceOver stops; the price is read before the title; favourite is unlabeled
VStack {
    AsyncImage(url: item.imageURL)
    Text(item.price)
    Text(item.title)
    Button { toggleFavourite() } label: { Image(systemName: item.isFavourite ? "heart.fill" : "heart") }
}

// GOOD: one element with a meaningful label; favourite exposed as a named action and a trait
VStack {
    AsyncImage(url: item.imageURL).accessibilityHidden(true)
    Text(item.title)
    Text(item.price)
    Button { toggleFavourite() } label: {
        Label("Favourite", systemImage: item.isFavourite ? "heart.fill" : "heart").labelStyle(.iconOnly)
    }
}
.accessibilityElement(children: .ignore)
.accessibilityLabel("\(item.title), \(item.price)")
.accessibilityValue(item.isFavourite ? "Favourite" : "")
.accessibilityAddTraits(.isButton)
.accessibilityAction { open(item) }
.accessibilityAction(named: item.isFavourite ? "Remove from favourites" : "Add to favourites") { toggleFavourite() }
```

### Focus after a sheet or error

```swift
@AccessibilityFocusState private var errorFocused: Bool

VStack {
    if let error { Text(error).accessibilityFocused($errorFocused) }
    Button("Pay") { Task { await pay() } }
}
.onChange(of: error) { _, newValue in errorFocused = newValue != nil }
```

## Dynamic Type

- Use text styles: `.font(.body)`, `.font(.headline)`. A custom font scales with
  `.font(.custom("Brand", size: 17, relativeTo: .body))`.
- No fixed `frame(height:)` on text; use `minHeight`. Let text wrap; avoid `.lineLimit(1)` on labels.
- Switch to a vertical layout at accessibility sizes (`dynamicTypeSize.isAccessibilitySize`) with `AnyLayout`
  (iOS 16) or `ViewThatFits`.
- Do not cap with `.dynamicTypeSize(...DynamicTypeSize.large)` app-wide. A cap on a single element that
  truly cannot grow should still allow accessibility sizes, and the content must stay reachable (for example
  through the Large Content Viewer for tab bar items).
- The HIG asks for text that can be enlarged by at least 200 percent (140 percent on watchOS).
- UIKit: `UIFont.preferredFont(forTextStyle:)` or `UIFontMetrics(forTextStyle:).scaledFont(for:)`, plus
  `adjustsFontForContentSizeCategory = true` on labels, text fields and text views.

## Touch targets and contrast (HIG)

- Default control size on iOS and iPadOS: 44x44 pt; minimum 28x28 pt. Use 44x44 for anything a user taps
  often; WCAG 2.5.8 sets the 24 by 24 floor.
- Enlarge hit areas without changing visuals: `.frame(minWidth: 44, minHeight: 44)` plus
  `.contentShape(Rectangle())`.
- HIG contrast guidance follows WCAG AA: 4.5:1 up to 17 pt text, 3:1 at 18 pt or bold text. Provide a
  higher-contrast variant when Increase Contrast is on (asset catalog "High Contrast" appearance or
  `colorSchemeContrast`).

## Motion

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

// BAD: parallax and zoom regardless of the setting
.scaleEffect(isPressed ? 1.2 : 1).animation(.spring, value: isPressed)

// GOOD: replace motion with a cross-fade or no animation
.scaleEffect(reduceMotion ? 1 : (isPressed ? 1.2 : 1))
.animation(reduceMotion ? nil : .default, value: isPressed)
```

UIKit: `UIAccessibility.isReduceMotionEnabled` and its change notification.

## UIKit essentials

```swift
// BAD
let button = UIButton(type: .custom)
button.setImage(UIImage(systemName: "trash"), for: .normal)

// GOOD
button.accessibilityLabel = String(localized: "Delete message")
headerLabel.accessibilityTraits.insert(.header)
decorativeImageView.isAccessibilityElement = false
UIAccessibility.post(notification: .announcement, argument: String(localized: "Saved"))
```

## Automated checks

### XCUITest accessibility audit (iOS 17 and later)

```swift
final class AccessibilityAuditTests: XCTestCase {
    @MainActor
    func testCheckoutScreen() throws {
        let app = XCUIApplication()
        app.launch()
        app.buttons["Checkout"].tap()

        try app.performAccessibilityAudit()   // fails the test for every issue found
    }

    @MainActor
    func testSettingsDynamicTypeAndContrast() throws {
        let app = XCUIApplication()
        app.launch()
        try app.performAccessibilityAudit(for: [.dynamicType, .contrast, .textClipped]) { issue in
            // Return true only to ignore a reviewed, documented false positive
            issue.auditType == .contrast && issue.element?.identifier == "brandLogo"
        }
    }
}
```

- Audit types (`XCUIAccessibilityAuditType`): `.all`, `.contrast`, `.dynamicType`, `.elementDetection`,
  `.hitRegion`, `.parentChild`, `.sufficientElementDescription`, `.textClipped`, `.trait`, `.action`.
  Not every type applies to every platform; check the documentation for the Xcode version in CI.
- Issues expose `auditType`, `element`, `compactDescription` and `detailedDescription`; put them in the
  report's evidence.
- The audit checks the current screen only: navigate to each critical screen and state, then audit.
- The current documentation lists the API under the XCUIAutomation framework. The test target needs an iOS 17
  or later simulator or device.

### Accessibility Inspector

Xcode > Open Developer Tool > Accessibility Inspector: inspect labels, traits and values on a simulator or
device, and run an audit on the current screen. Use Environment Overrides in the Xcode debug bar to switch
text size, Increase Contrast and other settings while the app runs.

### Previews

```swift
#Preview("AX5") { CheckoutView().environment(\.dynamicTypeSize, .accessibility5) }
```

## VoiceOver quick reference

- Enable: Settings > Accessibility > VoiceOver, or the Accessibility Shortcut (triple-click the side button).
- Swipe right or left: next or previous element. Double tap: activate. Three-finger swipe: scroll.
- Rotor (rotate two fingers): headings, actions, links, form controls. Custom actions appear under "Actions".
- Two-finger scrub ("Z" gesture): go back or dismiss; make sure custom modals support it
  (`.accessibilityAction(.escape)` or UIKit `accessibilityPerformEscape()`).
- Also test Voice Control (names spoken match visible labels) and Full Keyboard Access with a hardware keyboard.

The full manual procedure is in the manual test script reference.
