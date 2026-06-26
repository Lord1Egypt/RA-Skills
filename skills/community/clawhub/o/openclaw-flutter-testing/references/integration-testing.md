# Integration Testing Guide

## Overview

Integration tests test complete apps or large parts on real devices or emulators. They verify that different parts of your application work together correctly.

## When to Use Integration Tests

- Testing complete user flows
- Verifying multiple screens/pages
- Testing navigation flows
- Performance profiling
- End-to-end testing

## Setup

Add to `pubspec.yaml`:

```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
```

Create `integration_test/app_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  group('end-to-end test', () {
    testWidgets('complete user flow', (tester) async {
      await tester.pumpWidget(const MyApp());
      
      // Step 1: Navigate to screen
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle();
      
      // Step 2: Enter credentials
      await tester.enterText(find.byKey(const Key('username')), 'user');
      await tester.enterText(find.byKey(const Key('password')), 'pass');
      
      // Step 3: Submit
      await tester.tap(find.text('Submit'));
      await tester.pumpAndSettle();
      
      // Verify result
      expect(find.text('Welcome'), findsOneWidget);
    });
  });
}
```

## Running Integration Tests

```bash
# On connected device/emulator
flutter test integration_test/

# With specific device
flutter test integration_test/ -d <device-id>
```

## Performance Testing

```dart
testWidgets('scrolling performance', (tester) async {
  await tester.pumpWidget(const MyApp());
  
  final listFinder = find.byType(ListView);
  
  // Measure performance
  final timeline = await tester.trace(() async {
    await tester.fling(listFinder, const Offset(0, -500), 10000);
    await tester.pumpAndSettle();
  });
  
  // Analyze timeline
  final frameCount = timeline.frames.length;
  final averageFrameTime = timeline.frames
      .map((f) => f.buildDuration.inMicroseconds)
      .reduce((a, b) => a + b) / frameCount;
  
  expect(averageFrameTime, lessThan(17000)); // 60fps
});
```

## CI Integration

### GitHub Actions

```yaml
name: Integration Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test integration_test/
```

## Best Practices

1. tests focused Keep on user flows
2. Use realistic data
3. Clean up test data after tests
4. Don't over-rely on integration tests (expensive to run)
5. Use performance benchmarks for critical paths
