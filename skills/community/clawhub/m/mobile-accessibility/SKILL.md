---
name: mobile-accessibility
description: "Audits and fixes accessibility in Android, iOS and Flutter apps against WCAG 2.2 level AA and EN 301 549, and checks whether the European Accessibility Act applies. Covers Compose semantics, TalkBack, SwiftUI modifiers, VoiceOver, Dynamic Type, Flutter Semantics, touch targets, contrast, font scaling and automated checks. Engineering guidance, not legal advice. Use for accessibility reviews, EAA readiness, screen reader bugs or a11y tests."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile accessibility

Make an Android, iOS or Flutter app usable with a screen reader, large text, switch or keyboard access and
reduced motion, and show it: decide whether the European Accessibility Act (EAA) applies, test the critical
user journeys automatically and by hand, and report each failure against a WCAG 2.2 success criterion with
evidence and a code fix.

**This is engineering guidance, not legal advice.** The agent reports what the app does and which success
criterion or clause it relates to. Whether the EAA applies, whether an exemption or the disproportionate
burden clause can be used, and what goes into the accessibility statement are decisions for the team's
compliance or legal owner. Where a point cannot be verified, the agent says so instead of guessing.

## When to use

- "Is our app in scope of the European Accessibility Act?" or "Are we EAA ready?"
- Accessibility review of a screen, a pull request or a whole app against WCAG 2.2 AA or EN 301 549.
- TalkBack or VoiceOver bug reports: unlabeled buttons, wrong reading order, focus lost after a dialog.
- Text cut off at large font sizes, small touch targets, low contrast, animations that ignore Reduce Motion.
- Adding automated accessibility checks to Compose, Espresso, XCUITest or Flutter widget tests.
- Writing the accessibility information a service provider has to publish (EAA Annex V).

Not for: general code review (use `mobile-code-review`, which calls out basic accessibility), CRA, RED or GDPR
(use `mobile-eu-compliance`), or store listing and review rules (use `mobile-release`).

## Verified key facts

