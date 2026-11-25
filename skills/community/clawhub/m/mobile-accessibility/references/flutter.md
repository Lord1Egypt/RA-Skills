# Flutter accessibility: Semantics, text scaling and guideline tests

Load this when reviewing or fixing accessibility in a Flutter app. APIs checked against api.flutter.dev
(widgets, semantics, painting and flutter_test libraries).

## Semantics cookbook

| Need | Flutter API | WCAG 2.2 |
|---|---|---|
| Name for an icon button | `IconButton(tooltip: ...)`; `Icon(semanticLabel: ...)` for a meaningful standalone icon | 1.1.1, 4.1.2 |
| Name for an image | `Image(semanticLabel: ...)`; decorative: `excludeFromSemantics: true` | 1.1.1 |
| Custom widget semantics | `Semantics(label:, hint:, value:, button: true, onTap:, child:)` | 4.1.2 |
| Toggle, check and selection state | `Semantics(toggled:, checked:, selected:, enabled:)`, or Material `Switch`, `Checkbox`, `Radio` | 4.1.2 |
| Heading | `Semantics(header: true)`; `headingLevel` for a level | 1.3.1, 2.4.6 |
| One focus stop for a group | `MergeSemantics(child: ...)` | 1.3.1 |
| Replace children's semantics | `Semantics(excludeSemantics: true, label: ..., child: ...)` | 1.3.1 |
| Hide decoration | `ExcludeSemantics(child: ...)` | 1.1.1 |
| Hide content behind a modal | `BlockSemantics` (Material dialogs and sheets do this already) | 2.4.3 |
| Reading order | Fix the widget order first; otherwise `Semantics(sortKey: OrdinalSortKey(1))` on the siblings | 1.3.2 |
| Status message | `Semantics(liveRegion: true, child: Text(status))` | 4.1.3 |
| Announcement | `SemanticsService.sendAnnouncement(View.of(context), message, TextDirection.ltr)` (`announce` is deprecated since 3.35) | 4.1.3 |
| Gesture alternative | `Semantics(customSemanticsActions: {CustomSemanticsAction(label: ...): handler})` | 2.5.1, 2.5.7 |
| Autofill | `TextField(autofillHints: const [AutofillHints.email])` inside `AutofillGroup` | 1.3.5, 3.3.8 |
| Stable id for tests | `Semantics(identifier: 'checkout_pay')` | - |
| Touch target | Material default `MaterialTapTargetSize.padded` (48x48); `ConstrainedBox` for custom widgets | 2.5.8 |

### Custom tappable card

```dart
// BAD: GestureDetector has no role, no label; the image is read as "image"
GestureDetector(
  onTap: () => open(item),
  child: Column(children: [Image.network(item.imageUrl), Text(item.title), Text(item.price)]),
);

// GOOD: one button node with a meaningful label, decorative image excluded, favourite as an action
Semantics(
  button: true,
  label: '${item.title}, ${item.price}',
  onTapHint: l10n.openDetails,
  excludeSemantics: true,
  customSemanticsActions: {
    CustomSemanticsAction(label: item.isFavourite ? l10n.removeFavourite : l10n.addFavourite):
        () => toggleFavourite(item),
  },
  child: InkWell(
    onTap: () => open(item),
    child: Column(children: [
      Image.network(item.imageUrl, excludeFromSemantics: true),
      Text(item.title),
      Text(item.price),
    ]),
  ),
);
```

Keep a visible favourite button for touch users too; the custom action is the screen reader path.

## Text scaling

- Read the scaler with `MediaQuery.textScalerOf(context)`. `MediaQuery.textScaleFactorOf` and
  `TextScaler.textScaleFactor` exist for backward compatibility only; do not build new code on them.
- Never wrap the app in `MediaQuery(data: ...copyWith(textScaler: TextScaler.noScaling))`.
- `MediaQuery.withClampedTextScaling(maxScaleFactor: ...)` and `MediaQuery.withNoTextScaling` exist for a
  subtree that truly cannot grow. Use them locally, keep the maximum at 2.0 or more, and justify each use.
- No fixed `SizedBox(height: ...)` around text; use `ConstrainedBox(constraints: BoxConstraints(minHeight: ...))`.
  Let `Row`s wrap (`Wrap`, or switch to `Column` when `textScaler.scale(14) > 28`).
- Test at a scale of 2.0 in widget tests (see below) and on a device at the largest system setting.

## Other user preferences (EN 301 549 11.7)

```dart
final reduceMotion = MediaQuery.disableAnimationsOf(context); // Reduce Motion / Remove animations
final boldText = MediaQuery.boldTextOf(context);               // iOS Bold Text
final highContrast = MediaQuery.highContrastOf(context);       // iOS Increase Contrast
```

- Respect them: shorter or no animations, heavier weights, a high-contrast `ThemeData` (`MaterialApp` has
  `highContrastTheme` and `highContrastDarkTheme`).

## Automated checks

### Guideline tests

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('checkout screen meets accessibility guidelines', (tester) async {
    final SemanticsHandle handle = tester.ensureSemantics();
    await tester.pumpWidget(const MaterialApp(home: CheckoutScreen()));

    await expectLater(tester, meetsGuideline(androidTapTargetGuideline)); // 48x48
    await expectLater(tester, meetsGuideline(iOSTapTargetGuideline));     // 44x44
    await expectLater(tester, meetsGuideline(labeledTapTargetGuideline)); // tappable nodes have labels
    await expectLater(tester, meetsGuideline(textContrastGuideline));     // WCAG text contrast
    handle.dispose();
  });
}
```

- `textContrastGuideline` samples pixels around each text node with a simple light and dark partition; it can
  miss text on images and gradients. Check those by hand.
- Run the same test with large text:

```dart
testWidgets('checkout works at 200 percent text', (tester) async {
  tester.platformDispatcher.textScaleFactorTestValue = 2.0;
  addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
  await tester.pumpWidget(const MaterialApp(home: CheckoutScreen()));
  expect(tester.takeException(), isNull); // no overflow errors
});
```

### Semantics assertions

```dart
final handle = tester.ensureSemantics();
expect(
  tester.getSemantics(find.byTooltip('Delete message')),
  matchesSemantics(label: 'Delete message', isButton: true, hasTapAction: true,
      hasEnabledState: true, isEnabled: true, isFocusable: true),
);
expect(find.bySemanticsLabel('Payment method'), findsOneWidget);
handle.dispose();
```

`matchesSemantics` matches all flags exactly; when only some flags matter, `containsSemantics` is less brittle.

### On device

- Flutter renders its own pixels, so platform tools see only what the semantics tree exposes. Run Android
  Accessibility Scanner and the iOS Accessibility Inspector on a release or profile build as well.
- `showSemanticsDebugger: true` on `MaterialApp` shows the semantics tree over the UI during development.
