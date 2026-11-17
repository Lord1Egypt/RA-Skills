# Testing reference

Load this when adding or fixing Dart or Flutter tests. Packages: `flutter_test` (bundled), `test`,
`mocktail`, `fake_async`, `bloc_test` for Bloc apps, `integration_test` (bundled with the SDK).

## Pyramid

| Level | Tool | Tests | Speed |
|---|---|---|---|
| Unit | `package:test` or `flutter_test` | Repositories, mappers, notifiers, blocs, pure Dart | ms |
| Widget | `testWidgets` + `WidgetTester` | One screen or widget with faked dependencies | ms to s |
| Golden | `matchesGoldenFile` | Visual regressions of design-system widgets | s |
| Integration | `integration_test` on device or emulator | A few critical user flows end to end | min |

Most tests are unit and widget tests. Integration tests cover login, pairing, purchase: flows where a
break costs real money or support tickets.

## Fakes and mocks

```dart
class MockTodoRepository extends Mock implements TodoRepository {}
class FakeTodo extends Fake implements Todo {}

setUpAll(() => registerFallbackValue(FakeTodo())); // needed for any() on custom types

late MockTodoRepository repo;
setUp(() => repo = MockTodoRepository());

test('loads todos once', () async {
  when(() => repo.fetch()).thenAnswer((_) async => [Todo('1', 'Pair device')]);
  // ...
  verify(() => repo.fetch()).called(1);
  verifyNever(() => repo.add(any()));
});
```

- Stub futures with `thenAnswer((_) async => ...)`, never `thenReturn(Future...)`.
- Prefer a hand-written fake (an in-memory repository) when many tests need the same behaviour. Mocks
  are for verifying interactions.
- Mock your own interfaces, not third-party classes such as `http.Client` or `Dio` directly. Wrap them.

## Time

```dart
// BAD: real delay
await Future<void>.delayed(const Duration(seconds: 30));

// GOOD: virtual time with package:fake_async
test('retries after backoff', () {
  fakeAsync((async) {
    final values = <int>[];
    countdown(2).listen(values.add);
    async.elapse(const Duration(seconds: 3));
    expect(values, [2, 1, 0]);
  });
});
```

- Inside `testWidgets`, time is already fake: advance it with `tester.pump(duration)`.
- Inject a clock (`DateTime Function() now`) instead of calling `DateTime.now()` in logic.

## Riverpod

```dart
test('notifier loads todos', () async {
  when(() => repo.fetch()).thenAnswer((_) async => [Todo('1', 'Pair device')]);
  final container = ProviderContainer.test(
    overrides: [todoRepositoryProvider.overrideWithValue(repo)],
  );
  final sub = container.listen(todosProvider, (_, _) {}); // keeps autoDispose providers alive
  await expectLater(container.read(todosProvider.future), completion(hasLength(1)));
  sub.close();
});
```

- `ProviderContainer.test` disposes the container automatically at the end of the test.
- Widget tests wrap the tree in `ProviderScope(overrides: [...], child: ...)`.

## Bloc

```dart
blocTest<SearchBloc, SearchState>(
  'emits loading then results',
  setUp: () => when(() => api.search('ble')).thenAnswer((_) async => ['Sensor A']),
  build: () => SearchBloc(api),
  act: (bloc) => bloc.add(QueryChanged('ble')),
  expect: () => [isA<SearchLoading>(), isA<SearchResults>()],
);
```

- With value equality on states, compare whole states: `expect: () => [SearchLoading(), SearchResults(['Sensor A'])]`.
- Use `seed:` to start from a given state and `wait:` for debounced transformers.

## Widget tests

```dart
testWidgets('shows spinner then list', (tester) async {
  when(() => repo.fetch()).thenAnswer((_) async => [Todo('1', 'Pair device')]);
  await tester.pumpWidget(
    ProviderScope(
      overrides: [todoRepositoryProvider.overrideWithValue(repo)],
      child: const MaterialApp(home: Scaffold(body: TodosScreen())),
    ),
  );

  expect(find.byType(CircularProgressIndicator), findsOneWidget);
  await tester.pump(); // let the future complete and rebuild
  expect(find.text('Pair device'), findsOneWidget);
});
```

| Call | Does |
|---|---|
| `pump()` | One frame; microtasks and completed futures are processed |
| `pump(duration)` | Advances fake time, then one frame |
| `pumpAndSettle()` | Pumps until no frames are scheduled; fails with a timeout on endless animations |
| `runAsync(() => ...)` | Real async I/O (rare; files, real isolates) |

- Material widgets need `MaterialApp` and usually `Scaffold` (or `Material`) above them.
- Find by semantics a user sees (`find.text`, `find.bySemanticsLabel`, `find.byTooltip`) before `find.byKey`.
- `tester.enterText`, `tester.tap`, then `pump`; nothing rebuilds until a frame is pumped.

## Golden tests

```dart
testWidgets('device card', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: Scaffold(body: DeviceCard(device: sampleDevice))));
  await expectLater(find.byType(DeviceCard), matchesGoldenFile('goldens/device_card.png'));
}, tags: 'golden');
```

- Update with `flutter test --update-goldens`; review the PNG diff in the MR.
- Generate and compare on one pinned platform (usually the CI Linux image). Font rendering differs on
  macOS and Windows. Skip or tag goldens locally: `flutter test --exclude-tags golden`.
- Load real fonts in goldens, or text renders as boxes and hides layout bugs.

## Integration tests

```dart
// integration_test/pairing_test.dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('user pairs a device', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    await tester.tap(find.text('Add device'));
    // ...
  });
}
```

- Run: `flutter test integration_test --flavor staging`.
- Point at a test backend through `--dart-define-from-file`. Never at production with real user data.
- Native permission dialogs are outside Flutter; pre-grant permissions in the test setup or use a
  dedicated driver tool.

## CI commands

```bash
dart format --output=none --set-exit-if-changed .
flutter analyze
flutter test --coverage
```

- Fail the build on analyzer warnings, not only errors.
- Coverage is a signal, not a goal. Uncovered branches in notifiers and blocs matter more than widgets.
