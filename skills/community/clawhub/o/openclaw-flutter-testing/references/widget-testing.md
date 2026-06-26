# Widget Testing Guide

## Overview

Widget tests verify widget UI appearance and behavior in a test environment.

## When to Use Widget Tests

- Testing widget rendering
- Verifying user interactions (taps, drags, scrolling)
- Testing different orientations
- Validating widget state changes

## Finding Widgets

```dart
// By text
final titleFinder = find.text('Title');

// By widget type
final buttonFinder = find.byType(ElevatedButton);

// By key
final fabFinder = find.byKey(const ValueKey('increment'));

// By widget instance
final myWidgetFinder = find.byWidget(myWidgetInstance);

// By descendant
final listFinder = find.descendant(
  of: find.byType(ListView),
  matching: find.byType(ListTile),
);
```

## User Interactions

```dart
// Tap
await tester.tap(buttonFinder);
await tester.tap(find.byIcon(Icons.add));

// Double tap
await tester.tap(buttonFinder);
await tester.tap(buttonFinder);

// Long press
await tester.longPress(buttonFinder);

// Drag
await tester.drag(listFinder, const Offset(0, -300));

// Enter text
await tester.enterText(fieldFinder, 'Hello World');

// Scroll
await tester.fling(listFinder, const Offset(0, -500), 10000);
await tester.pumpAndSettle();

// Drag and drop
await tester.dragUntilVisible(
  targetFinder,
  scrollableFinder,
  const Offset(0, -100),
);
```

## Testing State Changes

```dart
testWidgets('counter increments on tap', (tester) async {
  await tester.pumpWidget(const MyWidget());
  
  // Initial state
  expect(find.text('0'), findsOneWidget);
  
  // Tap button
  await tester.tap(find.byIcon(Icons.add));
  await tester.pump();
  
  // Verify state changed
  expect(find.text('1'), findsOneWidget);
});
```

## Testing Different Orientations

```dart
testWidgets('widget in landscape mode', (tester) async {
  await tester.binding.setSurfaceSize(const Size(800, 400));
  await tester.pumpWidget(const MyApp());
  
  // Verify landscape behavior
  expect(find.byType(MyWidget), findsOneWidget);
  
  addTearDown(tester.binding.setSurfaceSize(null));
});
```

## Common Patterns

### Pump and Settle

```dart
// Wait for all animations to complete
await tester.pumpAndSettle();

// Wait for specific duration
await tester.pump(const Duration(milliseconds: 500));

// Pump one frame without waiting
await tester.pump();
```

### Rebuilds

```dart
// Rebuild widget
await tester.pumpWidget(newWidget);

// Pump and settle with duration
await tester.pumpAndSettle(const Duration(seconds: 5));
```
