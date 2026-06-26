# Plugin Testing Guide

## Overview

Testing Flutter plugins requires special handling due to platform-specific code (iOS/Android). This guide covers testing both the Dart and native parts of plugins.

## Testing App Code with Plugins

When your Flutter app uses plugins, you need to mock the platform channel calls in unit/widget tests.

### Basic Platform Channel Mock

```dart
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  
  group('MyPlugin Tests', () {
    setUp(() {
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(
        const MethodChannel('my.plugin.channel'),
        (MethodCall methodCall) async {
          if (methodCall.method == 'getPlatformVersion') {
            return 'Android 12';
          }
          if (methodCall.method == 'getBatteryLevel') {
            return 85;
          }
          return null;
        },
      );
    });
    
    tearDown(() {
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(
        const MethodChannel('my.plugin.channel'),
        null,
      );
    });
    
    testWidgets('gets platform version', (tester) async {
      final version = await MyPlugin.getPlatformVersion();
      expect(version, 'Android 12');
    });
  });
}
```

### Event Channel Mock

```dart
setUp(() {
  const eventChannel = EventChannel('my.plugin.events');
  
  TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
      .setMockStreamHandler(
    eventChannel,
    MockStreamHandler(),
  );
});

class MockStreamHandler implements StreamHandler {
  @override
  Stream onListen(Object? arguments, EventChannelSink? events) {
    // Stream mock events
    return Stream.periodic(const Duration(seconds: 1))
        .map((i) => 'event_$i');
  }
  
  @override
  void onCancel() {}
}
```

## Testing Plugin Packages

For testing the plugin itself (including native code), you need to create a test app.

### Directory Structure

```
my_plugin/
├── test/
│   ├── my_plugin_test.dart       # Unit tests
│   └── my_plugin_test.dart.tmp   # Generated
├── test_app/                      # Integration test app
│   ├── lib/
│   │   └── main.dart
│   └── integration_test/
│       └── app_test.dart
└── integration_test/
    └── app_test.dart              # Plugin integration tests
```

### Unit Testing Plugin Methods

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_plugin/my_plugin.dart';

void main() {
  group('MyPlugin', () {
    test('getPlatformVersion returns platform string', () async {
      final version = await MyPlugin.getPlatformVersion();
      expect(version, isNotNull);
      expect(version, isNotEmpty);
    });
  });
}
```

### Integration Testing Plugin

```dart
// test_app/integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_plugin_example/main.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('MyPlugin Integration Tests', () {
    testWidgets('plugin returns version', (tester) async {
      await tester.pumpWidget(const MyApp());
      
      final version = await MyPlugin.getPlatformVersion();
      expect(version, isNotNull);
    });
  });
}
```

## Testing Native Code

### iOS (Swift)

```swift
// Test/MyPluginTests.swift
import XCTest
@testable import MyPlugin

class MyPluginTests: XCTestCase {
    func testGetPlatformVersion() {
        let expectation = self.expectation(description: "version")
        
        MyPlugin().getPlatformVersion { version in
            XCTAssertNotNil(version)
            expectation.fulfill()
        }
        
        waitForExpectations(timeout: 5)
    }
}
```

### Android (Kotlin)

```kotlin
// app/src/test/java/com/example/MyPluginTest.kt
package com.example

import org.junit.Test
import org.junit.Assert.*

class MyPluginTest {
    @Test
    fun testGetPlatformVersion() {
        // Test implementation
    }
}
```

## Best Practices

1. **Mock in unit tests** - Use mock method channels for fast, isolated tests
2. **Test in integration tests** - Run actual plugin code in integration tests
3. **Test error handling** - Mock error scenarios to verify error handling
4. **Test on multiple platforms** - Run tests on Android, iOS, and web when applicable
5. **Clean up mocks** - Always clean up in tearDown to avoid test pollution

## Common Issues

### Plugin Not Registered

```dart
// Ensure binding is initialized
TestWidgetsFlutterBinding.ensureInitialized();
```

### Method Channel Not Found

```dart
// Verify channel name matches exactly
const MethodChannel('exact.channel.name');
```

### Event Stream Not Working

```dart
// Make sure to set up stream before pumping widget
await tester.pump();
```
