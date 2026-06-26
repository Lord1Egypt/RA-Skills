# Common Testing Errors

## Overview

This guide covers common errors encountered when testing Flutter applications and their solutions.

## RenderFlex Overflow

### Error
```
A RenderFlex overflowed by [X] pixels on the [bottom/right].
```

### Cause
Widget exceeds its parent constraints, typically in Row or Column.

### Solution

```dart
// Problem
Row(
  children: [
    Icon(Icons.message),
    Column(children: [Text('Very long text...')]), // Overflow!
  ],
)

// Solution: Use Expanded
Row(
  children: [
    Icon(Icons.message),
    Expanded(child: Column(children: [Text('Very long text...')])),
  ],
)

// Alternative: Use Flexible
Row(
  children: [
    Icon(Icons.message),
    Flexible(child: Column(children: [Text('Very long text...')])),
  ],
)
```

## Unbounded Height

### Error
```
RenderBox was given unbounded height.
RenderBox was given unbounded width.
```

### Cause
ListView or other scrollable inside Column/Row without constraints.

### Solution

```dart
// Problem
Column(
  children: [
    Text('Header'),
    ListView(children: [...]), // Error!
  ],
)

// Solution 1: Use Expanded
Column(
  children: [
    Text('Header'),
    Expanded(child: ListView(children: [...])),  ],
)

// Solution 2: Use shrinkWrap
ListView(
  shrinkWrap: true,
  children: [...],
)
```

## SetState During Build

### Error
```
setState() called during build()
```

### Cause
Calling setState() during the build phase of a widget.

### Solution

```dart
// Problem
@override
Widget build(BuildContext context) {
  // Wrong: setState called during build
  someFuture.then((_) => setState(() {}));  
  return widget;
}

// Solution 1: Use post-build callback
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addPostFrameCallback((_) {
    setState(() {});
  });
}

// Solution 2: Use didChangeDependencies
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  _loadData();
}
```

## Finder Errors

### Error
```
Expected: exactly one matching node in the widget tree
Actual: ?: _WidgetTypeFinder:<zero widgets with type "X" found>
```

### Solution

```dart
// Check if widget exists before asserting
expect(find.byType(MyWidget), findsOneWidget);

// Use pumps to wait for widget to appear
await tester.pumpAndSettle();

// Check if text is present
expect(find.text('Loading...'), findsOneWidget);
await tester.pump();
expect(find.text('Loading...'), findsNothing);
```

## Async Errors

### Error
```
Test timed out after 5 seconds
```

### Solution

```dart
// Add timeout to async operations
await tester.runAsync(() async {
  await longRunningOperation();
});

// Use pumpAndSettle with timeout
await tester.pumpAndSettle(const Duration(seconds: 10));
```

## Navigation Errors

### Error
```
Could not find a generator for route RouteSettings<...>
```

### Solution

```dart
// Wrap your app with MaterialApp for navigation testing
await tester.pumpWidget(
  MaterialApp(
    home: MyHomePage(),
    routes: {
      '/detail': (context) => DetailPage(),
    },
  ),
);

// For named routes
await tester.tap(find.text('Go to Detail'));
await tester.pumpAndSettle();
```

## Platform Channel Errors

### Error
```
MissingPluginException(No implementation found for method...)
```

### Solution

```dart
TestWidgetsFlutterBinding.ensureInitialized();

// Mock the platform channel
TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
    .setMockMethodCallHandler(
  const MethodChannel('plugin/channel'),
  (MethodCall methodCall) async {
    // Return mock response
    return 'mock response';
  },
);
```