Checked against the Official Journal text of Directive (EU) 2019/882
(https://eur-lex.europa.eu/eli/dir/2019/882/oj/eng), EN 301 549 V4.1.1 from the ETSI deliverables listing and
the WCAG 2.2 Recommendation. Re-check before quoting them in customer-facing documents.

| Topic | Fact |
|---|---|
| EAA application date | National measures apply from 28 June 2025 (Art. 31(2)); covers products placed on the market and services provided to consumers after that date (Art. 2(1) and (2)) |
| Services in scope (Art. 2(2)) | Electronic communications services; services providing access to audiovisual media services; listed elements of air, bus, rail and waterborne passenger transport (websites, mobile apps, e-tickets, travel information); consumer banking services; e-books and dedicated software; e-commerce services |
| E-commerce (Art. 3(30), recital 43) | Services at a distance, through websites and mobile device-based services, at the individual request of a consumer, with a view to concluding a consumer contract; recital 43 says this applies to the online sale of any product or service |
| Mobile app requirement (Annex I, Section III(c)) | Make "mobile device-based services, including mobile applications, accessible in a consistent and adequate way by making them perceivable, operable, understandable and robust" |
| Microenterprise exemption (Art. 4(5), Art. 3(23)) | Microenterprises providing services are exempt from the service requirements. Microenterprise: fewer than 10 persons and annual turnover or balance sheet total not exceeding EUR 2 million. Product manufacturers are not exempt (Art. 14(4) only lightens documentation) |
| Content not covered (Art. 2(4)) | Pre-recorded time-based media and office files published before 28 June 2025, some online maps, third-party content not funded, developed or controlled by the operator, archives not updated after 28 June 2025 |
| Transitional measures (Art. 32(1)) | Until 28 June 2030 services may keep using products lawfully used before that date; service contracts agreed before 28 June 2025 may continue until they expire, at most five years |
| Information duty (Art. 13(2), Annex V) | Service providers publish how the service meets the requirements, in the general terms and conditions or an equivalent document, in accessible form |
| Exceptions (Art. 14) | Fundamental alteration or disproportionate burden only with a documented assessment, kept for five years |
| EN 301 549 | V4.1.1 (2026-09) is the harmonised standard prepared for the EAA and aligned with WCAG 2.2; it gives presumption of conformity only once cited in the Official Journal under the EAA (check the citation status). Clause 11 (non-web software) applies to mobile apps, including web views inside them |
| WCAG 2.2 | W3C Recommendation (current version dated 12 December 2024). New at AA: 2.4.11, 2.5.7, 2.5.8, 3.3.8; new at A: 3.2.6, 3.3.7; 4.1.1 Parsing removed |

## Workflow

1. **Scope.** Decide whether the EAA applies before rating anything as a legal gap.
   - Is the app part of a service in Art. 2(2), provided to consumers in the EU? An IoT companion app,
     a game or a B2B tool is not listed as such, but an in-app shop or a checkout can make it e-commerce.
   - Microenterprise providing services (Art. 4(5))? Record the facts, not a conclusion. Public sector app:
     Directive (EU) 2016/2102 applies instead or as well.
   - Use the decision table in [EAA, EN 301 549 and WCAG 2.2](references/eaa-wcag.md). Open scope points go
     to the compliance owner. WCAG 2.2 AA is still the engineering target when the EAA does not apply.
2. **Critical journeys.** List the screens a user must be able to finish: onboarding, sign-in, the core
   task, purchase or payment, settings, help and error states. Audit these first.
3. **Load the platform reference** for the code under review:
   [Android](references/android.md), [iOS](references/ios.md), [Flutter](references/flutter.md).
4. **Static review.** Walk the rules below over each screen's code. Note file:line for every candidate.
5. **Automated checks.** Run what the project has, add what it lacks:
   - Android: Compose `enableAccessibilityChecks()`, Espresso `AccessibilityChecks.enable()`, Accessibility
     Scanner on a device, the Play pre-launch report.
   - iOS: `XCUIApplication().performAccessibilityAudit()` in a UI test (iOS 17 or later), Accessibility Inspector.
   - Flutter: `meetsGuideline(...)` widget tests with the four built-in guidelines.
   - Automated checks catch only part of the issues. A clean run is not a pass.
6. **Manual test.** Run the [manual screen reader test script](references/manual-test-script.md) with
   TalkBack and VoiceOver, at 200 percent text, with Reduce Motion and with a hardware keyboard or switch.
7. **Map and rate.** Each finding gets one WCAG 2.2 success criterion (number and name), a severity (see
   Output format), the screen, platform, evidence and a fix. For EN 301 549, mobile apps use clause 11: for
   most criteria the clause number is 11 followed by the WCAG number (1.4.3 is 11.1.4.3).
8. **Report** in the output format below. Fix code only when asked; add a regression test for every fix.

## Rules

### 1. Every control and meaningful image has a name; decorative content is hidden (1.1.1, 4.1.2, 2.5.3)

```kotlin
// BAD: icon-only button, TalkBack announces only "Button"
IconButton(onClick = onDelete) { Icon(Icons.Default.Delete, contentDescription = null) }

// GOOD: localized name on the actionable icon; decorative image explicitly null
IconButton(onClick = onDelete) {
    Icon(Icons.Default.Delete, contentDescription = stringResource(R.string.delete_message))
}
Image(painterResource(R.drawable.header_wave), contentDescription = null)
```

```swift
// BAD: no label, VoiceOver falls back to whatever it can derive from the image
Button(action: delete) { Image(systemName: "trash") }

// GOOD: the title is the accessibility label, the icon is what sighted users see
Button(action: delete) { Label("Delete message", systemImage: "trash") }
    .labelStyle(.iconOnly)
Image(decorative: "header-wave")
```

```dart
// BAD
IconButton(icon: const Icon(Icons.delete), onPressed: onDelete);

// GOOD: tooltip becomes the semantics label; decorative image excluded
IconButton(icon: const Icon(Icons.delete), tooltip: l10n.deleteMessage, onPressed: onDelete);
Image.asset('assets/header_wave.png', excludeFromSemantics: true);
```

- The visible text must be part of the accessible name (2.5.3 Label in Name), so voice control works.
- Names describe the action or content, not the widget type: "Delete message", not "Delete button".

### 2. Roles and states are exposed, preferably by native controls (4.1.2)

```kotlin
// BAD: two focus stops, no role on the row, state announced separately
Row(Modifier.clickable { onToggle() }) {
    Text("Wi-Fi")
    Switch(checked = on, onCheckedChange = { onToggle() })
}

// GOOD: one focus stop with role Switch and its on/off state
Row(Modifier.toggleable(value = on, role = Role.Switch, onValueChange = { onToggle() }).padding(16.dp)) {
    Text("Wi-Fi", Modifier.weight(1f))
    Switch(checked = on, onCheckedChange = null)
}
```

```swift
// BAD: looks like a toggle, VoiceOver hears static text
HStack { Text("Wi-Fi"); Spacer(); if on { Image(systemName: "checkmark") } }
    .onTapGesture { on.toggle() }

// GOOD: native control carries role and value
Toggle("Wi-Fi", isOn: $on)
```

```dart
// BAD
GestureDetector(onTap: toggle, child: Row(children: [const Text('Wi-Fi'), if (on) const Icon(Icons.check)]));

// GOOD
SwitchListTile(title: const Text('Wi-Fi'), value: on, onChanged: (_) => toggle());
```

### 3. Related content is one focus stop and the reading order follows the layout (1.3.1, 1.3.2, 2.4.3)

```kotlin
// BAD: avatar, name, time and preview are four swipes each
Row { Avatar(user); Column { Text(name); Text(time); Text(preview) } }

// GOOD: one node; clickable rows merge automatically
Row(Modifier.semantics(mergeDescendants = true) {}) { Avatar(user); Column { Text(name); Text(time); Text(preview) } }
```

```swift
// GOOD
HStack { Avatar(user); VStack { Text(name); Text(time); Text(preview) } }
    .accessibilityElement(children: .combine)
```

```dart
// GOOD
MergeSemantics(child: ListTile(leading: Avatar(user), title: Text(name), subtitle: Text(preview)));
```

- Fix reading order with the layout first. Override only when needed: `isTraversalGroup` and `traversalIndex`
  (Compose), `accessibilitySortPriority` (SwiftUI), `OrdinalSortKey` (Flutter).

### 4. Touch targets are at least 48dp on Android and 44pt on iOS (2.5.8)

WCAG 2.5.8 sets a 24 by 24 CSS pixel floor at AA. Material guidance (48dp) and the Apple HIG default
control size (44x44 pt) are stricter; use them as the engineering target.

```kotlin
// BAD: 24dp clickable icon with neighbours close by
Icon(Icons.Default.Close, stringResource(R.string.close), Modifier.size(24.dp).clickable(onClick = onClose))

// GOOD: IconButton reserves 48dp; custom clickables add Modifier.minimumInteractiveComponentSize()
IconButton(onClick = onClose) { Icon(Icons.Default.Close, stringResource(R.string.close)) }
```

```swift
// GOOD: visual size stays small, hit area grows
Button(action: close) { Image(systemName: "xmark") }
    .frame(minWidth: 44, minHeight: 44)
    .contentShape(Rectangle())
    .accessibilityLabel("Close")
```

```dart
// BAD: shrinks Material tap targets below 48
IconButton(style: IconButton.styleFrom(tapTargetSize: MaterialTapTargetSize.shrinkWrap), ...);

// GOOD: keep the default padded size, or enforce it for custom widgets
ConstrainedBox(constraints: const BoxConstraints(minWidth: 48, minHeight: 48), child: child);
```

### 5. Text follows the system size up to 200 percent without loss of content (1.4.4, 1.4.10, 1.4.12)

```kotlin
// BAD: fixed height cuts text at large font scale; dividing by fontScale cancels the user's setting
Box(Modifier.height(40.dp)) { Text(label, maxLines = 1, fontSize = (14 / LocalDensity.current.fontScale).sp) }

// GOOD: sp from the theme, minimum height instead of fixed height, wraps
Box(Modifier.heightIn(min = 40.dp)) { Text(label, style = MaterialTheme.typography.bodyLarge) }
```

```swift
// BAD
Text(label).font(.system(size: 15)).frame(height: 40)

// GOOD: text style scales with Dynamic Type; switch layout at accessibility sizes
@Environment(\.dynamicTypeSize) private var typeSize
@ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 24
var body: some View {
    let layout = typeSize.isAccessibilitySize ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())
    layout { Image(systemName: "bolt").frame(width: iconSize, height: iconSize); Text(label).font(.body) }
}
```

```dart
// BAD: switches off text scaling for the whole app
MediaQuery(data: MediaQuery.of(context).copyWith(textScaler: TextScaler.noScaling), child: app);

// GOOD: let text scale; clamp only a widget that truly cannot grow, and never below 2.0
MediaQuery.withClampedTextScaling(maxScaleFactor: 2.0, child: const BottomBarLabels());
```

### 6. Contrast is sufficient and colour is never the only signal (1.4.3, 1.4.11, 1.4.1)

- Text: at least 4.5:1, large text 3:1. Icons, focus indicators and control borders: 3:1 against adjacent colours.

```kotlin
// BAD: #9E9E9E on white is about 2.7:1; the error is shown only as a red border
Text(hint, color = Color(0xFF9E9E9E))
OutlinedTextField(value, onValueChange, isError = invalid)

// GOOD: #616161 on white is about 6.2:1; the error is also text, read by TalkBack
Text(hint, color = Color(0xFF616161))
OutlinedTextField(value, onValueChange, isError = invalid,
    supportingText = { if (invalid) Text(errorText) },
    modifier = Modifier.semantics { if (invalid) error(errorText) })
```

```swift
// GOOD: semantic colours adapt to dark mode and Increase Contrast
Text(hint).foregroundStyle(.secondary)
if invalid { Label(errorText, systemImage: "exclamationmark.triangle").foregroundStyle(.red) }
```

```dart
// GOOD: errorText is shown and announced, not only the red outline
TextField(decoration: InputDecoration(labelText: l10n.email, errorText: invalid ? l10n.emailInvalid : null));
```

### 7. Screens have titles and sections have headings (2.4.6, 1.3.1; EN 301 549 11.2.4.2)

```kotlin
// BAD
Text("Payment method", style = MaterialTheme.typography.titleMedium)

// GOOD
Text("Payment method", style = MaterialTheme.typography.titleMedium, modifier = Modifier.semantics { heading() })
```

```swift
// GOOD
Text("Payment method").font(.headline).accessibilityAddTraits(.isHeader)
```

```dart
// GOOD
Semantics(header: true, child: Text(l10n.paymentMethod, style: Theme.of(context).textTheme.titleMedium));
```

### 8. Status changes are announced without moving focus (4.1.3, 3.3.1)

```kotlin
// BAD: "Saved" appears visually only
if (saved) Text(stringResource(R.string.saved))

// GOOD
Text(statusText, Modifier.semantics { liveRegion = LiveRegionMode.Polite })
```

```swift
// GOOD (iOS 17 and later; use UIAccessibility.post(notification: .announcement, argument:) before that)
AccessibilityNotification.Announcement("Saved").post()
```

```dart
// GOOD: live region on the status widget; Android discourages announcement events
Semantics(liveRegion: true, child: Text(statusText));
```

- Use assertive or high-priority announcements only for time-critical information. No live region on timers.

### 9. Gestures have a single-tap alternative exposed to assistive technology (2.5.1, 2.5.7)

```kotlin
// BAD: swipe-to-delete is the only way to delete
SwipeToDismissBox(state, backgroundContent = { DeleteBackground() }) { MessageRow(m) }

// GOOD: same action as a custom accessibility action (and a visible menu item)
MessageRow(m, Modifier.semantics {
    customActions = listOf(CustomAccessibilityAction(deleteLabel) { onDelete(m); true })
})
```

```swift
// GOOD
MessageRow(message).accessibilityAction(named: "Delete") { delete(message) }
```

```dart
// GOOD
Semantics(
  customSemanticsActions: {CustomSemanticsAction(label: l10n.delete): () => onDelete(m)},
  child: MessageRow(m),
);
```

- Drag to reorder, sliders and maps need buttons or an equivalent control that works without dragging.

### 10. Motion respects Reduce Motion; nothing flashes (2.2.2, 2.3.1; EAA Annex I Section VII(i))

```kotlin
// GOOD: skip decorative animation when the user removed animations (API 26+)
val animate = ValueAnimator.areAnimatorsEnabled()
```

```swift
// GOOD
@Environment(\.accessibilityReduceMotion) private var reduceMotion
withAnimation(reduceMotion ? nil : .default) { expanded.toggle() }
```

```dart
// GOOD
final duration = MediaQuery.disableAnimationsOf(context) ? Duration.zero : const Duration(milliseconds: 300);
```

- Auto-playing carousels and looping animations longer than five seconds need pause, stop or hide (2.2.2).
- Nothing flashes more than three times per second (2.3.1).

### 11. Sign-in and forms work with password managers, autofill and labels (3.3.8, 3.3.2, 1.3.5, 3.3.7)

```kotlin
// BAD: placeholder as the only label, paste blocked, no autofill type
TextField(value, onValueChange, placeholder = { Text("Password") })

// GOOD: persistent label, autofill hint (Compose 1.8+), paste allowed
OutlinedTextField(value, onValueChange, label = { Text(stringResource(R.string.password)) },
    visualTransformation = PasswordVisualTransformation(),
    modifier = Modifier.semantics { contentType = ContentType.Password })
```

```swift
// GOOD
SecureField("Password", text: $password).textContentType(.password)
```

```dart
// GOOD
AutofillGroup(child: TextField(
  obscureText: true,
  autofillHints: const [AutofillHints.password],
  decoration: InputDecoration(labelText: l10n.password),
));
```

- Offer an alternative to memory or puzzle tests: passkeys, biometrics, magic links, copy and paste of codes.
- Do not ask for data already entered in the same flow (3.3.7 Redundant Entry).

## Anti-patterns

- Declaring the app "EAA compliant" or "WCAG conformant". The report states what was tested and found.
- Assuming every app is in EAA scope, or that none is. Scope follows Art. 2 and the provider's role.
- Treating a clean Accessibility Scanner, audit or `meetsGuideline` run as a pass. Manual testing is required.
- Labels that repeat the role ("Button, delete button") or describe the icon ("trash can") instead of the action.
- Hiding content from screen readers to "reduce noise" when it carries information.
- Disabling or clamping font scaling app-wide; fixed heights on text containers; `maxLines = 1` on labels.
- Custom gesture-only interactions with no accessibility action.
- Locking portrait for convenience (1.3.4). Android 16 ignores orientation locks on large screens anyway.
- Overlay "accessibility widgets" or SDKs that claim to fix an app automatically.
- Inventing article numbers, success criterion numbers or deadlines. If a citation cannot be confirmed, say so.

## Checklist

- [ ] EAA scope recorded: service category, consumer-facing, provider role, microenterprise facts, open questions
- [ ] Critical journeys listed and each one tested end to end with TalkBack and VoiceOver
- [ ] Every actionable element has a localized, action-based name; decorative images hidden
- [ ] Custom controls expose role and state; native controls preferred
- [ ] Related content merged; reading and focus order match the visual order; focus moves into dialogs and back
- [ ] Touch targets at least 48dp / 44pt, or at minimum 24 by 24 with spacing
- [ ] Text scales to 200 percent without clipping or overlap; no app-wide scaling override
- [ ] Contrast 4.5:1 for text, 3:1 for large text, icons and control borders; no colour-only meaning
- [ ] Headings marked; each screen has a title
- [ ] Status messages and errors announced; errors also shown as text
- [ ] Gestures and dragging have alternatives exposed as accessibility actions
- [ ] Reduce Motion respected; no flashing; auto-playing motion can be paused
- [ ] Sign-in supports password managers, autofill and paste; fields have persistent labels
- [ ] Automated checks run in CI: Compose or Espresso checks, XCUITest audit, Flutter guideline tests
- [ ] Accessibility information for Annex V drafted if the EAA applies
- [ ] Report says "engineering guidance, not legal advice" and lists unverified points

## Output format

~~~markdown
## Accessibility report: <app / version / build>

Engineering assessment, not legal advice. Scope and conformity decisions belong to <compliance owner>.

Target: WCAG 2.2 level AA (EN 301 549 V4.1.1 clause 11 for mobile). Devices: <model, OS and screen reader versions>. Journeys tested: <sign-in, checkout, settings>.
EAA: <in scope as e-commerce service | not in scope | open question>. Microenterprise: <facts or unknown>.

| ID | WCAG 2.2 SC | Severity | Screen | Platform | Evidence | Fix |
|---|---|---|---|---|---|---|
| A11Y-01 | 1.1.1 Non-text Content, 4.1.2 Name, Role, Value | Blocker | Checkout | Android | Pay button is an Icon with `contentDescription = null` (`CheckoutScreen.kt:88`); TalkBack: "Button" | Add localized contentDescription (rule 1) |
| A11Y-02 | 1.4.4 Resize Text | Major | Settings | iOS | At AX3 the row title is truncated; `.frame(height: 44)` in `SettingsRow.swift:21` | Replace with `minHeight`, use text styles (rule 5) |
| A11Y-03 | 2.5.8 Target Size (Minimum) | Minor | Feed | Flutter | `meetsGuideline(androidTapTargetGuideline)` fails: like button 32x32 (`feed_item.dart:54`) | Remove `shrinkWrap`, 48x48 min (rule 4) |

### Automated checks
- <tool, version, result, link to CI run>

### Open questions for the compliance owner
- <for example: does the in-app subscription purchase make the app an e-commerce service?>

### Not tested
- <screens, platforms, assistive technologies, third-party content not under the team's control>
~~~

Severity: Blocker -- a user of assistive technology cannot complete a critical journey (sign-in, payment,
core task). Major -- the journey is possible but a criterion fails on a critical screen or app-wide.
Minor -- a criterion fails on a secondary screen, or the issue slows users down without blocking them.

Every finding has exactly one primary success criterion (add a second only when both fail for the same cause),
evidence a reviewer can reproduce, and a fix. Order by severity.

## Related skills

- `mobile-code-review` -- general review that flags basic accessibility issues in a diff
- `mobile-testing` -- test setup for the Compose, XCUITest and Flutter accessibility checks
- `mobile-eu-compliance` -- CRA, RED and GDPR assessment for the same product
- `mobile-release` -- store listing, release notes and the published accessibility information
- `mobile-ci-cd` -- running accessibility tests on every pull request
- `mobile-kotlin`, `mobile-swift`, `mobile-flutter` -- language and UI framework rules the fixes follow
