# Mocking Guide

## Overview

Mocking is essential for writing fast, reliable unit and widget tests by isolating the code under test from external dependencies.

## Using Mockito

Add to `pubspec.yaml`:

```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

### Basic Mock

```dart
import 'package:mockito/mockito.dart';
import 'package:flutter_test/flutter_test.dart';

class MockDataSource extends Mock implements DataSource {}

void main() {
  late MockDataSource mockDataSource;
  late Repository repository;

  setUp(() {
    mockDataSource = MockDataSource();
    repository = Repository(mockDataSource);
  });

  test('should return data from data source', () async {
    // Arrange
    when(mockDataSource.getData()).thenAnswer((_) async => 'test data');

    // Act
    final result = await repository.getData();

    // Assert
    expect(result, 'test data');
    verify(mockDataSource.getData()).called(1```

###);
  });
}
 Stubbing Different Methods

```dart
// Stub with specific argument
when(mockDataSource.getById(1)).thenAnswer((_) async => User(id: 1));

// Stub with any argument
when(mockDataSource.getById(any)).thenAnswer((_) async => User(id: 0));

// Stub with matcher
when(mockDataSource.getById(argThat(isPositive))).thenAnswer((_) async => User(id: 1));

// Stub with exception
when(mockDataSource.getData()).thenThrow(Exception('Network error'));
```

### Verifying Calls

```dart
// Verify method was called
verify(mockDataSource.getData()).called(1);

// Verify method was called with specific argument
verify(mockDataSource.saveData('test'));

// Verify no more interactions
verifyNoMoreInteractions(mockDataSource);

// Verify zero calls
verifyNever(mockDataSource.deleteData());
```

## Fake Implementation

```dart
class FakeRepository extends Fake implements Repository {
  @override
  Future<User> getUser(int id) async {
    return User(id: id, name: 'Fake User');
  }
}

void main() {
  setUpAll(() {
    registerFallbackValue(FakeRepository());
  });
}
```

## Platform Channel Mocks

```dart
import 'package:flutter/services.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  
  setUp(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('my.plugin/channel'),
      (MethodCall methodCall) async {
        if (methodCall.method == 'getPlatformVersion') {
          return 'Android 12';
        }
        return null;
      },
    );
  });
  
  tearDown(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('my.plugin/channel'),
      null,
    );
  });
}
```

## Best Practices

1. Mock at the boundary of your system (repositories, services)
2. Don't mock value objects or data classes
3. Use fakes for complex dependencies when mocks are too complicated
4. Always register fallback values for complex arguments
5. Clean up mocks in tearDown
