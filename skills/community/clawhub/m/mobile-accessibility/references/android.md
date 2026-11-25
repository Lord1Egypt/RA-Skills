# Android accessibility: Compose, Views, TalkBack and tests

Load this when reviewing or fixing accessibility in an Android app. APIs checked against
developer.android.com (Compose semantics, accessibility defaults and testing pages, the material3 and
ui-test references, Android 14 and 16 platform notes).

## Compose semantics cookbook

| Need | Compose API | WCAG 2.2 |
|---|---|---|
| Name for an icon or image | `contentDescription` parameter, or `Modifier.semantics { contentDescription = ... }` | 1.1.1, 4.1.2 |
| Decorative image | `contentDescription = null` | 1.1.1 |
| Hide a node that carries no information | `Modifier.semantics { hideFromAccessibility() }` (`invisibleToUser()` is deprecated) | 1.3.1 |
| One focus stop for a group | `Modifier.semantics(mergeDescendants = true) {}`; `clickable` and `toggleable` merge by default | 1.3.1 |
| Replace children's semantics | `Modifier.clearAndSetSemantics { contentDescription = ... }` | 1.3.1 |
| Role and state | `toggleable(value, role = Role.Switch, ...)`, `selectable(..., role = Role.RadioButton)`, `triStateToggleable` | 4.1.2 |
| Custom state text | `Modifier.semantics { stateDescription = ... }` | 4.1.2 |
| Click hint | `clickable(onClickLabel = ...)`, `combinedClickable(onLongClickLabel = ...)` | 4.1.2 |
| Heading | `Modifier.semantics { heading() }` | 1.3.1, 2.4.6 |
| Reading order | `Modifier.semantics { isTraversalGroup = true }` and `traversalIndex = ...` | 1.3.2, 2.4.3 |
| Status message | `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` | 4.1.3 |
| Error text | `Modifier.semantics { error(message) }`, plus visible `supportingText` | 3.3.1 |
| Gesture alternative | `Modifier.semantics { customActions = listOf(CustomAccessibilityAction(label) { ...; true }) }` | 2.5.1, 2.5.7 |
| Autofill type | `Modifier.semantics { contentType = ContentType.Password }` (`androidx.compose.ui.autofill`, Compose 1.8+) | 1.3.5, 3.3.8 |
| Pane or dialog title | `Modifier.semantics { paneTitle = ... }` | 2.4.2 |
| Touch target | `Modifier.minimumInteractiveComponentSize()` (material3, reserves at least 48.dp) or `sizeIn(minWidth = 48.dp, minHeight = 48.dp)` | 2.5.8 |

### List row with secondary actions

```kotlin
// BAD: row has a clickable body, a bookmark icon and a share icon: three focus stops,
// and the icons have no names
Row(Modifier.clickable(onClick = open)) {
    Text(article.title)
    Icon(Icons.Default.BookmarkBorder, null, Modifier.clickable(onClick = bookmark))
    Icon(Icons.Default.Share, null, Modifier.clickable(onClick = share))
}

// GOOD: one focus stop that reads the title, with the secondary actions as custom actions;
// the visible icons stay tappable for touch users
Row(
    Modifier
        .clickable(onClickLabel = stringResource(R.string.open_article), onClick = open)
        .semantics {
            customActions = listOf(
                CustomAccessibilityAction(bookmarkLabel) { bookmark(); true },
                CustomAccessibilityAction(shareLabel) { share(); true },
            )
        }
) {
    Text(article.title, Modifier.weight(1f))
    IconButton(onClick = bookmark, modifier = Modifier.clearAndSetSemantics {}) {
        Icon(Icons.Default.BookmarkBorder, contentDescription = null)
    }
    IconButton(onClick = share, modifier = Modifier.clearAndSetSemantics {}) {
        Icon(Icons.Default.Share, contentDescription = null)
    }
}
```

### Selection controls

```kotlin
// GOOD: the row is the control; the Checkbox has no own click handler so it is not a second focus stop
Row(
    Modifier
        .toggleable(value = checked, role = Role.Checkbox, onValueChange = onCheckedChange)
        .padding(16.dp)
        .fillMaxWidth()
) {
    Text(label, Modifier.weight(1f))
    Checkbox(checked = checked, onCheckedChange = null)
}
```

Material components add the 48dp minimum only when they are interactive: `Checkbox(onCheckedChange = null)`
has no padding, which is correct when the parent row handles the click.

## Text scaling

- Always `sp` for text (through `MaterialTheme.typography`). Never `dp` for text size, never divide by
  `LocalDensity.current.fontScale`.
