# Unit Testing Guide

## Overview

Unit tests verify the correctness of a unit of logic under various conditions. They are the foundation of the testing pyramid.

## When to Use Unit Tests

- Testing business logic functions
- Validating data transformations
- Testing state management logic
- Mocking external services/API calls

## Key Concepts

- Use `package:test/test.dart`
- Mock dependencies using Mockito or similar
- Avoid file I/O or UI rendering
- Fast execution, high maintainability

## Mockito Basics

```dart
import 'package:mockito/mockito.dart';
import 'package:flutter_test/flutter_test.dart';

class MockRepository extends Mock implements Repository {}

void main() {
  late MockRepository mockRepository;
  late UseCase useCase;

  setUp(() {
    mockRepository = MockRepository();
    useCase = UseCase(mockRepository);
  });

  test('should get data from repository', () async {
    // Arrange
    when(mockRepository.getData()).thenAnswer((_) async => 'test data');

    // Act
    final result = await useCase.execute();

    // Assert
    expect(result, 'test data');
    verify(mockRepository.getData());
  });
}
```

## Best Practices

1. Test one thing per test
2. Use descriptive test names
3. Follow Arrange-Act-Assert pattern
4. Keep tests independent
5. Mock external dependencies