- Android 14 scales fonts up to 200 percent with a nonlinear curve. Do not compute sizes from
  `Configuration.fontScale` or `DisplayMetrics.scaledDensity`; for Views use `TypedValue.applyDimension()`
  and `TypedValue.deriveDimension()`.
- Do not use `sp` for padding or fixed heights: with nonlinear scaling, 4sp + 20sp might not equal 24sp.
- Containers with text use `heightIn(min = ...)`, not `height(...)`; avoid `maxLines = 1` on labels and buttons.
- Preview large text with `@PreviewFontScale` (a multipreview of font scales) or `@Preview(fontScale = 2f)`.
- Views: `android:textSize` and `android:lineHeight` both in `sp`.

## Views (legacy screens)

```xml
<!-- BAD: no label, 32dp target -->
<ImageButton android:layout_width="32dp" android:layout_height="32dp" android:src="@drawable/ic_delete" />

<!-- GOOD -->
<ImageButton
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:minWidth="48dp"
    android:minHeight="48dp"
    android:contentDescription="@string/delete_message"
    android:src="@drawable/ic_delete" />
```

- Decorative: `android:importantForAccessibility="no"`. Headings: `android:accessibilityHeading="true"`
  or `ViewCompat.setAccessibilityHeading(view, true)`. Labels for inputs: `android:labelFor`, or
  `TextInputLayout` with a hint.
- Live status: `android:accessibilityLiveRegion="polite"` or `ViewCompat.setAccessibilityLiveRegion(...)`.

## Motion

```kotlin
// GOOD: respects "Remove animations" (animator duration scale 0); API 26+
val animationsOn = ValueAnimator.areAnimatorsEnabled()
val spec: AnimationSpec<Float> = if (animationsOn) tween(300) else snap()
```

## Orientation and large screens

- Android 16 (targetSdk 36): orientation, resizability and aspect-ratio restrictions are ignored on displays
  with smallest width 600dp or more (games excepted). The opt-out property
  `android.window.PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY` is temporary and will not apply when
  targeting API 37. Build layouts that work in both orientations (WCAG 1.3.4).

## Automated checks

### Compose UI tests (Compose 1.8+)

```kotlin
// build.gradle.kts: same version as the other Compose ui-test artifacts, declared in libs.versions.toml
androidTestImplementation("androidx.compose.ui:ui-test-junit4-accessibility")
```

```kotlin
@get:Rule val composeTestRule = createAndroidComposeRule<ComponentActivity>()

@Test fun checkoutScreen_passesAccessibilityChecks() {
    composeTestRule.setContent { CheckoutScreen(state = previewState) }
    composeTestRule.enableAccessibilityChecks()        // requires API 34+ on the test device
    composeTestRule.onRoot().tryPerformAccessibilityChecks()
}
```

- After `enableAccessibilityChecks()`, every action such as `performClick()` also runs the checks.
- Pass an `AccessibilityValidator` to tune the checks, for example
  `AccessibilityValidator().setThrowExceptionFor(AccessibilityCheckResult.AccessibilityCheckResultType.WARNING)`.
- The checks cover missing labels, contrast, touch target size and traversal order.

### Semantics assertions (any API level)

```kotlin
composeTestRule.onNodeWithContentDescription("Delete message").assertHasClickAction()
composeTestRule.onNode(hasText("Payment method") and isHeading()).assertExists()
composeTestRule.onNode(SemanticsMatcher.expectValue(SemanticsProperties.Role, Role.Switch))
    .performClick().assertIsOn()
composeTestRule.onNodeWithTag("closeButton").assertHeightIsAtLeast(48.dp).assertWidthIsAtLeast(48.dp)
```

### Espresso (Views)

```kotlin
// androidTestImplementation("androidx.test.espresso:espresso-accessibility:<version>")
@Before fun enableChecks() { AccessibilityChecks.enable() }   // runs on every ViewAction
```

### Outside tests

- Accessibility Scanner (Google Play): Snapshot for one screen, Record for a flow. Checks content labels,
  touch target size, clickable items, text and image contrast.
- Google Play pre-launch report: Accessibility tab with touch target, contrast, labeling and implementation results.
- Android Studio Compose UI Check mode on a preview audits accessibility issues such as low contrast.

## TalkBack quick reference

- Enable: Settings > Accessibility > TalkBack, or volume-key shortcut. Developer setting "Log output level:
  VERBOSE" helps debugging.
- Swipe right or left: next or previous element. Double tap: activate. Two-finger swipe: scroll.
- The TalkBack menu lists custom actions ("Actions") and reading controls. Its gesture differs between
  TalkBack versions and devices; check it on the test device.
- Switch Access: check that every action is reachable and each item is highlighted once.

The full manual procedure is in the manual test script reference.
